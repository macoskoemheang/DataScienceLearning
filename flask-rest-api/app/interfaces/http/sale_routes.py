from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.application.exceptions import NotFoundError, ValidationError
from app.application.use_cases.sale_use_cases import (
    CreateSaleUseCase,
    GetSaleUseCase,
    ListSalesUseCase,
)
from app.infrastructure.repositories.sqlalchemy_customer_repository import (
    SqlAlchemyCustomerRepository,
)
from app.infrastructure.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)
from app.infrastructure.repositories.sqlalchemy_sale_repository import SqlAlchemySaleRepository

sale_bp = Blueprint("sales", __name__, url_prefix="/api/sales")
sale_repository = SqlAlchemySaleRepository()
product_repository = SqlAlchemyProductRepository()
customer_repository = SqlAlchemyCustomerRepository()


@sale_bp.get("")
@jwt_required()
def list_sales():
    """List sales (paginated, most recent first, optional date range)
    ---
    tags:
      - Sales
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 20
      - name: start_date
        in: query
        type: string
        description: ISO date/time, e.g. 2026-09-01
      - name: end_date
        in: query
        type: string
        description: ISO date/time, e.g. 2026-09-30
    responses:
      200:
        description: A page of sales with pagination metadata
      400:
        description: Invalid start_date/end_date format
      401:
        description: Missing or invalid access token
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    try:
        start_date = _parse_date(request.args.get("start_date"))
        end_date = _parse_date(request.args.get("end_date"))
    except ValueError:
        return jsonify({"error": "start_date/end_date must be ISO format, e.g. 2026-09-01"}), 400

    sales, total = ListSalesUseCase(sale_repository).execute_paginated(
        page=page, per_page=per_page, start_date=start_date, end_date=end_date
    )
    return jsonify(
        {
            "items": [sale.to_dict() for sale in sales],
            "page": page,
            "per_page": per_page,
            "total": total,
        }
    )


def _parse_date(value):
    return datetime.fromisoformat(value) if value else None


@sale_bp.get("/<int:sale_id>")
@jwt_required()
def get_sale(sale_id):
    """Get a single sale by ID
    ---
    tags:
      - Sales
    security:
      - Bearer: []
    parameters:
      - name: sale_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The requested sale
      401:
        description: Missing or invalid access token
      404:
        description: Sale not found
    """
    try:
        sale = GetSaleUseCase(sale_repository).execute(sale_id)
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(sale.to_dict())


@sale_bp.post("/checkout")
@jwt_required()
def checkout():
    """Checkout a cart: creates a sale, snapshots prices, and decrements stock
    ---
    tags:
      - Sales
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - items
          properties:
            customer_id:
              type: integer
              example: 1
            items:
              type: array
              items:
                type: object
                required:
                  - product_id
                  - quantity
                properties:
                  product_id:
                    type: integer
                    example: 1
                  quantity:
                    type: integer
                    example: 2
    responses:
      201:
        description: Sale created
      400:
        description: Invalid items or insufficient stock
      401:
        description: Missing or invalid access token
      404:
        description: Product or customer not found
    """
    data = request.get_json(silent=True) or {}
    employee_id = int(get_jwt_identity())

    try:
        sale = CreateSaleUseCase(sale_repository, product_repository, customer_repository).execute(
            employee_id=employee_id,
            items=data.get("items", []),
            customer_id=data.get("customer_id"),
        )
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(sale.to_dict()), 201
