from pymongo import MongoClient
from config import CONFIG


client = MongoClient(CONFIG.mongo_connection.get_secret_value())

def get_db():
    yield client