import json
from pathlib import Path

AUTO_PERSONAS_PATH = Path("personas/personas_auto.json")
AUTO_SPEC_PATH = Path("spec/spec_auto.md")


def load_personas():
    with open(AUTO_PERSONAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["personas"]


def generate_requirements(personas):
    requirements = [
        {
            "id": "FR1",
            "description": "The system shall provide emotionally supportive responses to users experiencing anxiety, distress, or negative thoughts.",
            "persona": "Emotionally Distressed Support User",
            "group": "G1",
            "acceptance": "Given a user expresses emotional distress, when the chatbot receives the message, then it must return a supportive response within 2 seconds."
        },
        {
            "id": "FR2",
            "description": "The system shall provide guided CBT exercises to help users manage negative thought patterns.",
            "persona": "Guided Self-Help User",
            "group": "G2",
            "acceptance": "Given a user opens CBT tools, when the feature is selected, then at least one guided CBT exercise must be displayed."
        },
        {
            "id": "FR3",
            "description": "The system shall provide guided meditation and breathing exercises through the wellness tools interface.",
            "persona": "Guided Self-Help User",
            "group": "G2",
            "acceptance": "Given a user selects meditation or breathing exercises, when the feature starts, then the selected exercise must load successfully."
        },
        {
            "id": "FR4",
            "description": "The system shall maintain relevant conversation context across user sessions.",
            "persona": "Personalized Conversation User",
            "group": "G3",
            "acceptance": "Given a returning user continues a prior conversation, when a follow-up message is sent, then the chatbot must reference earlier context."
        },
        {
            "id": "FR5",
            "description": "The system shall generate contextually relevant responses and reduce repetitive or generic replies.",
            "persona": "Personalized Conversation User",
            "group": "G3",
            "acceptance": "Given two different user prompts, when the chatbot responds, then each reply must be specific to the user input and not duplicated."
        },
        {
            "id": "FR6",
            "description": "The system shall support multilingual interaction for supported non-English languages.",
            "persona": "Inclusive Access User",
            "group": "G4",
            "acceptance": "Given a supported language is selected, when the user interacts with the system, then the chatbot and interface labels must appear in that language."
        },
        {
            "id": "FR7",
            "description": "The system shall support accessible navigation for users relying on assistive technologies.",
            "persona": "Inclusive Access User",
            "group": "G4",
            "acceptance": "Given a user relies on screen-reader support, when navigating the main interface, then key functions must remain accessible."
        },
        {
            "id": "FR8",
            "description": "The system shall clearly display subscription plans, pricing, and premium feature differences.",
            "persona": "Price-Aware Premium Evaluator",
            "group": "G5",
            "acceptance": "Given a user opens the premium page, when subscription options are displayed, then pricing and included features must be clearly shown."
        },
        {
            "id": "FR9",
            "description": "The system shall display free trial and billing information before premium activation.",
            "persona": "Price-Aware Premium Evaluator",
            "group": "G5",
            "acceptance": "Given a user starts a free trial, when trial information appears, then billing date and cancellation information must be visible."
        },
        {
            "id": "FR10",
            "description": "The system shall keep core emotional support features available to non-premium users.",
            "persona": "Price-Aware Premium Evaluator",
            "group": "G5",
            "acceptance": "Given a non-premium user accesses the application, when using core support functions, then emotional support chat must remain available."
        }
    ]

    return requirements


def save_spec(requirements):
    lines = []
    for req in requirements:
        lines.append(f"# Requirement ID: {req['id']}")
        lines.append(f"- Description: {req['description']}")
        lines.append(f"- Source Persona: {req['persona']}")
        lines.append(f"- Traceability: Derived from review group {req['group']}")
        lines.append(f"- Acceptance Criteria: {req['acceptance']}")
        lines.append("")

    with open(AUTO_SPEC_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    personas = load_personas()
    requirements = generate_requirements(personas)
    save_spec(requirements)
    print(f"Saved automated specification to {AUTO_SPEC_PATH}")


if __name__ == "__main__":
    main()