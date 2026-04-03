"""
run_all.py

Runs the automated pipeline end-to-end for the EECS 4312 SpecChain project.

Execution order:
1. Collect/import raw reviews -> data/reviews_raw.jsonl
2. Clean reviews -> data/reviews_clean.jsonl
3. Generate automated review groups -> data/review_groups_auto.json
4. Generate automated personas -> personas/personas_auto.json
5. Generate automated specification -> spec/spec_auto.md
6. Generate automated tests -> tests/tests_auto.json
7. Compute automated metrics -> metrics/metrics_auto.json

This script automates only the programmatic pipeline, as required.
"""

import subprocess
import sys
from pathlib import Path


def run_step(step_name: str, script_path: str) -> None:
    print(f"\n=== Running: {step_name} ===")
    result = subprocess.run([sys.executable, script_path], check=False)
    if result.returncode != 0:
        print(f"Step failed: {step_name}")
        sys.exit(result.returncode)
    print(f"Completed: {step_name}")


def main() -> None:
    print("Starting automated pipeline...")

    # Step 1: collect/import raw reviews
    run_step("Collect raw reviews", "src/01_collect_or_import.py")

    # Step 2: clean raw reviews
    run_step("Clean reviews", "src/02_clean.py")

    # Step 3: generate automated review groups and personas
    run_step("Generate automated groups and personas", "src/05_personas_auto.py")

    # Step 4: generate automated specification
    run_step("Generate automated specification", "src/06_spec_generate.py")

    # Step 5: generate automated tests
    run_step("Generate automated tests", "src/07_tests_generate.py")

    # Step 6: compute automated metrics
    run_step("Compute automated metrics", "src/08_metrics.py")

    print("\nAutomated pipeline finished successfully.")
    print("Generated files should now include:")
    print("- data/reviews_raw.jsonl")
    print("- data/reviews_clean.jsonl")
    print("- data/review_groups_auto.json")
    print("- personas/personas_auto.json")
    print("- spec/spec_auto.md")
    print("- tests/tests_auto.json")
    print("- metrics/metrics_auto.json")


if __name__ == "__main__":
    main()