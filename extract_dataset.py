from pathlib import Path
import csv
import random

# Repository location
BASE_DIR = Path("juliet-java-test-suite")

# Six defect categories
CATEGORIES = {
    "CWE-23": "juliet-cwe23",
    "CWE-36": "juliet-cwe36",
    "CWE-476": "juliet-cwe476",
    "CWE-78": "juliet-cwe78",
    "CWE-80": "juliet-cwe80",
    "CWE-89": "juliet-cwe89",
}

SAMPLES_PER_CATEGORY = 250

OUTPUT_DIR = Path("dataset/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

dataset = []

for label, folder_name in CATEGORIES.items():

    folder = BASE_DIR / folder_name

    if not folder.exists():
        print(f"Folder not found: {folder}")
        continue

    # Find all Java files
    java_files = list(folder.rglob("*.java"))

    print(f"{label}: found {len(java_files)} Java files")

    # Shuffle files
    random.shuffle(java_files)

   
    # Take 250 files
    selected_files = java_files[:SAMPLES_PER_CATEGORY]

    for file_path in selected_files:

        try:
            code = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            dataset.append({
                "label": label,
                "file": str(file_path),
                "code": code
            })

        except Exception as e:
            print(f"Could not read {file_path}: {e}")


# Shuffle complete dataset
random.shuffle(dataset)


# Save CSV
output_file = OUTPUT_DIR / "defect_dataset.csv"

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=["label", "file", "code"]
    )

    writer.writeheader()
    writer.writerows(dataset)


print()
print("=" * 50)
print("DATASET CREATED")
print("=" * 50)

print(f"Total samples: {len(dataset)}")
print(f"Output: {output_file}")

for label in CATEGORIES:
    count = sum(1 for item in dataset if item["label"] == label)
    print(f"{label}: {count}")