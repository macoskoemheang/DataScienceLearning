from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.application.use_cases.dashboard_use_cases import (
    GetDashboardSummaryUseCase,
    LowStockProductsUseCase,
    RecentSalesUseCase,
    TopProductsUseCase,
)
from app.infrastructure.repositories.sqlalchemy_customer_repository import (
    SqlAlchemyCustomerRepository,
)
from app.infrastructure.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)
from app.infrastructure.repositories.sqlalchemy_sale_repository import SqlAlchemySaleRepository

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")
sale_repository = SqlAlchemySaleRepository()
product_repository = SqlAlchemyProductRepository()
customer_repository = SqlAlchemyCustomerRepository()


@dashboard_bp.get("/summary")
@jwt_required()
def summary():
    """Dashboard summary: revenue, sale count, product/customer counts, low stock
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    parameters:
      - name: low_stock_threshold
        in: query
        type: integer
        default: 5
    responses:
      200:
        description: Summary metrics
      401:
        description: Missing or invalid access token
    """
    threshold = request.args.get("low_stock_threshold", 5, type=int)
    data = GetDashboardSummaryUseCase(
        sale_repository, product_repository, customer_repository
    ).execute(low_stock_threshold=threshold)
    return jsonify(data)


@dashboard_bp.get("/top-products")
@jwt_required()
def top_products():
    """Best-selling products by quantity sold
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    parameters:
      - name: limit
        in: query
        type: integer
        default: 5
    responses:
      200:
        description: Ranked list of products with quantity_sold and revenue
      401:
        description: Missing or invalid access token
    """
    limit = request.args.get("limit", 5, type=int)
    data = TopProductsUseCase(sale_repository, product_repository).execute(limit=limit)
    return jsonify(data)


@dashboard_bp.get("/low-stock")
@jwt_required()
def low_stock():
    """Products at or below a stock threshold
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    parameters:
      - name: threshold
        in: query
        type: integer
        default: 5
    responses:
      200:
        description: List of low-stock products
      401:
        description: Missing or invalid access token
    """
    threshold = request.args.get("threshold", 5, type=int)
    products = LowStockProductsUseCase(product_repository).execute(threshold=threshold)
    return jsonify([product.to_dict() for product in products])


@dashboard_bp.get("/recent-sales")
@jwt_required()
def recent_sales():
    """Most recent sales
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    parameters:
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: List of the most recent sales, newest first
      401:
        description: Missing or invalid access token
    """
    limit = request.args.get("limit", 10, type=int)
    sales = RecentSalesUseCase(sale_repository).execute(limit=limit)
    return jsonify([sale.to_dict() for sale in sales])
