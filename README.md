# Peblo AI Backend Engineer Challenge

## Mini Content Ingestion + Adaptive Quiz Engine

## Overview

This project implements a prototype **AI-powered learning backend system** that ingests educational PDF content and automatically converts it into interactive quiz questions.

The system extracts text from uploaded educational PDFs, processes the content into structured chunks, generates quiz questions using a Large Language Model (LLM), and serves quizzes through API endpoints. The system also includes **adaptive difficulty logic**, which adjusts quiz difficulty based on student performance.

This project demonstrates:

* AI-driven backend pipeline design
* Educational content ingestion
* LLM integration for question generation
* API-based quiz delivery
* Adaptive learning logic

---

# System Architecture

The system follows a modular AI content processing pipeline.

```
PDF Upload
   ↓
Text Extraction
   ↓
Content Cleaning
   ↓
Chunk Generation
   ↓
MongoDB Storage
   ↓
LLM Question Generation
   ↓
Quiz Retrieval API
   ↓
Student Answer Submission
   ↓
Adaptive Difficulty Engine
```

---

# Tech Stack

### Backend Framework

FastAPI

### Programming Language

Python

### Database

MongoDB

### PDF Processing

PyMuPDF

### AI Model

Google Gemini API

### Environment Management

python-dotenv

---

# Key Features

### Content Ingestion

* Accepts educational PDF files
* Extracts raw text from documents
* Cleans and processes extracted content
* Splits content into manageable chunks for AI processing

### Structured Data Storage

The system stores structured data in MongoDB collections:

* sources
* chunks
* questions
* student_answers

### AI Quiz Generation

Uses an LLM to generate quiz questions from educational text chunks.

Supported question types:

* Multiple Choice Questions (MCQ)
* True / False
* Fill in the blank

All generated questions maintain **traceability to the source content chunk**.

### Quiz Retrieval API

Provides quiz questions via REST API based on difficulty level.

### Student Answer Submission

Students can submit answers through the API.

### Adaptive Difficulty Logic

Difficulty level adjusts based on student performance.

Rules implemented:

* Correct answer → Increase difficulty
* Incorrect answer → Decrease difficulty

Difficulty levels:

```
easy → medium → hard
```

---

# Project Structure

```
peblo-ai-quiz-engine
│
├── app
│   ├── main.py
│
│   ├── database
│   │   └── mongo.py
│
│   ├── routes
│   │   ├── ingest.py
│   │   ├── quiz.py
│   │   └── answer.py
│
│   ├── services
│   │   ├── pdf_service.py
│   │   ├── chunk_service.py
│   │   ├── llm_service.py
│   │   └── adaptive_service.py
│
│   └── utils
│
├── uploads
├── sample_outputs
├── requirements.txt
├── .env.example
└── README.md
```

---

# Database Schema

## Sources Collection

```
{
 "_id": "SRC_001",
 "filename": "grade1_math_numbers.pdf",
 "subject": "Math",
 "grade": 1,
 "uploaded_at": "2026-03-15"
}
```

---

## Chunks Collection

```
{
 "_id": "CHUNK_001",
 "source_id": "SRC_001",
 "topic": "Shapes",
 "text": "A triangle has three sides and three corners..."
}
```

---

## Questions Collection

```
{
 "_id": "Q001",
 "chunk_id": "CHUNK_001",
 "question": "How many sides does a triangle have?",
 "type": "MCQ",
 "options": ["2","3","4","5"],
 "answer": "3",
 "difficulty": "easy"
}
```

---

## Student Answers Collection

```
{
 "student_name": "John",
 "question_id": "Q001",
 "selected_answer": "3",
 "is_correct": true
}
```

---

# API Endpoints

## 1. Ingest PDF

### Endpoint

```
POST /ingest
```

### Description

Uploads a PDF file and extracts structured content chunks.

### Response Example

```
{
 "message": "PDF ingested successfully",
 "source_id": "e8b7c2",
 "chunks_created": 25
}
```

---

## 2. Generate Quiz Questions

### Endpoint

```
POST /generate-quiz
```

### Description

Generates quiz questions from stored content chunks using the LLM.

### Response Example

```
{
 "message": "Quiz generated",
 "questions_created": 15
}
```

---

## 3. Retrieve Quiz Questions

### Endpoint

```
GET /quiz?difficulty=easy
```

### Description

Returns quiz questions filtered by difficulty.

### Response Example

```
{
 "difficulty": "easy",
 "questions": [
  {
   "_id": "665fa7c...",
   "question": "How many sides does a triangle have?",
   "type": "MCQ",
   "options": ["2","3","4","5"]
  }
 ]
}
```

---

