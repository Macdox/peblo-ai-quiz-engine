from fastapi import FastAPI
from app.routes import ingest, quiz, answer

app = FastAPI(title="Peblo Quiz Engine")

app.include_router(ingest.router)
app.include_router(quiz.router)
app.include_router(answer.router)
