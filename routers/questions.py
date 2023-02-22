from schemas import QuestionModel
from database import question_collection

from fastapi import Body, HTTPException, status, APIRouter, Response
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder


question_router = APIRouter()


@question_router.get("/", response_description="Get all the questions", response_model=QuestionModel)
async def get_questions_list():
    questions = await question_collection.find().to_list(1000)
    if not questions:
        return Response(status_code=status.HTTP_404_NOT_FOUND, detail="Oops! No questions found!")
    return JSONResponse(status_code=status.HTTP_200_OK, content=questions)


@question_router.post("/add", response_description="Add new question", response_model=QuestionModel)
async def add_question(question: QuestionModel = Body(...)):
    question = jsonable_encoder(question)
    new_question = await question_collection.insert_one(question)
    created_question = await question_collection.find_one({"_id": new_question.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_question)


@question_router.delete("/delete/{id}")
async def delete_question(id: str):
    delete_result = await question_collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question {id} not found")