import pymongo.errors
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from v0.config import settings


client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client["fastapi"]
user_collection = db["Users"]  # Collection to store user initial data
question_collection = db["Questions"]  # Collection to store questions


async def db_connection_check():

    try:
        await db.list_database_names()
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Cannot connect to MongoDB server")
        sys.exit(1)

db_connection_check()


