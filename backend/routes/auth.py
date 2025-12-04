from flask import Blueprint, request, jsonify
from config.db import users_collection
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400
    users_collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        token = jwt.encode(
            {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"message": "Login successful!", "token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
