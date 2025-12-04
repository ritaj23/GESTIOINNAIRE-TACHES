from flask import Blueprint, request, jsonify
from config.db import tasks_collection
from bson.objectid import ObjectId
from utils.token import token_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/tasks", methods=["POST"])
@token_required
def create_task(current_user):
    data = request.get_json()
    task = {
        "title": data.get("title"),
        "description": data.get("description"),
        "owner": current_user,
        "collaborators": data.get("collaborators", []),
        "completed": False
    }
    result = tasks_collection.insert_one(task)
    return jsonify({"message": "Task created", "id": str(result.inserted_id)}), 201

@tasks_bp.route("/tasks", methods=["GET"])
@token_required
def get_tasks(current_user):
    tasks = list(tasks_collection.find())
    filtered_tasks = []
    for task in tasks:
        if task["owner"] == current_user or current_user in task.get("collaborators", []):
            task["_id"] = str(task["_id"])
            filtered_tasks.append(task)
    return jsonify(filtered_tasks)

@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
@token_required
def update_task(current_user, task_id):
    data = request.get_json()
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if task["owner"] != current_user:
        return jsonify({"error": "Not allowed"}), 403
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {
            "title": data.get("title"),
            "description": data.get("description"),
            "completed": data.get("completed", False),
            "collaborators": data.get("collaborators", [])
        }}
    )
    return jsonify({"message": "Task updated"}), 200

@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if task["owner"] != current_user:
        return jsonify({"error": "Not allowed"}), 403
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"message": "Task deleted"}), 200
