
"""
AI-Assisted Code Risk Index (ACRI)
Prototype score for prioritizing code review.

This is a heuristic score, NOT a probability of defects.
Weights and thresholds are provisional and require validation.
"""


WEIGHTS = {
    "static_findings": 0.45,
    "complexity": 0.25,
    "model_signal": 0.30,
}

SEVERITY_POINTS = {
    "high": 3,
    "critical": 3,
    "medium": 2,
    "moderate": 2,
    "low": 1,
}


def _get_severity(finding):
    """Read common severity field names from a finding."""
    if not isinstance(finding, dict):
        return "medium"

    for key in ("severity", "level", "risk"):
        value = finding.get(key)
        if isinstance(value, str):
            value = value.strip().lower()
            if value in SEVERITY_POINTS:
                return value

    return "medium"


def _get_model_signal(prediction):
    """
    Normalize a reported confidence to 0-100.
    This is a model-strength signal, NOT defect probability.
    """
    if not isinstance(prediction, dict):
        return 0.0, "No prediction confidence was available."

    confidence = prediction.get(
        "confidence",
        prediction.get("score")
    )

    if not isinstance(confidence, (int, float)):
        return 0.0, "Prediction confidence was unavailable."

    confidence = float(confidence)

    # Accept either a fraction (0-1) or percentage (0-100).
    if 0.0 <= confidence <= 1.0:
        confidence *= 100.0

    confidence = max(0.0, min(100.0, confidence))

    return confidence, (
        "Uses the model's reported confidence as a signal, "
        "not as a probability of a defect."
    )


def calculate_acri(
    static_analysis=None,
    software_metrics=None,
    prediction=None,
    finding_threshold=10,
):
    """Return ACRI, component scores, weights, and limitations."""

    findings = static_analysis if isinstance(static_analysis, list) else []
    metrics = software_metrics if isinstance(software_metrics, dict) else {}
    prediction = prediction if isinstance(prediction, dict) else {}

    # Component 1: Static Finding Severity Score (SFS)
    weighted_findings = sum(
        SEVERITY_POINTS[_get_severity(item)]
        for item in findings
    )
    threshold = max(1, int(finding_threshold))
    sfs = min(100.0, 100.0 * weighted_findings / threshold)

    # Component 2: Complexity Risk (CR)
    raw_complexity = metrics.get(
        "cyclomatic_complexity_estimate", 1
    )
    try:
        complexity = max(1.0, float(raw_complexity))
    except (TypeError, ValueError):
        complexity = 1.0

    cr = min(100.0, max(0.0, ((complexity - 1.0) / 9.0) * 100.0))

    # Component 3: Model signal (MRS)
    mrs, model_note = _get_model_signal(prediction)

    # Overall ACRI: 0-100
    score = (
        WEIGHTS["static_findings"] * sfs
        + WEIGHTS["complexity"] * cr
        + WEIGHTS["model_signal"] * mrs
    )
    score = round(max(0.0, min(100.0, score)), 2)

    if score < 25:
        priority = "Low"
    elif score < 50:
        priority = "Moderate"
    elif score < 75:
        priority = "High"
    else:
        priority = "Critical"

    return {
        "score": score,
        "priority": priority,
        "components": {
            "static_finding_severity_score": round(sfs, 2),
            "complexity_risk": round(cr, 2),
            "model_signal": round(mrs, 2),
        },
        "weights": WEIGHTS.copy(),
        "details": {
            "finding_count": len(findings),
            "weighted_findings": weighted_findings,
            "complexity_estimate": complexity,
            "predicted_label": prediction.get("label"),
        },
        "explanation": (
            "This score combines static finding severity, "
            "complexity risk, and the AI model signal."
        ),
        "model_signal_note": model_note,
    }
