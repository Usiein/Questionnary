from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import users, questions
from database import db
from schemas import UserAuthentication, UserInDB
from utilities import get_current_active_user, oauth2_scheme, fake_users_db, fake_hash_password


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


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/")
async def get_authorized(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# example of typical bearer token approach to get current authenticated user
@app.get("/me")
async def get_authed_user(current_user: UserAuthentication = Depends(get_current_active_user)):
    return current_user


@app.get("/api/healthchecker")
def root():

    return {"message": "Welcome to FastAPI with MongoDB", "result": ""}