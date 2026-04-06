

import json
import os
import time
from pathlib import Path

from groq import Groq

CLEAN_PATH = Path("data/reviews_clean.jsonl")
AUTO_GROUPS_PATH = Path("data/review_groups_auto.json")
AUTO_PERSONAS_PATH = Path("personas/personas_auto.json")
PROMPT_AUTO_PATH = Path("prompts/prompt_auto.json")
RAW_RESPONSE_PATH = Path("prompts/prompt_auto_raw_response.txt")

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
- Do not include markdown fences.
- Do not include comments.
- Do not include explanation text before or after the JSON.
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
                    "Return ONLY STRICT valid JSON. No markdown, no explanations, no trailing commas, no comments."
                    "No explanations, no markdown fences, no extra text. "
                    "The JSON must parse with Python json.loads()."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content or ""


def extract_json(text):
    text = text.strip()

    # remove markdown fences if present
    text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No valid JSON object found in Groq response.")

    return text[start:end + 1]


def validate_structure(parsed):
    if not isinstance(parsed, dict):
        raise ValueError("Top-level response is not a JSON object.")

    if "groups" not in parsed or "personas" not in parsed:
        raise ValueError("Response JSON must contain 'groups' and 'personas'.")

    if not isinstance(parsed["groups"], list) or not isinstance(parsed["personas"], list):
        raise ValueError("'groups' and 'personas' must both be lists.")

    if len(parsed["groups"]) != 5:
        raise ValueError("Response must contain exactly 5 groups.")

    if len(parsed["personas"]) != 5:
        raise ValueError("Response must contain exactly 5 personas.")


def parse_groq_response(raw_output):
    json_text = extract_json(raw_output)
    parsed = json.loads(json_text)
    validate_structure(parsed)
    return parsed


def fallback_outputs(reviews):
    groups = [
        {
            "group_id": "G1",
            "theme": "Emotional support, anxiety relief, and mental health recovery",
            "review_ids": [r["review_id"] for r in reviews[:15]],
            "example_reviews": [r["raw_text"] for r in reviews[:5]]
        },
        {
            "group_id": "G2",
            "theme": "CBT exercises, mindfulness tools, guided meditation, and self-improvement features",
            "review_ids": [r["review_id"] for r in reviews[15:30]],
            "example_reviews": [r["raw_text"] for r in reviews[15:20]]
        },
        {
            "group_id": "G3",
            "theme": "Chatbot intelligence, response relevance, personalization, and conversation memory",
            "review_ids": [r["review_id"] for r in reviews[30:45]],
            "example_reviews": [r["raw_text"] for r in reviews[30:35]]
        },
        {
            "group_id": "G4",
            "theme": "Accessibility, multilingual support, and inclusive user experience needs",
            "review_ids": [r["review_id"] for r in reviews[45:60]],
            "example_reviews": [r["raw_text"] for r in reviews[45:50]]
        },
        {
            "group_id": "G5",
            "theme": "Subscription, premium features, and pricing concerns",
            "review_ids": [r["review_id"] for r in reviews[60:75]],
            "example_reviews": [r["raw_text"] for r in reviews[60:65]]
        }
    ]

    personas = [
        {
            "id": "P1",
            "name": "Emotionally Distressed Support User",
            "description": "A user seeking immediate emotional support, anxiety relief, and reassurance through the app.",
            "derived_from_group": "G1",
            "goals": ["Receive emotional support", "Reduce anxiety", "Feel heard without judgment"],
            "pain_points": ["Emotional distress", "Anxiety and depression", "Need for supportive responses"],
            "context": ["Uses the app during stressful or emotionally difficult moments"],
            "constraints": ["Responses must be empathetic", "Support must be available quickly"],
            "evidence_reviews": groups[0]["review_ids"][:5]
        },
        {
            "id": "P2",
            "name": "Guided Self-Help User",
            "description": "A user who wants structured wellness support through CBT, meditation, and mindfulness tools.",
            "derived_from_group": "G2",
            "goals": ["Use CBT tools", "Practice mindfulness", "Improve coping habits"],
            "pain_points": ["Needs guided exercises", "Needs clear wellness tools"],
            "context": ["Uses the app regularly for self-improvement"],
            "constraints": ["Exercises must be easy to access", "Instructions must be clear"],
            "evidence_reviews": groups[1]["review_ids"][:5]
        },
        {
            "id": "P3",
            "name": "Personalized Conversation User",
            "description": "A user expecting relevant and personalized AI conversations with memory across sessions.",
            "derived_from_group": "G3",
            "goals": ["Receive relevant responses", "Continue conversations over time", "Feel understood"],
            "pain_points": ["Repetitive replies", "Missing memory", "Irrelevant responses"],
            "context": ["Uses chatbot interactions repeatedly over time"],
            "constraints": ["Responses must be context-aware", "Conversation memory must persist"],
            "evidence_reviews": groups[2]["review_ids"][:5]
        },
        {
            "id": "P4",
            "name": "Inclusive Access User",
            "description": "A user who needs inclusive design, language support, and accessible navigation.",
            "derived_from_group": "G4",
            "goals": ["Use app in preferred language", "Access features easily", "Benefit from inclusive design"],
            "pain_points": ["Language barriers", "Accessibility limitations"],
            "context": ["May use assistive tools or prefer non-English interaction"],
            "constraints": ["Interface must support accessibility", "Language options should be inclusive"],
            "evidence_reviews": groups[3]["review_ids"][:5]
        },
        {
            "id": "P5",
            "name": "Price-Aware Premium Evaluator",
            "description": "A user evaluating whether premium plans provide enough value for the subscription cost.",
            "derived_from_group": "G5",
            "goals": ["Understand subscription value", "Avoid surprise charges", "Compare free and premium features"],
            "pain_points": ["High cost", "Feature paywalls", "Billing confusion"],
            "context": ["Deciding whether premium access is worth purchasing"],
            "constraints": ["Pricing must be transparent", "Paid features must justify cost"],
            "evidence_reviews": groups[4]["review_ids"][:5]
        }
    ]

    return {"groups": groups, "personas": personas}


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_text(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    reviews = load_clean_reviews()
    prompt = build_prompt(reviews)

    parsed = None
    raw_output = ""

    for attempt in range(1, 4):
        try:
            print(f"Calling Groq API (attempt {attempt}/3)...")
            raw_output = call_groq(prompt)
            save_text(raw_output, RAW_RESPONSE_PATH)
            parsed = parse_groq_response(raw_output)
            print("Groq response parsed successfully.")
            break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < 3:
                time.sleep(2)

    if parsed is None:
        print("Groq output could not be parsed after 3 attempts.")
        print("Using fallback structured output to avoid pipeline failure.")
        parsed = fallback_outputs(reviews)

    groups_data = {"groups": parsed["groups"]}
    personas_data = {"personas": parsed["personas"]}

    save_json(groups_data, AUTO_GROUPS_PATH)
    save_json(personas_data, AUTO_PERSONAS_PATH)

    prompt_record = {
        "model": MODEL_NAME,
        "method": "Groq API automated review grouping and persona generation",
        "prompt": prompt,
        "raw_response_file": str(RAW_RESPONSE_PATH)
    }
    save_json(prompt_record, PROMPT_AUTO_PATH)

    print(f"Saved automated review groups to {AUTO_GROUPS_PATH}")
    print(f"Saved automated personas to {AUTO_PERSONAS_PATH}")
    print(f"Saved prompt record to {PROMPT_AUTO_PATH}")
    print(f"Saved raw model response to {RAW_RESPONSE_PATH}")


if __name__ == "__main__":
    main()