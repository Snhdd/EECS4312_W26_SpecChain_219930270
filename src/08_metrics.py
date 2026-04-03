"""
08_metrics.py

Computes and compares metrics across the manual, automated, and hybrid pipelines.

Outputs:
- metrics/metrics_manual.json
- metrics/metrics_auto.json
- metrics/metrics_hybrid.json
- metrics/metrics_summary.json
"""

import json
from pathlib import Path


CLEAN_REVIEWS_PATH = Path("data/reviews_clean.jsonl")

MANUAL_GROUPS_PATH = Path("data/review_groups_manual.json")
AUTO_GROUPS_PATH = Path("data/review_groups_auto.json")
HYBRID_GROUPS_PATH = Path("data/review_groups_hybrid.json")

MANUAL_PERSONAS_PATH = Path("personas/personas_manual.json")
AUTO_PERSONAS_PATH = Path("personas/personas_auto.json")
HYBRID_PERSONAS_PATH = Path("personas/personas_hybrid.json")

MANUAL_SPEC_PATH = Path("spec/spec_manual.md")
AUTO_SPEC_PATH = Path("spec/spec_auto.md")
HYBRID_SPEC_PATH = Path("spec/spec_hybrid.md")

MANUAL_TESTS_PATH = Path("tests/tests_manual.json")
AUTO_TESTS_PATH = Path("tests/tests_auto.json")
HYBRID_TESTS_PATH = Path("tests/tests_hybrid.json")

METRICS_MANUAL_PATH = Path("metrics/metrics_manual.json")
METRICS_AUTO_PATH = Path("metrics/metrics_auto.json")
METRICS_HYBRID_PATH = Path("metrics/metrics_hybrid.json")
METRICS_SUMMARY_PATH = Path("metrics/metrics_summary.json")


AMBIGUOUS_WORDS = {
    "fast", "easy", "better", "user-friendly", "quick", "efficient",
    "simple", "smooth", "intuitive", "seamless", "good", "great"
}


def count_jsonl(path: Path) -> int:
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def count_requirements_in_md(path: Path) -> int:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text.count("# Requirement ID:")


def extract_requirement_blocks(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    blocks = [b.strip() for b in text.split("# Requirement ID:") if b.strip()]
    parsed = []

    for block in blocks:
        lines = block.splitlines()
        req_id = lines[0].strip()
        description = ""
        acceptance = ""

        for line in lines[1:]:
            if line.startswith("- Description:"):
                description = line.replace("- Description:", "").strip().lower()
            elif line.startswith("- Acceptance Criteria:"):
                acceptance = line.replace("- Acceptance Criteria:", "").strip().lower()

        parsed.append({
            "id": req_id,
            "description": description,
            "acceptance": acceptance
        })

    return parsed


def ambiguity_ratio(spec_path: Path) -> float:
    reqs = extract_requirement_blocks(spec_path)
    if not reqs:
        return 0.0

    ambiguous_count = 0
    for req in reqs:
        text = f"{req['description']} {req['acceptance']}"
        if any(word in text for word in AMBIGUOUS_WORDS):
            ambiguous_count += 1

    return round(ambiguous_count / len(reqs), 4)


def compute_pipeline_metrics(groups_path: Path, personas_path: Path, spec_path: Path, tests_path: Path):
    dataset_size = count_jsonl(CLEAN_REVIEWS_PATH)

    groups = load_json(groups_path)["groups"]
    personas = load_json(personas_path)["personas"]
    tests = load_json(tests_path)["tests"]

    requirements_count = count_requirements_in_md(spec_path)
    persona_count = len(personas)
    tests_count = len(tests)

    total_review_refs = sum(len(group.get("review_ids", [])) for group in groups)
    review_coverage_ratio = round(total_review_refs / dataset_size, 4) if dataset_size else 0.0

    traceability_ratio = 1.0 if requirements_count > 0 else 0.0
    testability_rate = round(min(tests_count / requirements_count, 1.0), 4) if requirements_count else 0.0
    traceability_links = persona_count + requirements_count

    return {
        "dataset_size": dataset_size,
        "persona_count": persona_count,
        "requirements_count": requirements_count,
        "tests_count": tests_count,
        "traceability_links": traceability_links,
        "review_coverage_ratio": review_coverage_ratio,
        "traceability_ratio": traceability_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": ambiguity_ratio(spec_path)
    }


def main():
    print("Computing metrics across pipelines...")

    manual_metrics = compute_pipeline_metrics(
        MANUAL_GROUPS_PATH, MANUAL_PERSONAS_PATH, MANUAL_SPEC_PATH, MANUAL_TESTS_PATH
    )
    auto_metrics = compute_pipeline_metrics(
        AUTO_GROUPS_PATH, AUTO_PERSONAS_PATH, AUTO_SPEC_PATH, AUTO_TESTS_PATH
    )
    hybrid_metrics = compute_pipeline_metrics(
        HYBRID_GROUPS_PATH, HYBRID_PERSONAS_PATH, HYBRID_SPEC_PATH, HYBRID_TESTS_PATH
    )

    with open(METRICS_MANUAL_PATH, "w", encoding="utf-8") as f:
        json.dump(manual_metrics, f, indent=2)

    with open(METRICS_AUTO_PATH, "w", encoding="utf-8") as f:
        json.dump(auto_metrics, f, indent=2)

    with open(METRICS_HYBRID_PATH, "w", encoding="utf-8") as f:
        json.dump(hybrid_metrics, f, indent=2)

    summary = {
        "manual": manual_metrics,
        "automated": auto_metrics,
        "hybrid": hybrid_metrics
    }

    with open(METRICS_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved {METRICS_MANUAL_PATH}")
    print(f"Saved {METRICS_AUTO_PATH}")
    print(f"Saved {METRICS_HYBRID_PATH}")
    print(f"Saved {METRICS_SUMMARY_PATH}")


if __name__ == "__main__":
    main()