import pandas as pd
import torch

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

from torch.utils.data import Dataset


# ==============================
# LOAD DATASET
# ==============================

train_df = pd.read_csv("dataset/processed/train.csv")
test_df = pd.read_csv("dataset/processed/test.csv")

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)


# ==============================
# ENCODE LABELS
# ==============================

label_encoder = LabelEncoder()

all_labels = pd.concat([
    train_df["label"],
    test_df["label"]
])

label_encoder.fit(all_labels)

train_df["label_id"] = label_encoder.transform(train_df["label"])
test_df["label_id"] = label_encoder.transform(test_df["label"])

print("\n===== CLASSES =====")
print(label_encoder.classes_)


# ==============================
# CODEBERT TOKENIZER
# ==============================

MODEL_NAME = "microsoft/codebert-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


# ==============================
# DATASET CLASS
# ==============================

class CodeDataset(Dataset):

    def __init__(self, dataframe):
        self.codes = dataframe["code"].tolist()
        self.labels = dataframe["label_id"].tolist()

    def __len__(self):
        return len(self.codes)

    def __getitem__(self, index):

        encoding = tokenizer(
            self.codes[index],
            truncation=True,
            padding="max_length",
            max_length=256,
            return_tensors="pt"
        )

        item = {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(self.labels[index], dtype=torch.long)
        }

        return item


# ==============================
# CREATE DATASETS
# ==============================

train_dataset = CodeDataset(train_df)
test_dataset = CodeDataset(test_df)

print("\n===== DATASET =====")
print("Training samples:", len(train_dataset))
print("Testing samples:", len(test_dataset))


# ==============================
# LOAD CODEBERT
# ==============================

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label_encoder.classes_)
)


# ==============================
# TRAINING ARGUMENTS
# ==============================

training_args = TrainingArguments(
    output_dir="./models/codebert_results",

    num_train_epochs=5,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    learning_rate=2e-5,

    weight_decay=0.01,

    logging_steps=10,

    save_strategy="epoch",

    eval_strategy="epoch",

    load_best_model_at_end=True,

    report_to="none"
)


# ==============================
# TRAINER
# ==============================

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)


# ==============================
# TRAIN MODEL
# ==============================

print("\n===== TRAINING CODEBERT =====")

trainer.train()


# ==============================
# EVALUATION
# ==============================

print("\n===== EVALUATION =====")

predictions = trainer.predict(test_dataset)

predicted_labels = predictions.predictions.argmax(axis=1)

print(
    classification_report(
        test_df["label_id"],
        predicted_labels,
        labels=list(range(len(label_encoder.classes_))),
        target_names=[str(x) for x in label_encoder.classes_],
        zero_division=0
    )
)


# ==============================
# SAVE MODEL
# ==============================

print("\n===== SAVING MODEL =====")

trainer.save_model("./models/codebert_model")
tokenizer.save_pretrained("./models/codebert_model")

print("CodeBERT model saved successfully.")