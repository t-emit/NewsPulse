# database/mongo.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


# -----------------------------
# MongoDB Singleton Connection
# -----------------------------
class MongoDB:

    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)

        return cls._instance


    def __init__(self):

        if not hasattr(self, "client"):

            try:

                self.client = MongoClient(MONGO_URI)

                # Test connection
                self.client.admin.command("ping")

                print("✅ MongoDB Atlas connected successfully")

            except Exception as e:

                print("❌ MongoDB connection failed:", e)

                self.client = None


    def get_db(self, db_name="NewsPulseDB"):

        if self.client is not None:
            return self.client[db_name]

        return None


# -----------------------------
# Create Singleton Instance
# -----------------------------
db_connection = MongoDB()


# -----------------------------
# Export Database
# -----------------------------
db = db_connection.get_db()


# -----------------------------
# Collections
# -----------------------------
users_collection = db["users"] if db is not None else None
bookmarks_collection = db["bookmarks"] if db is not None else None
activity_logs_collection = db["activity_logs"] if db is not None else None