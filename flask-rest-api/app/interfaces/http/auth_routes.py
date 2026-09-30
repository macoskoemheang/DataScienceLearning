from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app.application.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.application.use_cases.auth_use_cases import (
    AuthenticateUserUseCase,
    GetUserUseCase,
    RegisterUserUseCase,
)
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
user_repository = SqlAlchemyUserRepository()


@auth_bp.post("/register")
def register():
    """Register a new account
    ---
    tags:
      - Auth
    description: >
      Public self-registration. The very first account created in the
      system automatically becomes an admin; every account after that is
      created as a cashier. Admins can create further staff with an
      explicit role via POST /api/employees.
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
              example: alice
            password:
              type: string
              example: secret123
    responses:
      201:
        description: User created
      400:
        description: Missing fields or username already taken
    """
    data = request.get_json(silent=True) or {}
    try:
        user = RegisterUserUseCase(user_repository).execute(
            data.get("username"), data.get("password")
        )
    except (ValidationError, ConflictError) as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(user.to_dict()), 201


@auth_bp.post("/login")
def login():
    """Log in and receive JWT access + refresh tokens
    ---
    tags:
      - Auth
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
              example: alice
            password:
              type: string
              example: secret123
    responses:
      200:
        description: Login successful, returns access_token and refresh_token
      401:
        description: Invalid credentials
    """
    data = request.get_json(silent=True) or {}
    try:
        user = AuthenticateUserUseCase(user_repository).execute(
            data.get("username"), data.get("password")
        )
    except AuthenticationError as e:
        return jsonify({"error": str(e)}), 401

    claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Exchange a refresh token for a new access token
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: New access_token
      401:
        description: Missing or invalid refresh token
    """
    identity = get_jwt_identity()
    claims = {"role": get_jwt().get("role")}
    access_token = create_access_token(identity=identity, additional_claims=claims)
    return jsonify(access_token=access_token)


@auth_bp.get("/me")
@jwt_required()
def me():
    """Get the current logged-in user
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: The current user
      401:
        description: Missing or invalid access token
    """
    try:
        user = GetUserUseCase(user_repository).execute(int(get_jwt_identity()))
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(user.to_dict())
