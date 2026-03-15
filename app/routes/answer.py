from fastapi import APIRouter
from bson import ObjectId
from app.database.mongo import db
from app.services.adaptive_service import adjust_difficulty

router = APIRouter()

@router.post("/submit-answer")
async def submit_answer(
    student_name: str,
    question_id: str,
    selected_answer: str,
    current_difficulty: str
):

    question = await db.questions.find_one(
        {"_id": ObjectId(question_id)}
    )

    if not question:
        return {"error": "Question not found"}

    correct = selected_answer == question["answer"]

    await db.student_answers.insert_one({
        "student_name": student_name,
        "question_id": question_id,
        "selected_answer": selected_answer,
        "is_correct": correct
    })

    next_difficulty = adjust_difficulty(current_difficulty, correct)

    return {
        "correct": correct,
        "next_difficulty": next_difficulty
    }
