"""
run_all.py

Runs the automated pipeline end-to-end for the EECS 4312 SpecChain project.

Execution order:
1. Collect raw reviews -> data/reviews_raw.jsonl
2. Clean reviews -> data/reviews_clean.jsonl
3. Generate automated review groups and personas -> data/review_groups_auto.json, personas/personas_auto.json
4. Generate automated specification -> spec/spec_auto.md
5. Generate automated tests -> tests/tests_auto.json
6. Compute metrics across pipelines -> metrics/*.json
"""

import subprocess
import sys


def run_step(step_name: str, script_path: str) -> None:
    print(f"\n=== Running: {step_name} ===")
    result = subprocess.run([sys.executable, script_path], check=False)
    if result.returncode != 0:
        print(f"Step failed: {step_name}")
        sys.exit(result.returncode)
    print(f"Completed: {step_name}")


def main() -> None:
    print("Starting automated pipeline...")

    run_step("Collect raw reviews", "src/01_collect_or_import.py")
    run_step("Clean reviews", "src/02_clean.py")
    run_step("Generate automated groups and personas", "src/05_personas_auto.py")
    run_step("Generate automated specification", "src/06_spec_generate.py")
    run_step("Generate automated tests", "src/07_tests_generate.py")
    run_step("Compute metrics", "src/08_metrics.py")

    print("\nAutomated pipeline finished successfully.")


if __name__ == "__main__":
    main()