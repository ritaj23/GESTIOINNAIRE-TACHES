from pymongo import MongoClient

# إذا تحبي تستعملي متغيرات بيئية:
import os
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "admin123")
MONGO_DB   = os.getenv("MONGO_DB", "taskmanager")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]

# Collections
tasks_collection = db["tasks"]
users_collection = db["users"]  # <---- هنا ضيفيه
