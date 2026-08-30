from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

import sys
import os


# ============================================================
# PATH SETUP
# ============================================================

# Project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Model directory
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "codebert_1500_model"
)

# Source directory
SRC_PATH = os.path.join(
    BASE_DIR,
    "src"
)

# Add src directory to Python path
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)


# Import static analysis function
from static_analysis import analyze_java_code


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Java Defect Prediction API",
    description="Static Analysis + CodeBERT Defect Prediction",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

# Allows your frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DEVICE CONFIGURATION
# ============================================================

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("=" * 60)
print("Java Defect Prediction API")
print("=" * 60)
print("Using device:", device)
print("Model path:", MODEL_PATH)
print("=" * 60)


# ============================================================
# CHECK MODEL PATH
# ============================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"CodeBERT model not found at: {MODEL_PATH}"
    )


# ============================================================
# LOAD TOKENIZER
# ============================================================

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

print("Tokenizer loaded successfully.")


# ============================================================
# LOAD CODEBERT MODEL
# ============================================================

print("Loading CodeBERT model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)

model.eval()

print("CodeBERT model loaded successfully.")


# ============================================================
# DEFECT LABELS
# ============================================================

LABELS = {
    0: "CWE-23",
    1: "CWE-36",
    2: "CWE-476",
    3: "CWE-78",
    4: "CWE-80",
    5: "CWE-89"
}


# ============================================================
# REQUEST MODEL
# ============================================================

class CodeRequest(BaseModel):

    code: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Java Defect Prediction API is running"
    }


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": True,
        "device": str(device)
    }


# ============================================================
# CODEBERT PREDICTION FUNCTION
# ============================================================

def predict_defect(code: str):

    # Tokenize Java code
    inputs = tokenizer(
        code,
        truncation=True,
        padding=True,
        max_length=256,
        return_tensors="pt"
    )

    # Move tensors to CPU/GPU
    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    # Disable gradient calculation
    with torch.no_grad():

        outputs = model(
            **inputs
        )

    # Convert logits to probabilities
    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )

    # Get predicted class
    predicted_id = torch.argmax(
        probabilities,
        dim=1
    ).item()

    # Get confidence
    confidence = probabilities[
        0,
        predicted_id
    ].item()

    # Get label
    label = LABELS.get(
        predicted_id,
        f"UNKNOWN-{predicted_id}"
    )

    return {
        "label": label,
        "confidence": round(
            confidence * 100,
            2
        )
    }


# ============================================================
# ANALYZE CODE ENDPOINT
# ============================================================

@app.post("/analyze")
def analyze_code(request: CodeRequest):

    # Get Java code
    code = request.code

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    if not code or not code.strip():

        return {
            "success": False,
            "message": "Code cannot be empty.",
            "prediction": None,
            "static_analysis": []
        }


    try:

        # ----------------------------------------------------
        # STATIC ANALYSIS
        # ----------------------------------------------------

        static_results = analyze_java_code(
            code
        )


        # ----------------------------------------------------
        # CODEBERT PREDICTION
        # ----------------------------------------------------

        prediction = predict_defect(
            code
        )


        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        return {

            "success": True,

            "prediction": prediction,

            "static_analysis": static_results

        }


    except Exception as e:

        print(
            "Error while analyzing code:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing code: {str(e)}"
        )


# ============================================================
# END OF FILE
# ============================================================