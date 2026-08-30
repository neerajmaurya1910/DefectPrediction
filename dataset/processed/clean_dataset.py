import pandas as pd
import re


def clean_java_code(code):
    if not isinstance(code, str):
        return ""

    # Remove /* ... */ block comments
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

    # Remove // comments
    code = re.sub(r"//.*", "", code)

    # Remove CWE identifiers from class/package names
    # Example:
    # CWE36_Absolute_Path_Traversal__Property_52a
    # becomes:
    # VULNERABILITY_CLASS
    code = re.sub(
        r"\bCWE\d+_[A-Za-z0-9_]+",
        "VULNERABILITY_CLASS",
        code
    )
    # Remove remaining obvious CWE references
    code = re.sub(r"\bCWE[-_ ]?\d+\b", "", code, flags=re.IGNORECASE)

    # Remove excessive blank lines
    code = re.sub(r"\n\s*\n+", "\n\n", code)

    return code.strip()

# Load datasets
train = pd.read_csv("dataset/processed/group_train.csv")
val = pd.read_csv("dataset/processed/group_val.csv")
test = pd.read_csv("dataset/processed/group_test.csv")

# Clean Java code
train["code"] = train["code"].apply(clean_java_code)
val["code"] = val["code"].apply(clean_java_code)
test["code"] = test["code"].apply(clean_java_code)

# Save new datasets
train.to_csv("dataset/processed/clean_group_train.csv", index=False)
val.to_csv("dataset/processed/clean_group_val.csv", index=False)
test.to_csv("dataset/processed/clean_group_test.csv", index=False)

print("Cleaning completed!")
print("Clean train:", train.shape)
print("Clean validation:", val.shape)
print("Clean test:", test.shape)
print("\nTrain distribution:")
print(train["label"].value_counts().sort_index())

print("\nTest distribution:")
print(test["label"].value_counts().sort_index())