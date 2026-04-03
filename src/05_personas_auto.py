import json
from pathlib import Path
from collections import defaultdict

CLEAN_PATH = Path("data/reviews_clean.jsonl")
AUTO_GROUPS_PATH = Path("data/review_groups_auto.json")
AUTO_PERSONAS_PATH = Path("personas/personas_auto.json")
PROMPT_AUTO_PATH = Path("prompts/prompt_auto.json")


def load_clean_reviews():
    reviews = []
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        for line in f:
            reviews.append(json.loads(line))
    return reviews


def classify_review(cleaned_text: str):
    text = cleaned_text.lower()

    emotional_keywords = [
        "anxiety", "depression", "distress", "suicidal", "stress",
        "mental health", "support", "mindset", "recovery", "emotion", "lonely"
    ]
    cbt_keywords = [
        "cbt", "meditation", "breathing", "exercise", "mindfulness",
        "journal", "journaling", "tool", "therapy", "prompt", "relaxation"
    ]
    chatbot_keywords = [
        "response", "robotic", "memory", "remember", "conversation",
        "chatbot", "irrelevant", "repetitive", "scripted", "ai", "context"
    ]
    accessibility_keywords = [
        "language", "english", "indonesian", "accessible", "accessibility",
        "talkback", "visual", "navigate", "navigation", "inclusive"
    ]
    pricing_keywords = [
        "premium", "subscription", "trial", "price", "pricing",
        "pay", "payment", "paid", "cost", "charge", "billing"
    ]

    scores = {
        "G1": sum(1 for kw in emotional_keywords if kw in text),
        "G2": sum(1 for kw in cbt_keywords if kw in text),
        "G3": sum(1 for kw in chatbot_keywords if kw in text),
        "G4": sum(1 for kw in accessibility_keywords if kw in text),
        "G5": sum(1 for kw in pricing_keywords if kw in text),
    }

    best_group = max(scores, key=scores.get)

    if scores[best_group] == 0:
        return "G1"

    return best_group


def build_auto_groups(reviews):
    grouped = defaultdict(list)

    for review in reviews:
        gid = classify_review(review["cleaned_text"])
        grouped[gid].append(review)

    themes = {
        "G1": "Emotional support, anxiety relief, and mental health recovery",
        "G2": "CBT exercises, mindfulness tools, guided meditation, and self-improvement features",
        "G3": "Chatbot intelligence, response relevance, personalization, and conversation memory",
        "G4": "Accessibility, multilingual support, and inclusive user experience needs",
        "G5": "Subscription, premium features, and pricing concerns"
    }

    result = {"groups": []}

    for gid in ["G1", "G2", "G3", "G4", "G5"]:
        group_reviews = grouped.get(gid, [])[:15]
        result["groups"].append({
            "group_id": gid,
            "theme": themes[gid],
            "review_ids": [r["review_id"] for r in group_reviews],
            "example_reviews": [r["raw_text"] for r in group_reviews[:5]]
        })

    return result


def build_auto_personas():
    personas = {
        "personas": [
            {
                "id": "P1",
                "name": "Emotionally Distressed Support User",
                "description": "A user seeking immediate emotional support, anxiety relief, and mental health reassurance through the app.",
                "derived_from_group": "G1",
                "goals": [
                    "Get emotional support quickly",
                    "Reduce anxiety and negative thinking",
                    "Feel heard without judgment"
                ],
                "pain_points": [
                    "Emotional distress",
                    "Anxiety and depression",
                    "Need for safe and supportive responses"
                ],
                "context": [
                    "Uses the app during stressful or emotionally difficult moments"
                ],
                "constraints": [
                    "Responses must be empathetic",
                    "Support must be available quickly"
                ],
                "evidence_reviews": []
            },
            {
                "id": "P2",
                "name": "Guided Self-Help User",
                "description": "A user who wants structured wellness support through CBT, meditation, mindfulness, and guided exercises.",
                "derived_from_group": "G2",
                "goals": [
                    "Use CBT tools",
                    "Practice mindfulness",
                    "Build healthy coping habits"
                ],
                "pain_points": [
                    "Needs guided self-help structure",
                    "Needs clear exercises"
                ],
                "context": [
                    "Uses the app regularly for personal improvement"
                ],
                "constraints": [
                    "Exercises must be easy to access",
                    "Instructions must be clear"
                ],
                "evidence_reviews": []
            },
            {
                "id": "P3",
                "name": "Personalized Conversation User",
                "description": "A user expecting smart, relevant, and personalized AI conversations that remember prior context.",
                "derived_from_group": "G3",
                "goals": [
                    "Get relevant responses",
                    "Continue conversations over time",
                    "Feel understood by the chatbot"
                ],
                "pain_points": [
                    "Repetitive replies",
                    "Missing conversation memory",
                    "Irrelevant responses"
                ],
                "context": [
                    "Uses the chatbot often for support and reflection"
                ],
                "constraints": [
                    "The system must retain context",
                    "Replies must feel personalized"
                ],
                "evidence_reviews": []
            },
            {
                "id": "P4",
                "name": "Inclusive Access User",
                "description": "A user who needs inclusive design, language support, and accessible app interaction.",
                "derived_from_group": "G4",
                "goals": [
                    "Use the app in a preferred language",
                    "Access features easily",
                    "Benefit from accessibility support"
                ],
                "pain_points": [
                    "Limited language support",
                    "Accessibility barriers"
                ],
                "context": [
                    "May use assistive tools or prefer non-English interaction"
                ],
                "constraints": [
                    "The interface must support accessibility",
                    "Language options should be inclusive"
                ],
                "evidence_reviews": []
            },
            {
                "id": "P5",
                "name": "Price-Aware Premium Evaluator",
                "description": "A user evaluating whether premium plans provide enough value for the subscription cost.",
                "derived_from_group": "G5",
                "goals": [
                    "Understand subscription value",
                    "Avoid surprise charges",
                    "Compare free and premium features"
                ],
                "pain_points": [
                    "High cost",
                    "Feature paywalls",
                    "Billing confusion"
                ],
                "context": [
                    "Deciding whether premium access is worth purchasing"
                ],
                "constraints": [
                    "Pricing must be transparent",
                    "Paid features must justify cost"
                ],
                "evidence_reviews": []
            }
        ]
    }

    return personas


def attach_evidence_reviews(personas, auto_groups):
    group_lookup = {g["group_id"]: g["review_ids"] for g in auto_groups["groups"]}
    for persona in personas["personas"]:
        gid = persona["derived_from_group"]
        persona["evidence_reviews"] = group_lookup.get(gid, [])[:10]
    return personas


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_prompt_record():
    prompt_record = {
        "method": "keyword-based automatic grouping and persona generation",
        "note": "This automated version uses rule-based keyword classification to approximate automated grouping before hybrid refinement."
    }
    save_json(prompt_record, PROMPT_AUTO_PATH)


def main():
    reviews = load_clean_reviews()
    auto_groups = build_auto_groups(reviews)
    auto_personas = build_auto_personas()
    auto_personas = attach_evidence_reviews(auto_personas, auto_groups)

    save_json(auto_groups, AUTO_GROUPS_PATH)
    save_json(auto_personas, AUTO_PERSONAS_PATH)
    save_prompt_record()

    print(f"Saved automated review groups to {AUTO_GROUPS_PATH}")
    print(f"Saved automated personas to {AUTO_PERSONAS_PATH}")
    print(f"Saved prompt record to {PROMPT_AUTO_PATH}")


if __name__ == "__main__":
    main()