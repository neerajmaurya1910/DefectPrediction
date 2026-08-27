import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os


# ==============================
# LOAD DATASET
# ==============================

df = pd.read_csv("dataset/processed/defect_dataset.csv")

print("Dataset shape:", df.shape)


# ==============================
# CLEAN DATA
# ==============================

# Remove missing values
df = df.dropna(subset=["code", "label"])

# Remove duplicate code snippets
df = df.drop_duplicates(subset=["code"])

print("After cleaning:", df.shape)


# ==============================
# FEATURES AND TARGET
# ==============================

X = df["code"]
y = df["label"]


# ==============================
# ENCODE LABELS
# ==============================

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\n===== LABELS =====")
print("Classes:", label_encoder.classes_)


# ==============================
# TRAIN / TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ==============================
# DATASET INFORMATION
# ==============================

print("\n===== DATA SPLIT =====")

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


print("\n===== TRAIN LABELS =====")

train_labels = pd.Series(y_train)
print(train_labels.value_counts().sort_index())


print("\n===== TEST LABELS =====")

test_labels = pd.Series(y_test)
print(test_labels.value_counts().sort_index())


# ==============================
# SAVE PROCESSED DATA
# ==============================

os.makedirs("dataset/processed", exist_ok=True)


train_df = pd.DataFrame({
    "code": X_train.values,
    "label": y_train
})

test_df = pd.DataFrame({
    "code": X_test.values,
    "label": y_test
})


train_df.to_csv(
    "dataset/processed/train.csv",
    index=False
)

test_df.to_csv(
    "dataset/processed/test.csv",
    index=False
)


# Save label encoder
joblib.dump(
    label_encoder,
    "dataset/processed/label_encoder.pkl"
)


# ==============================
# COMPLETE
# ==============================

print("\n===== PREPROCESSING COMPLETE =====")

print("Saved:")
print("dataset/processed/train.csv")
print("dataset/processed/test.csv")
print("dataset/processed/label_encoder.pkl")