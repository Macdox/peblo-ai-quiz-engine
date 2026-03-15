from fastapi import APIRouter
from app.database.mongo import db
from app.services.llm_service import generate_questions_from_text
from app.utils.question_filter import (
    is_duplicate_question,
    validate_question,
    evaluate_question_quality
)

router = APIRouter()

# Simple in-memory cache
quiz_cache = {}


@router.post("/generate-quiz")
async def generate_quiz(source_id: str):

    chunks = await db.chunks.find(
        {"source_id": source_id}
    ).to_list(length=5)

    generated = 0
    duplicates_skipped = 0
    invalid_skipped = 0

    for chunk in chunks:

        questions = generate_questions_from_text(chunk["text"])

        for q in questions:

            # Validate question structure
            if not validate_question(q):
                invalid_skipped += 1
                continue

            # Check duplicate questions
            if await is_duplicate_question(q["question"]):
                duplicates_skipped += 1
                continue

            quality_score = evaluate_question_quality(q)

            question_doc = {
                "chunk_id": str(chunk["_id"]),
                "source_id": source_id,
                "question": q["question"],
                "type": q["type"],
                "options": q.get("options", []),
                "answer": q["answer"],
                "difficulty": q.get("difficulty", "easy"),
                "quality_score": quality_score
            }

            if not validate_question(q):
                continue

            quality_score = evaluate_question_quality(q)

            question_doc = {
                "chunk_id": str(chunk["_id"]),
                "source_id": source_id,
                "question": q["question"],
                "type": q["type"],
                "options": q.get("options", []),
                "answer": q["answer"],
                "difficulty": q.get("difficulty", "easy"),
                "quality_score": quality_score
            }

            await db.questions.insert_one(question_doc)

            generated += 1

    # clear cache after new questions
    quiz_cache.clear()

    return {
        "message": "Quiz generated",
        "questions_created": generated,
        "duplicates_skipped": duplicates_skipped,
        "invalid_skipped": invalid_skipped
    }


@router.get("/quiz")
async def get_quiz(difficulty: str = "easy", limit: int = 5):

    # Check cache first
    cache_key = f"{difficulty}_{limit}"

    if cache_key in quiz_cache:
        return {
            "difficulty": difficulty,
            "questions": quiz_cache[cache_key],
            "cached": True
        }

    questions = await db.questions.find(
        {"difficulty": difficulty}
    ).limit(limit).to_list(length=limit)

    for q in questions:
        q["_id"] = str(q["_id"])

    # Store in cache
    quiz_cache[cache_key] = questions

    return {
        "difficulty": difficulty,
        "questions": questions,
        "cached": False
    }