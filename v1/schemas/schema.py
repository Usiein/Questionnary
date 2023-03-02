from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import Union


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TokenModel(BaseModel):
    access_token: str
    token_type: str

    class Config:
        arbitrary_types_allowed = True


class TokenDataModel(TokenModel):
    username: Union[str, None]


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: Union[str, None]
    email: Union[EmailStr, None]
    position: Union[str, None]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        example = {
            "username": "Kamaz Othodov",
            "email": "some@email.io",
            "position": "Third assistant to the Junior Nothing Manager"
        }


class RegistrationReqModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password: str
    username: Union[str, None]
    email: Union[EmailStr, None]
    position: Union[str, None]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        example = {
            "username": "Kamaz Othodov",
            "email": "some@email.io",
            "position": "Third assistant to the Junior Nothing Manager"
        }
    # hashed_secret: str


class RegistrationResModel(BaseModel):
    username: str
    position: str


class UserAuthModel(UserModel):
    password: str
    disabled: Union[bool, None] = None


class UserDBModel(BaseModel):
    username: str
    password: str

    class Config:
        json_encoders = {ObjectId: str}


class UserDBResponseModel(BaseModel):
    user: Union[UserDBModel, None]
    detail: Union[str, None]


class UserMutateModel(UserModel):
    username: str = None
    email: EmailStr = None
    position: str = None
    avatar: str = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        example = {
            "username": "Podjeg Saraiev",
            "email": "some@mail.io",
            "position": "some position",
            "avatar": "some link or somehow"
        }

