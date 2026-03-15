from fastapi import APIRouter
from app.database.mongo import db
from app.services.llm_service import generate_questions_from_text

router = APIRouter()

@router.post("/generate-quiz")
async def generate_quiz(source_id: str):

    chunks = await db.chunks.find(
        {"source_id": source_id}
    ).to_list(length=5)

    generated = 0

    for chunk in chunks:

        questions = generate_questions_from_text(chunk["text"])

        for q in questions:

            question_doc = {
                "chunk_id": str(chunk["_id"]),
                "source_id": source_id,
                "question": q["question"],
                "type": q["type"],
                "options": q["options"],
                "answer": q["answer"],
                "difficulty": q["difficulty"]
            }

            await db.questions.insert_one(question_doc)

            generated += 1

    return {
        "message": "Quiz generated",
        "questions_created": generated
    }

@router.get("/quiz")
async def get_quiz(difficulty: str = "easy", limit: int = 5):

    questions = await db.questions.find(
        {"difficulty": difficulty}
    ).limit(limit).to_list(length=limit)

    for q in questions:
        q["_id"] = str(q["_id"])

    return {
        "difficulty": difficulty,
        "questions": questions
    }