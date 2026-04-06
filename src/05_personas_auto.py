"""
05_personas_auto.py

Automated review grouping and persona generation using Groq API
with meta-llama/llama-4-scout-17b-16e-instruct.

Outputs:
- data/review_groups_auto.json
- personas/personas_auto.json
- prompts/prompt_auto.json
"""

import json
import os
from pathlib import Path

from groq import Groq

CLEAN_PATH = Path("data/reviews_clean.jsonl")
AUTO_GROUPS_PATH = Path("data/review_groups_auto.json")
AUTO_PERSONAS_PATH = Path("personas/personas_auto.json")
PROMPT_AUTO_PATH = Path("prompts/prompt_auto.json")

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"


def load_clean_reviews(limit=120):
    reviews = []
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            obj = json.loads(line)
            reviews.append({
                "review_id": obj["review_id"],
                "raw_text": obj["raw_text"],
                "cleaned_text": obj["cleaned_text"]
            })
    return reviews


def build_prompt(reviews):
    return f"""
You are helping with a software requirements engineering project.

Task:
1. Read the following cleaned app reviews for the Wysa mental health app.
2. Automatically group them into exactly 5 meaningful review groups.
3. Each group must have:
   - group_id: G1 to G5
   - theme
   - review_ids
   - example_reviews
4. Then generate exactly 5 personas, one persona per group.
5. Each persona must include:
   - id: P1 to P5
   - name
   - description
   - derived_from_group
   - goals
   - pain_points
   - context
   - constraints
   - evidence_reviews

Important:
- Use only evidence supported by the reviews.
- Keep the personas grounded and realistic.
- Return STRICT JSON only.
- Use this exact top-level structure:
{{
  "groups": [...],
  "personas": [...]
}}

Reviews:
{json.dumps(reviews, ensure_ascii=False, indent=2)}
""".strip()


def call_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Return ONLY valid JSON. "
                    "No explanations, no markdown fences, no extra text."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


def extract_json(text):
    text = text.strip()

    # remove markdown fences
    text = text.replace("```json", "").replace("```", "").strip()

    # find first opening brace
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No valid JSON object found in Groq response.")

    return text[start:end + 1]


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    reviews = load_clean_reviews()
    prompt = build_prompt(reviews)

    raw_output = call_groq(prompt)
    json_text = extract_json(raw_output)
    parsed = json.loads(json_text)

    groups_data = {"groups": parsed["groups"]}
    personas_data = {"personas": parsed["personas"]}

    save_json(groups_data, AUTO_GROUPS_PATH)
    save_json(personas_data, AUTO_PERSONAS_PATH)

    prompt_record = {
        "model": MODEL_NAME,
        "method": "Groq API automated review grouping and persona generation",
        "prompt": prompt
    }
    save_json(prompt_record, PROMPT_AUTO_PATH)

    print(f"Saved automated review groups to {AUTO_GROUPS_PATH}")
    print(f"Saved automated personas to {AUTO_PERSONAS_PATH}")
    print(f"Saved prompt record to {PROMPT_AUTO_PATH}")


if __name__ == "__main__":
    main()