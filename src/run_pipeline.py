import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


PIPELINE_STEPS = [
    ("Cleaning data", "src/clean_data.py"),
    ("Generating data quality report", "src/data_quality_report.py"),
    ("Quarantining invalid records", "src/quarantine_records.py"),
    ("Verifying data quality", "src/verify_quality.py"),
    ("Creating Gold layer", "src/create_gold_layer.py"),
    ("Creating dashboard metrics", "src/create_dashboard_metrics.py"),
]


def run_step(name, script):
    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / script)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print()
        print(f"PIPELINE FAILED: {name}")
        print(f"Script: {script}")
        sys.exit(result.returncode)


def main():

    print("=" * 60)
    print("ASG AIRLINES DATA ENGINEERING PIPELINE")
    print("=" * 60)

    for name, script in PIPELINE_STEPS:
        run_step(name, script)

    print()
    print("=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()