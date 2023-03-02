from datetime import timedelta

from v1.schemas.schema import TokenModel, TokenDataModel, RegistrationReqModel, RegistrationResModel, UserAuthModel, UserDBModel
from v1.database import user_collection
from v1.utils import authenticate_user, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Body, Form, HTTPException, status, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()


@auth_router.get("/register", response_description="Get Register EP", response_model=RegistrationReqModel)
async def get_register():
    payload = {"text": "Hello", "icon": "iconcode"}
    return JSONResponse(content=payload, status_code=status.HTTP_200_OK)


@auth_router.post("/register", response_description="Register new user account", response_model=RegistrationResModel)
async def post_register(user: RegistrationReqModel = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = get_password_hash(user["password"])
    requested_user = await user_collection.insert_one(user)
    registered_user = await user_collection.find_one({"_id": requested_user.inserted_id})
    return JSONResponse(content=registered_user, status_code=status.HTTP_201_CREATED)


@auth_router.post("/login", response_description="Get login form", response_model=TokenDataModel)
async def post_login(auth_form: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(auth_form.username, auth_form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = user["username"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}