from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import users, questions
from database import db
from schemas import UserAuthentication
from utilities import get_current_user, oauth2_scheme



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

# authorization primitive prototype


@app.get("/")
async def get_authorized(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# example of typical bearer token approach to get current authenticated user
@app.get("/me")
async def get_authed_user(current_user: UserAuthentication = Depends(get_current_user)):
    return current_user


@app.get("/api/healthchecker")
def root():

    return {"message": "Welcome to FastAPI with MongoDB", "result": ""}