import re
import json
from pathlib import Path

AUTO_SPEC_PATH = Path("spec/spec_auto.md")
AUTO_TESTS_PATH = Path("tests/tests_auto.json")


def parse_requirements():
    with open(AUTO_SPEC_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = [b.strip() for b in content.split("# Requirement ID:") if b.strip()]
    requirements = []

    for block in blocks:
        lines = block.splitlines()
        req_id = lines[0].strip()

        desc = ""
        for line in lines[1:]:
            if line.startswith("- Description:"):
                desc = line.replace("- Description:", "").strip()
                break

        requirements.append({
            "id": req_id,
            "description": desc
        })

    return requirements


def make_tests(requirements):
    tests = []
    counter = 1

    for req in requirements:
        req_id = req["id"]
        desc = req["description"]

        tests.append({
            "test_id": f"T_auto_{counter}",
            "requirement_id": req_id,
            "scenario": f"Primary validation for {req_id}",
            "steps": [
                "Open the relevant application feature",
                "Trigger the functionality related to the requirement",
                "Observe the system behavior"
            ],
            "expected_result": f"The system satisfies the requirement: {desc}"
        })
        counter += 1

        tests.append({
            "test_id": f"T_auto_{counter}",
            "requirement_id": req_id,
            "scenario": f"Secondary validation for {req_id}",
            "steps": [
                "Access the same feature as a typical user",
                "Repeat the interaction under normal usage conditions",
                "Verify the output remains correct"
            ],
            "expected_result": f"The feature continues to behave according to requirement {req_id}."
        })
        counter += 1

    return {"tests": tests}


def main():
    requirements = parse_requirements()
    tests = make_tests(requirements)

    with open(AUTO_TESTS_PATH, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)

    print(f"Saved automated tests to {AUTO_TESTS_PATH}")


if __name__ == "__main__":
    main()