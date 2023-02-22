from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import users, questions
from database import db


app = FastAPI()


origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.user_router, tags=['Users'], prefix='/api/users')
app.include_router(questions.question_router, tags=['Questions'], prefix='/api/questions')


@app.get("/api/healthchecker")
def root():

    return {"message": "Welcome to FastAPI with MongoDB", "result": ""}