from app.database.mongo import db


async def is_duplicate_question(question_text: str):

    existing = await db.questions.find_one({
        "question": {"$regex": f"^{question_text}$", "$options": "i"}
    })

    return existing is not None


def validate_question(q):

    # question text must exist
    if not q.get("question"):
        return False

    # answer must exist
    if not q.get("answer"):
        return False

    # MCQ validation
    if q.get("type") == "MCQ":

        options = q.get("options", [])

        if len(options) < 2:
            return False

        if q["answer"] not in options:
            return False

    return True

def evaluate_question_quality(q):

    score = 0

    if len(q["question"]) > 10:
        score += 1

    if q.get("type") == "MCQ" and len(q.get("options", [])) >= 3:
        score += 1

    if q.get("answer"):
        score += 1

    return score