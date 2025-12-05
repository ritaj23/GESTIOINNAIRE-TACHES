from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# رابط الاتصال بالمونغو
client = MongoClient("mongodb://localhost:27017/")  # هذا إذا كان MongoDB خارجي
db = client["gestionnaire"]  # اسم قاعدة البيانات

tasks_collection = db["tasks"]

@app.route("/tasks")
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    return jsonify(tasks)

@app.route("/")
def home():
    return "Backend Flask fonctionne !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
