from fastapi import APIRouter, UploadFile, File
import shutil
import uuid

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.database.mongo import db

router = APIRouter()

UPLOAD_DIR = "uploads/"

@router.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):

    source_id = str(uuid.uuid4())

    file_path = f"{UPLOAD_DIR}{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Chunk text
    chunks = chunk_text(text)

    chunk_docs = []

    for chunk in chunks:

        chunk_doc = {
            "source_id": source_id,
            "text": chunk
        }

        chunk_docs.append(chunk_doc)

    # Store chunks
    if chunk_docs:
        await db.chunks.insert_many(chunk_docs)

    return {
        "message": "PDF ingested successfully",
        "source_id": source_id,
        "chunks_created": len(chunk_docs)
    }
