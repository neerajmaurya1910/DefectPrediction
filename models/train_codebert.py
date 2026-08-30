import os
import pandas as pd
import torch

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)

from torch.utils.data import Dataset


# ============================================================
# CONFIG
# ============================================================

MODEL_NAME = "microsoft/codebert-base"

TRAIN_PATH = "dataset/processed/clean_group_train.csv"
VAL_PATH = "dataset/processed/clean_group_val.csv"
TEST_PATH = "dataset/processed/clean_group_test.csv"

OUTPUT_DIR = "./models/codebert_1500_model"

MAX_LENGTH = 256


# ============================================================
# LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
val_df = pd.read_csv(VAL_PATH)
test_df = pd.read_csv(TEST_PATH)

print("=" * 60)
print("DATASET")
print("=" * 60)

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)

print("\nTraining distribution:")
print(train_df["label"].value_counts().sort_index())

print("\nValidation distribution:")
print(val_df["label"].value_counts().sort_index())

print("\nTesting distribution:")
print(test_df["label"].value_counts().sort_index())


# ============================================================
# LABEL ENCODING
# ============================================================

label_encoder = LabelEncoder()

all_labels = pd.concat([
    train_df["label"],
    val_df["label"],
    test_df["label"]
])

label_encoder.fit(all_labels)

train_df["label_id"] = label_encoder.transform(train_df["label"])
val_df["label_id"] = label_encoder.transform(val_df["label"])
test_df["label_id"] = label_encoder.transform(test_df["label"])

num_labels = len(label_encoder.classes_)

print("\nClasses:")
print(label_encoder.classes_)

print("Number of classes:", num_labels)


# ============================================================
# TOKENIZER
# ============================================================

print("\n" + "=" * 60)
print("LOADING CODEBERT TOKENIZER")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


# ============================================================
# DATASET
# ============================================================

class CodeDataset(Dataset):

    def __init__(self, dataframe):
        self.codes = dataframe["code"].astype(str).tolist()
        self.labels = dataframe["label_id"].tolist()

    def __len__(self):
        return len(self.codes)

    def __getitem__(self, index):

        encoding = tokenizer(
            self.codes[index],
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(
                self.labels[index],
                dtype=torch.long
            )
        }


train_dataset = CodeDataset(train_df)
val_dataset = CodeDataset(val_df)
test_dataset = CodeDataset(test_df)

print("\nTraining samples:", len(train_dataset))
print("Validation samples:", len(val_dataset))
print("Testing samples:", len(test_dataset))

# ============================================================
# MODEL
# ============================================================

print("\n" + "=" * 60)
print("LOADING CODEBERT")
print("=" * 60)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels
)


# ============================================================
# METRICS
# ============================================================

def compute_metrics(eval_pred):

    predictions, labels = eval_pred

    predicted_labels = predictions.argmax(axis=1)

    accuracy = accuracy_score(
        labels,
        predicted_labels
    )

    report = classification_report(
        labels,
        predicted_labels,
        labels=list(range(num_labels)),
        target_names=[
            str(x) for x in label_encoder.classes_
        ],
        output_dict=True,
        zero_division=0
    )

    macro_f1 = report["macro avg"]["f1-score"]

    weighted_f1 = report["weighted avg"]["f1-score"]

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1
    }


# ============================================================
# TRAINING ARGUMENTS
# ============================================================

training_args = TrainingArguments(

    output_dir="./models/codebert_results",

    # More epochs, but early stopping will prevent
    # unnecessary training.
    num_train_epochs=15,

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    learning_rate=1e-5,

    weight_decay=0.05,

    warmup_steps=10,

    logging_steps=10,

    eval_strategy="epoch",

    save_strategy="epoch",

    load_best_model_at_end=True,

    metric_for_best_model="macro_f1",

    greater_is_better=True,

    save_total_limit=2,

    report_to="none",

    fp16=False,

    dataloader_pin_memory=False
)


# ============================================================
# TRAINER
# ============================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=val_dataset,

    compute_metrics=compute_metrics,

    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=3
        )
    ]
)


# ============================================================
# TRAIN
# ============================================================

print("\n" + "=" * 60)
print("TRAINING CODEBERT")
print("=" * 60)

trainer.train()


# ============================================================
# FINAL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL EVALUATION")
print("=" * 60)

predictions = trainer.predict(test_dataset)

predicted_labels = predictions.predictions.argmax(axis=1)

true_labels = test_df["label_id"].values


# Accuracy

accuracy = accuracy_score(
    true_labels,
    predicted_labels
)

print("\nAccuracy:", round(accuracy * 100, 2), "%")


# Detailed report

print("\nClassification Report:\n")

print(
    classification_report(
        true_labels,
        predicted_labels,
        labels=list(range(num_labels)),
        target_names=[
            str(x) for x in label_encoder.classes_
        ],
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(
    true_labels,
    predicted_labels
)

print("\nConfusion Matrix:\n")

print(cm)


# ============================================================
# SAVE MODEL
# ============================================================

print("\n" + "=" * 60)
print("SAVING MODEL")
print("=" * 60)

os.makedirs(OUTPUT_DIR, exist_ok=True)

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

# Save label encoder

import pickle

with open(
    os.path.join(
        OUTPUT_DIR,
        "label_encoder.pkl"
    ),
    "wb"
) as f:

    pickle.dump(
        label_encoder,
        f
    )


print("\nCodeBERT model saved successfully!")

print("Model location:")
print(os.path.abspath(OUTPUT_DIR))