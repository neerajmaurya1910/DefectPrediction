import pandas as pd
import torch
import pickle
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import confusion_matrix, classification_report

# ==============================
# CONFIG
# ==============================

MODEL_PATH = "./models/codebert_1500_model"
TEST_PATH = "dataset/processed/clean_group_test.csv"

# ==============================
# LOAD MODEL
# ==============================

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

# ==============================
# LOAD TEST DATA
# ==============================

df = pd.read_csv(TEST_PATH)

print(f"Test samples: {len(df)}")

# ==============================
# LABEL MAPPING
# ==============================

import pickle

with open(f"{MODEL_PATH}/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

id2label = {
    i: label
    for i, label in enumerate(label_encoder.classes_)
}

print("\nLabel mapping:")
print(id2label)

# ==============================
# PREDICTIONS
# ==============================

predictions = []

print("\nRunning predictions...")

for i, code in enumerate(df["code"]):

    inputs = tokenizer(
        str(code),
        truncation=True,
        padding=True,
        max_length=256,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_id = torch.argmax(outputs.logits, dim=1).item()

    predictions.append(id2label[predicted_id])

    if (i + 1) % 50 == 0:
        print(f"Processed {i + 1}/{len(df)}")

# ==============================
# ADD PREDICTIONS
# ==============================

df["prediction"] = predictions

# ==============================
# FIND ERRORS
# ==============================

errors = df[df["label"] != df["prediction"]].copy()

print("\n==============================")
print("ERROR ANALYSIS")
print("==============================")

print(f"Total test samples: {len(df)}")
print(f"Correct predictions: {len(df) - len(errors)}")
print(f"Wrong predictions: {len(errors)}")

print(
    f"Error rate: {len(errors) / len(df) * 100:.2f}%"
)

# ==============================
# ERROR DISTRIBUTION
# ==============================

print("\nErrors by actual label:")

print(
    errors["label"]
    .value_counts()
    .sort_index()
)

print("\nMost common wrong predictions:")

print(
    errors.groupby(["label", "prediction"])
    .size()
    .sort_values(ascending=False)
    .head(20)
)

# ==============================
# SHOW CWE-23 / CWE-36 ERRORS
# ==============================

pair_errors = errors[
    (
        (errors["label"] == "CWE-23") &
        (errors["prediction"] == "CWE-36")
    )
    |
    (
        (errors["label"] == "CWE-36") &
        (errors["prediction"] == "CWE-23")
    )
]

print("\n==============================")
print("CWE-23 <-> CWE-36 ERRORS")
print("==============================")

print(f"Total: {len(pair_errors)}")

for _, row in pair_errors.iterrows():

    print("\n------------------------------")

    print("Actual:    ", row["label"])
    print("Predicted: ", row["prediction"])
    print("File:      ", row["file"])

# ==============================
# SAVE ALL ERRORS
# ==============================

errors.to_csv(
    "dataset/processed/error_analysis.csv",
    index=False
)

print("\nError file saved:")
print("dataset/processed/error_analysis.csv")

print("\nDone!")