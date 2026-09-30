from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.application.exceptions import ConflictError, NotFoundError, ValidationError
from app.application.use_cases.category_use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
)
from app.domain.entities.user import ROLE_ADMIN
from app.infrastructure.repositories.sqlalchemy_category_repository import (
    SqlAlchemyCategoryRepository,
)
from app.infrastructure.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)
from app.interfaces.http.decorators import role_required

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")
category_repository = SqlAlchemyCategoryRepository()
product_repository = SqlAlchemyProductRepository()


@category_bp.get("")
@jwt_required()
def list_categories():
    """List all categories
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    responses:
      200:
        description: A list of categories
      401:
        description: Missing or invalid access token
    """
    categories = ListCategoriesUseCase(category_repository).execute()
    return jsonify([category.to_dict() for category in categories])


@category_bp.post("")
@role_required(ROLE_ADMIN)
def create_category():
    """Create a new category (admin only)
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    description: >
      Set parent_id to create a subcategory. Only one level of nesting is
      supported -- a subcategory cannot itself have subcategories.
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
              example: Beverages
            parent_id:
              type: integer
              description: Set to make this a subcategory of an existing top-level category
              example: null
    responses:
      201:
        description: Category created
      400:
        description: Missing name, category already exists at this level, or invalid parent
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: parent_id does not exist
    """
    data = request.get_json(silent=True) or {}
    try:
        category = CreateCategoryUseCase(category_repository).execute(
            data.get("name"), data.get("parent_id")
        )
    except (ValidationError, ConflictError) as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(category.to_dict()), 201


@category_bp.put("/<int:category_id>")
@role_required(ROLE_ADMIN)
def update_category(category_id):
    """Rename a category (admin only)
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - name: category_id
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
              example: Snacks
            parent_id:
              type: integer
              description: Set/change the parent category, or null to make it top-level
    responses:
      200:
        description: Category updated
      400:
        description: Invalid name, invalid parent, or name already taken at this level
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Category (or parent_id) not found
    """
    data = request.get_json(silent=True) or {}
    try:
        category = UpdateCategoryUseCase(category_repository).execute(category_id, **data)
    except (ValidationError, ConflictError) as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(category.to_dict())


@category_bp.delete("/<int:category_id>")
@role_required(ROLE_ADMIN)
def delete_category(category_id):
    """Delete a category (admin only)
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Category deleted
      400:
        description: Category still has products assigned to it
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Category not found
    """
    try:
        DeleteCategoryUseCase(category_repository, product_repository).execute(category_id)
    except ConflictError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return "", 204
