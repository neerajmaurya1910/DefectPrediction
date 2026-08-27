import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==============================
# LOAD DATASET
# ==============================

df = pd.read_csv("dataset/processed/defect_dataset.csv")

X_text = df["code"]
y = df["label"]


# ==============================
# ENCODE LABELS
# ==============================

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# ==============================
# TF-IDF
# ==============================

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    lowercase=True
)

X = vectorizer.fit_transform(X_text)


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
# TRAIN MODEL
# ==============================

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train, y_train)


# ==============================
# PREDICTION
# ==============================

y_pred = model.predict(X_test)


# ==============================
# EVALUATION
# ==============================

accuracy = accuracy_score(y_test, y_pred)

print("\n===== MODEL RESULTS =====")
print("Accuracy:", accuracy)

print("\n===== CLASSIFICATION REPORT =====")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)


# ==============================
# SAVE MODEL
# ==============================

joblib.dump(model, "models/defect_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("\n===== MODEL SAVED =====")
print("models/defect_model.pkl")