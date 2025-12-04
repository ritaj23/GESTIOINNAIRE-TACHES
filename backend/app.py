from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(tasks_bp, url_prefix="/api")

@app.route("/")
def home():
    return {"message": "Backend works!"}

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8000, debug=True)

