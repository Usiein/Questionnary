from v0.schemas import UserAuthentication, UserInDB
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


# This is added to prevent circular import error
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "3bf74cd1b2a21fd6e94fc4a970b8405c9777c52e68dc6ed59ddad53d1c8c0d7f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# fake database collection
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$Rdwj77Ky7/sj.HWfqjR2SuQN1GgHJlLAfLPoUb/XCk37Y42wrZTGO",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$6DQZ2vXnlNYtXFOd6akuiucXQ9QwrsYi18WxSiU6TcB27nWcX2OLC",
        "disabled": True,
    },
}


# authentication primitive
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# fake password hashing
def fake_hash_password(password: str):
    return "fakehashed" + password


# Data for testing authentication (some kind of mock or utility)
def fake_decode_token(token):
    # not secure, for testing only
    user = get_user(fake_users_db, token)
    return user
    # return UserAuthentication(
    #     username=token + "fakedecoded",
    #     email="uosmanov@test.io",
    #     full_name="Usiein Lienurovich Osmanov"
    # )


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# utility function
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


async def get_current_active_user(current_user: UserAuthentication = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user