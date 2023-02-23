from schemas import UserAuthentication, UserInDB
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# fake database collection
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
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
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
    # user = fake_decode_token(token)
    # return user


async def get_current_active_user(current_user: UserAuthentication = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user