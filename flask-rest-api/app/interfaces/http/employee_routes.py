from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.application.exceptions import ConflictError, NotFoundError, ValidationError
from app.application.use_cases.auth_use_cases import (
    CreateEmployeeUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    UpdateEmployeeUseCase,
)
from app.domain.entities.user import ROLE_ADMIN
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.interfaces.http.decorators import role_required

employee_bp = Blueprint("employees", __name__, url_prefix="/api/employees")
user_repository = SqlAlchemyUserRepository()


@employee_bp.get("")
@role_required(ROLE_ADMIN)
def list_employees():
    """List all employees (admin only)
    ---
    tags:
      - Employees
    security:
      - Bearer: []
    responses:
      200:
        description: A list of employees
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
    """
    users = ListUsersUseCase(user_repository).execute()
    return jsonify([user.to_dict() for user in users])


@employee_bp.post("")
@role_required(ROLE_ADMIN)
def create_employee():
    """Create a new employee with a specific role (admin only)
    ---
    tags:
      - Employees
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: bob
            password:
              type: string
              example: secret123
            role:
              type: string
              enum: [admin, cashier]
              example: cashier
    responses:
      201:
        description: Employee created
      400:
        description: Missing/invalid fields or username already taken
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
    """
    data = request.get_json(silent=True) or {}
    try:
        user = CreateEmployeeUseCase(user_repository).execute(
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role", "cashier"),
        )
    except (ValidationError, ConflictError) as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(user.to_dict()), 201


@employee_bp.get("/<int:employee_id>")
@role_required(ROLE_ADMIN)
def get_employee(employee_id):
    """Get a single employee by ID (admin only)
    ---
    tags:
      - Employees
    security:
      - Bearer: []
    parameters:
      - name: employee_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The requested employee
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Employee not found
    """
    try:
        user = GetUserUseCase(user_repository).execute(employee_id)
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(user.to_dict())


@employee_bp.put("/<int:employee_id>")
@role_required(ROLE_ADMIN)
def update_employee(employee_id):
    """Update an employee's role or active status (admin only)
    ---
    tags:
      - Employees
    description: >
      Employees are never hard-deleted (past sales reference them) --
      set is_active to false to revoke access instead. An admin cannot
      modify their own account through this endpoint.
    security:
      - Bearer: []
    parameters:
      - name: employee_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            role:
              type: string
              enum: [admin, cashier]
            is_active:
              type: boolean
    responses:
      200:
        description: Employee updated
      400:
        description: Invalid role, or attempting to modify your own account
      401:
        description: Missing or invalid access token
      403:
        description: Caller is not an admin
      404:
        description: Employee not found
    """
    if employee_id == int(get_jwt_identity()):
        return jsonify({"error": "admins cannot modify their own account here"}), 400

    data = request.get_json(silent=True) or {}
    try:
        user = UpdateEmployeeUseCase(user_repository).execute(
            employee_id, role=data.get("role"), is_active=data.get("is_active")
        )
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(user.to_dict())
