from flasgger import Swagger
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import Config
from app.infrastructure.extensions import db
from app.interfaces.http.auth_routes import auth_bp
from app.interfaces.http.category_routes import category_bp
from app.interfaces.http.customer_routes import customer_bp
from app.interfaces.http.dashboard_routes import dashboard_bp
from app.interfaces.http.employee_routes import employee_bp
from app.interfaces.http.product_routes import product_bp
from app.interfaces.http.sale_routes import sale_bp

SWAGGER_TEMPLATE = {
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: **Bearer &lt;your access_token&gt;**",
        }
    },
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    origins = app.config["CORS_ORIGINS"]
    CORS(app, resources={r"/api/*": {"origins": origins.split(",") if origins != "*" else "*"}})

    db.init_app(app)
    JWTManager(app)
    Swagger(app, template=SWAGGER_TEMPLATE)

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(sale_bp)
    app.register_blueprint(dashboard_bp)

    @app.get("/")
    def index():
        return redirect("/apidocs/")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Not found"}), 404

    with app.app_context():
        db.create_all()

    return app
