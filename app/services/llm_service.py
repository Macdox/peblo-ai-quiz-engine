import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("LLM_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")

def generate_questions_from_text(text):

    prompt = f"""
Generate 3 quiz questions from the following educational text.

Types required:
1 MCQ
1 True/False
1 Fill in the blank

Return ONLY valid JSON like this:

[
 {{
  "question": "...",
  "type": "MCQ",
  "options": ["A","B","C","D"],
  "answer": "...",
  "difficulty": "easy"
 }},
 {{
  "question": "...",
  "type": "TrueFalse",
  "options": ["True","False"],
  "answer": "...",
  "difficulty": "easy"
 }},
 {{
  "question": "...",
  "type": "FillBlank",
  "options": [],
  "answer": "...",
  "difficulty": "easy"
 }}
]

Text:
{text}
"""

    response = model.generate_content(prompt)

    return json.loads(response.text)
