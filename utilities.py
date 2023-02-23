from schemas import UserAuthentication, UserInDB
from fastapi import Depends
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
    return UserAuthentication(
        username=token + "fakedecoded",
        email="uosmanov@test.io",
        full_name="Usiein Lienurovich Osmanov"
    )


# utility function
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user