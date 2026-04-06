

from pathlib import Path

REQUIRED_PATHS = [
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "prompts/prompt_auto.json",
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/04_personas_manual.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",
    "README.md",
    "reflection/reflection.md"
]


def main() -> None:
    print("Checking repository structure...")

    missing = []

    for rel_path in REQUIRED_PATHS:
        path = Path(rel_path)
        if path.exists():
            print(f"{rel_path} found")
        else:
            print(f"{rel_path} MISSING")
            missing.append(rel_path)

    if missing:
        print("\nRepository validation failed.")
        print("Missing files:")
        for item in missing:
            print(f"- {item}")
    else:
        print("\nRepository validation complete")
        print("All required files are present.")


if __name__ == "__main__":
    main()