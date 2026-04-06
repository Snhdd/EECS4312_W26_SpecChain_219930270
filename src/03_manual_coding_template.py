


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