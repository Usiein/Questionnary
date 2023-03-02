from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union


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


# model of authentication response body
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# Class used to resolve user authentication
class UserAuthentication(BaseModel):
    username: str
    email: Union[EmailStr, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

    class Config:
        json_encoders = {ObjectId: str}


# Class used for
class UserInDB(UserAuthentication):
    hashed_password: str


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    avatar: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.mail",
                "avatar": "someavatarstring"
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    avatar: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.mail",
                "avatar": "someavatarstring"
            }
        }


class QuestionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    categories: Optional[str] = Field(...)
    text: str = Field(...)
    addedDate: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Question #999",
                "categories": "AbstractThinking, Logic",
                "text": "Do we have infinite number of infinities?",
                "addedDate": "10.10.2010"
            }
        }
