import pymongo.errors
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from v0.config import settings


client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client["tb_app"]
user_collection = db["Users"]  # Collection to store user initial data
user_answer_history = db["User_answers"]  # Collection to store answer history
question_collection = db["Questions"]  # Collection to store questions
