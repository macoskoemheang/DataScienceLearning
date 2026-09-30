from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.application.exceptions import NotFoundError, ValidationError
from app.application.use_cases.customer_use_cases import (
    CreateCustomerUseCase,
    GetCustomerUseCase,
    ListCustomersUseCase,
    UpdateCustomerUseCase,
)
from app.infrastructure.repositories.sqlalchemy_customer_repository import (
    SqlAlchemyCustomerRepository,
)

customer_bp = Blueprint("customers", __name__, url_prefix="/api/customers")
customer_repository = SqlAlchemyCustomerRepository()


@customer_bp.get("")
@jwt_required()
def list_customers():
    """List customers (paginated, with optional name search)
    ---
    tags:
      - Customers
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
      - name: search
        in: query
        type: string
        description: Filter by customer name (case-insensitive substring)
    responses:
      200:
        description: A page of customers with pagination metadata
      401:
        description: Missing or invalid access token
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    search = request.args.get("search")

    customers, total = ListCustomersUseCase(customer_repository).execute_paginated(
        page=page, per_page=per_page, search=search
    )
    return jsonify(
        {
            "items": [customer.to_dict() for customer in customers],
            "page": page,
            "per_page": per_page,
            "total": total,
        }
    )


@customer_bp.get("/<int:customer_id>")
@jwt_required()
def get_customer(customer_id):
    """Get a single customer by ID
    ---
    tags:
      - Customers
    security:
      - Bearer: []
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The requested customer
      401:
        description: Missing or invalid access token
      404:
        description: Customer not found
    """
    try:
        customer = GetCustomerUseCase(customer_repository).execute(customer_id)
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(customer.to_dict())


@customer_bp.post("")
@jwt_required()
def create_customer():
    """Create a new customer
    ---
    tags:
      - Customers
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: John Doe
            phone:
              type: string
              example: "012345678"
            email:
              type: string
              example: john@example.com
    responses:
      201:
        description: Customer created
      400:
        description: Missing name
      401:
        description: Missing or invalid access token
    """
    data = request.get_json(silent=True) or {}
    try:
        customer = CreateCustomerUseCase(customer_repository).execute(
            name=data.get("name"),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
        )
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(customer.to_dict()), 201


@customer_bp.put("/<int:customer_id>")
@jwt_required()
def update_customer(customer_id):
    """Update an existing customer
    ---
    tags:
      - Customers
    security:
      - Bearer: []
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            phone:
              type: string
            email:
              type: string
    responses:
      200:
        description: Customer updated
      400:
        description: Invalid fields
      401:
        description: Missing or invalid access token
      404:
        description: Customer not found
    """
    data = request.get_json(silent=True) or {}
    try:
        customer = UpdateCustomerUseCase(customer_repository).execute(customer_id, **data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(customer.to_dict())
