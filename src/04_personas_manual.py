


def get_persona_template():
    return {
        "personas": [
            {
                "id": "P1",
                "name": "Example Persona",
                "description": "Example user persona derived from manual review groups.",
                "derived_from_group": "G1",
                "goals": [],
                "pain_points": [],
                "context": [],
                "constraints": [],
                "evidence_reviews": []
            }
        ]
    }


def main():
    template = get_persona_template()
    print("Manual persona template loaded successfully.")
    print(template)


if __name__ == "__main__":
    main()