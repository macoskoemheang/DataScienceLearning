from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from extensions import db
from models import Task

api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/tasks")
@jwt_required()
def list_tasks():
    """List all tasks
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: A list of tasks
      401:
        description: Missing or invalid access token
    """
    tasks = Task.query.order_by(Task.id).all()
    return jsonify([task.to_dict() for task in tasks])


@api.get("/tasks/<int:task_id>")
@jwt_required()
def get_task(task_id):
    """Get a single task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The requested task
      401:
        description: Missing or invalid access token
      404:
        description: Task not found
    """
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


@api.post("/tasks")
@jwt_required()
def create_task():
    """Create a new task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: Learn Flask
            description:
              type: string
              example: Build a REST API
            done:
              type: boolean
              example: false
    responses:
      201:
        description: Task created
      400:
        description: Missing or invalid title
      401:
        description: Missing or invalid access token
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "'title' is required"}), 400

    task = Task(
        title=title,
        description=data.get("description", ""),
        done=bool(data.get("done", False)),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api.put("/tasks/<int:task_id>")
@jwt_required()
def update_task(task_id):
    """Update an existing task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            done:
              type: boolean
    responses:
      200:
        description: Task updated
      400:
        description: Invalid title
      401:
        description: Missing or invalid access token
      404:
        description: Task not found
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}

    if "title" in data:
        if not data["title"]:
            return jsonify({"error": "'title' cannot be empty"}), 400
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "done" in data:
        task.done = bool(data["done"])

    db.session.commit()
    return jsonify(task.to_dict())


@api.delete("/tasks/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    """Delete a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Task deleted
      401:
        description: Missing or invalid access token
      404:
        description: Task not found
    """
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204
