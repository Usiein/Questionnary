from datetime import datetime
#from fastapi import Depends, HTTPException, status, APIRouter, Response
#from pymongo.collection import ReturnDocument
from schemas import UserModel, UpdateUserModel
from database import user_collection
from typing import List

#from serializers.postSerializers import postEntity, postListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from fastapi import Body, HTTPException, status, APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import db_connection_check


user_router = APIRouter()


@user_router.post("/", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@user_router.get("/", response_description="List all users", response_model=UserModel)
async def list_users():
    users = await user_collection.find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@user_router.get(
    "/{id}", response_description="Get a single user", response_model=UserModel
)
async def show_user(id: str):
    if (user := await user_collection.find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")


@user_router.put("/{id}", response_description="Update a user", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await user_collection.update_one({"_id": id}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await user_collection.find_one({"_id": id})
            ) is not None:
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_user)

    if (existing_user := await user_collection.find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=existing_user)

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@user_router.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    delete_result = await user_collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")
