import google.generativeai as genai
import os
import json
import time

genai.configure(api_key=os.getenv("LLM_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_questions_from_text(text, retries=3):

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

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                wait = 10 * (attempt + 1)  # 10s, 20s, 30s
                print(f"Rate limit hit. Waiting {wait}s before retry {attempt + 1}/{retries}...")
                time.sleep(wait)
            else:
                raise e

    print("Max retries reached. Skipping this chunk.")
    return []
