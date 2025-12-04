from functools import wraps
from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            token = token.split(" ")[1]  # "Bearer <token>"
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data["username"]
        except:
            return jsonify({"error": "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated
