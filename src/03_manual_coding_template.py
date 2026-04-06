"""
03_manual_coding_template.py

This script provides a reusable template structure for manual coding
of review groups during the manual pipeline.

Purpose:
- organize review groups
- assign themes
- record example reviews
- support traceability into personas and requirements

This file serves as a template/reference for Task 3.
"""


def get_manual_group_template():
    return {
        "groups": [
            {
                "group_id": "G1",
                "theme": "Example theme",
                "review_ids": [],
                "example_reviews": [],
                "notes": "Manually refined from raw review evidence"
            }
        ]
    }


def main():
    template = get_manual_group_template()
    print("Manual coding template loaded successfully.")
    print(template)


if __name__ == "__main__":
    main()