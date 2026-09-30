from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.application.exceptions import ConflictError, NotFoundError, ValidationError
from app.application.use_cases.product_use_cases import (
    AddStockUseCase,
    CreateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
)
from app.domain.entities.user import ROLE_ADMIN
from app.infrastructure.repositories.sqlalchemy_category_repository import (
    SqlAlchemyCategoryRepository,
)
from app.infrastructure.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)
from app.infrastructure.repositories.sqlalchemy_sale_repository import SqlAlchemySaleRepository
from app.interfaces.http.decorators import role_required

product_bp = Blueprint("products", __name__, url_prefix="/api/products")
product_repository = SqlAlchemyProductRepository()
category_repository = SqlAlchemyCategoryRepository()
sale_repository = SqlAlchemySaleRepository()


@product_bp.get("")
@jwt_required()
def list_products():
    """List products (paginated, with optional search and category filter)
    ---
    tags:
      - Products
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
        description: Filter by product name (case-insensitive substring)
      - name: category_id
        in: query
        type: integer
    responses:
      200:
        description: A page of products with pagination metadata
      401:
        description: Missing or invalid access token
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    search = request.args.get("search")
    category_id = request.args.get("category_id", type=int)

    products, total = ListProductsUseCase(product_repository).execute_paginated(
        page=page, per_page=per_page, search=search, category_id=category_id
    )
    return jsonify(
        {
            "items": [product.to_dict() for product in products],
            "page": page,
            "per_page": per_page,
            "total": total,
        }
    )


@product_bp.get("/<int:product_id>")
@jwt_required()
def get_product(product_id):
    """Get a single product by ID
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The requested product
      401:
        description: Missing or invalid access token
      404:
        description: Product not found
    """
    try:
        product = GetProductUseCase(product_repository).execute(product_id)
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(product.to_dict())


@product_bp.post("")
@role_required(ROLE_ADMIN)
def create_product():
    """Create a new product (admin only)
    ---
    tags:
      - Products
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
            - price
          properties:
            name:
              type: string
              example: Iced Coffee
            sku:
              type: string
              example: BEV-001
            price:
              type: number
              example: 2.50
            stock_quantity:
              type: integer
              example: 100
            category_id:
              type: integer
              example: 1
    responses:
      201:
        description: Product created
      400:
        description: Missing or invalid fields
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
    """
    data = request.get_json(silent=True) or {}
    try:
        product = CreateProductUseCase(product_repository, category_repository).execute(
            name=data.get("name"),
            price=data.get("price"),
            sku=data.get("sku", ""),
            stock_quantity=data.get("stock_quantity", 0),
            category_id=data.get("category_id"),
        )
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(product.to_dict()), 201


@product_bp.put("/<int:product_id>")
@role_required(ROLE_ADMIN)
def update_product(product_id):
    """Update an existing product (admin only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: product_id
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
            sku:
              type: string
            price:
              type: number
            stock_quantity:
              type: integer
            category_id:
              type: integer
    responses:
      200:
        description: Product updated
      400:
        description: Invalid fields
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Product not found
    """
    data = request.get_json(silent=True) or {}
    try:
        product = UpdateProductUseCase(product_repository, category_repository).execute(
            product_id, **data
        )
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(product.to_dict())


@product_bp.post("/<int:product_id>/stock")
@role_required(ROLE_ADMIN)
def add_stock(product_id):
    """Add stock to a product (restock; admin only)
    ---
    tags:
      - Products
    description: >
      Adds ``quantity`` to the product's current stock_quantity, rather than
      overwriting it -- use this for receiving new inventory. Use PUT
      /api/products/<id> instead if you need to set an exact stock value.
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - quantity
          properties:
            quantity:
              type: integer
              example: 50
    responses:
      200:
        description: Stock added, returns the updated product
      400:
        description: quantity must be a positive integer
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Product not found
    """
    data = request.get_json(silent=True) or {}
    try:
        product = AddStockUseCase(product_repository).execute(product_id, data.get("quantity"))
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(product.to_dict())


@product_bp.delete("/<int:product_id>")
@role_required(ROLE_ADMIN)
def delete_product(product_id):
    """Delete a product (admin only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Product deleted
      400:
        description: Product has existing sales and cannot be deleted
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Product not found
    """
    try:
        DeleteProductUseCase(product_repository, sale_repository).execute(product_id)
    except ConflictError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return "", 204