## 4. Submit Student Answer

### Endpoint

```
POST /submit-answer
```

### Example Input

```
{
 "student_name": "Alice",
 "question_id": "665fa7c...",
 "selected_answer": "3",
 "current_difficulty": "easy"
}
```

### Example Response

```
{
 "correct": true,
 "next_difficulty": "medium"
}
```

---

# Adaptive Difficulty Logic

The system adjusts quiz difficulty dynamically based on student performance.

Algorithm:

```
if correct:
    difficulty = increase
else:
    difficulty = decrease
```

Difficulty progression:

```
easy → medium → hard
```

---

# Setup & Usage

## 1. Install Dependencies

First clone the repository:

```
git clone https://github.com/yourusername/peblo-ai-quiz-engine.git
cd peblo-ai-quiz-engine
```

Create a Python virtual environment:

```
python -m venv venv
```

Activate the environment:

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

Install required dependencies:

```
pip install -r requirements.txt
```

---

# 2. Configure Environment Variables

Create a `.env` file in the project root.

Example configuration:

```
DATABASE_URL=mongodb://localhost:27017
LLM_API_KEY=your_gemini_api_key
```

Environment variables:

DATABASE_URL
MongoDB connection string used by the application.

LLM_API_KEY
API key used for accessing the LLM service (Google Gemini).

**Important:**
Do not commit your `.env` file to the repository.

---

# 3. Run the Backend Server

Start the FastAPI server:

```
uvicorn app.main:app --reload
```

The backend server will start at:

```
http://localhost:8000
```

Interactive API documentation is automatically generated by FastAPI.

Open:

```
http://localhost:8000/docs
```

---

# 4. Testing API Endpoints

You can test all endpoints using **FastAPI Swagger UI**, **Postman**, or **curl**.

Recommended approach: Swagger UI.

Open:

```
http://localhost:8000/docs
```

---

## Step 1: Upload a PDF

Endpoint:

```
POST /ingest
```

Upload an educational PDF file.
The system will extract text and create structured content chunks.

Example response:

```
{
 "message": "PDF ingested successfully",
 "source_id": "SRC_001",
 "chunks_created": 24
}
```

---

## Step 2: Generate Quiz Questions

Endpoint:

```
POST /generate-quiz
```

Provide the `source_id` returned from the ingestion step.

The system will use the LLM to generate quiz questions from stored content chunks.

Example response:

```
{
 "message": "Quiz generated",
 "questions_created": 15
}
```

---

## Step 3: Retrieve Quiz Questions

Endpoint:

```
GET /quiz?difficulty=easy
```

Returns quiz questions filtered by difficulty level.

Example response:

```
{
 "difficulty": "easy",
 "questions": [
  {
   "_id": "665fa7c...",
   "question": "How many sides does a triangle have?",
   "type": "MCQ",
   "options": ["2","3","4","5"]
  }
 ]
}
```

---

## Step 4: Submit Student Answer

Endpoint:

```
POST /submit-answer
```

Example input:

```
{
 "student_name": "Alice",
 "question_id": "665fa7c...",
 "selected_answer": "3",
 "current_difficulty": "easy"
}
```

Example response:

```
{
 "correct": true,
 "next_difficulty": "medium"
}
```

The system evaluates the answer and updates the quiz difficulty based on performance.

---

# Local Testing Workflow

Typical workflow for testing the system:

1. Upload a PDF using `/ingest`
2. Generate quiz questions using `/generate-quiz`
3. Retrieve questions using `/quiz`
4. Submit answers using `/submit-answer`
5. Observe adaptive difficulty updates

---

# Notes

This project focuses on backend system design and AI pipeline integration.
The user interface is intentionally minimal since the challenge focuses on backend architecture and API design.


# Sample Outputs

Example generated quiz question:

```
{
 "question": "How many sides does a triangle have?",
 "type": "MCQ",
 "options": ["2","3","4","5"],
 "answer": "3",
 "difficulty": "easy"
}
```

Example extracted content chunk:

```
{
 "source_id": "SRC_001",
 "text": "A triangle has three sides and three corners."
}
```

# Future Improvements

Possible enhancements for production systems:

* Duplicate question detection using embeddings
* Semantic search using vector databases
* Question quality evaluation
* Caching generated quizzes
* Topic-based quiz retrieval
* Multi-user student profiles
* Frontend learning dashboard

---

# Conclusion

This project demonstrates a complete prototype pipeline for converting educational content into interactive quizzes using AI. It highlights backend system design, data modeling, LLM integration, and adaptive learning capabilities.

The architecture is modular and extensible, allowing future improvements such as semantic retrieval, learning analytics, and personalized education workflows.
