import os

from flasgger import Swagger
from flask import Flask, jsonify, redirect
from flask_jwt_extended import JWTManager

from auth import auth
from extensions import db
from routes import api

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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")
    app.config["SWAGGER"] = {
        "title": "Task Manager API",
        "uiversion": 3,
    }

    db.init_app(app)
    JWTManager(app)
    Swagger(app, template=SWAGGER_TEMPLATE)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    @app.get("/")
    def index():
        return redirect("/apidocs/")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Not found"}), 404

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
