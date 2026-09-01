from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from extensions import db
from models import User

auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.post("/register")
def register():
    """Register a new user
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
      201:
        description: User created
      400:
        description: Missing fields or username already taken
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "'username' and 'password' are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already taken"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth.post("/login")
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
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password or ""):
        return jsonify({"error": "invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth.post("/refresh")
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
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@auth.get("/me")
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
    user = User.query.get_or_404(int(get_jwt_identity()))
    return jsonify(user.to_dict())


@auth.get("/users")
@jwt_required()
def list_users():
    """List all registered users
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: A list of users
      401:
        description: Missing or invalid access token
    """
    users = User.query.order_by(User.id).all()
    return jsonify([user.to_dict() for user in users])
