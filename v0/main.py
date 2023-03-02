from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt

from v0.config import settings
from v0.routers import users, questions
from v0.schemas import UserAuthentication, TokenData
from v0.utilities import get_current_active_user, oauth2_scheme, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, get_user
from v0.security import create_access_token, authenticate_user


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


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
    # user = fake_decode_token(token)
    # return user

# authorization primitive prototype


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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