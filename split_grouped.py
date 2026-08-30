import pandas as pd
import re
from sklearn.model_selection import StratifiedGroupKFold

# Load cleaned dataset
df = pd.read_csv("dataset/processed/defect_dataset.csv")

print("Total samples:", len(df))
print("\nOriginal distribution:")
print(df["label"].value_counts().sort_index())


# --------------------------------------------------
# Create a group ID
# --------------------------------------------------
def make_group(filepath):
    filename = str(filepath).replace("\\", "/").split("/")[-1]

    # Remove .java
    filename = re.sub(r"\.java$", "", filename)

    # Remove Juliet variant suffixes:
    # _05, _52a, _81_bad, _81_goodG2B, etc.
    filename = re.sub(
        r"_\d+[a-z]?(?:_(?:bad|goodG2B|base))?$",
        "",
        filename,
        flags=re.IGNORECASE
    )

    return filename


df["group"] = df["file"].apply(make_group)

print("\nNumber of unique groups:", df["group"].nunique())


# --------------------------------------------------
# Stratified Group K-Fold
# --------------------------------------------------
sgkf = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# Create fold numbers
df["fold"] = -1

for fold, (train_idx, val_idx) in enumerate(
    sgkf.split(df, df["label"], groups=df["group"])
):
    df.loc[val_idx, "fold"] = fold


# --------------------------------------------------
# Use:
# Fold 0 -> Test
# Fold 1 -> Validation
# Folds 2,3,4 -> Training
# --------------------------------------------------

test_df = df[df["fold"] == 0].copy()
val_df = df[df["fold"] == 1].copy()
train_df = df[df["fold"].isin([2, 3, 4])].copy()


# --------------------------------------------------
# Remove helper columns
# --------------------------------------------------

train_df = train_df.drop(columns=["group", "fold"])
val_df = val_df.drop(columns=["group", "fold"])
test_df = test_df.drop(columns=["group", "fold"])


# --------------------------------------------------
# Save
# --------------------------------------------------

train_df.to_csv(
    "dataset/processed/group_train.csv",
    index=False
)

val_df.to_csv(
    "dataset/processed/group_val.csv",
    index=False
)

test_df.to_csv(
    "dataset/processed/group_test.csv",
    index=False
)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\n==============================")
print("GROUP-AWARE SPLIT COMPLETE")
print("==============================")

print("\nTrain:", train_df.shape)
print("Validation:", val_df.shape)
print("Test:", test_df.shape)

print("\nTrain distribution:")
print(train_df["label"].value_counts().sort_index())

print("\nValidation distribution:")
print(val_df["label"].value_counts().sort_index())

print("\nTest distribution:")
print(test_df["label"].value_counts().sort_index())


# --------------------------------------------------
# Verify group leakage
# --------------------------------------------------

train_groups = set(df[df["fold"].isin([2, 3, 4])]["group"])
val_groups = set(df[df["fold"] == 1]["group"])
test_groups = set(df[df["fold"] == 0]["group"])

print("\n==============================")
print("GROUP LEAKAGE CHECK")
print("==============================")

print("Train ∩ Validation:",
      len(train_groups & val_groups))

print("Train ∩ Test:",
      len(train_groups & test_groups))

print("Validation ∩ Test:",
      len(val_groups & test_groups))

print("\n0 in all three = GOOD")