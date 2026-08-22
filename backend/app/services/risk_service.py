from __future__ import annotations


def calculate_risk_score(confidence: float, source_reliability: float, corroborating_sources: int, vulnerability_count: int = 0) -> float:
    """Return an explainable score between 0 and 100.

    The formula gives the largest weight to confidence, then source reliability,
    and then a smaller boost for corroboration and vulnerabilities.
    """

    corroboration_score = min(corroborating_sources * 18.0, 100.0)
    vulnerability_boost = min(vulnerability_count * 4.0, 20.0)

    raw_score = (
        confidence * 0.5
        + source_reliability * 0.3
        + corroboration_score * 0.15
        + vulnerability_boost * 0.05
    )
    return max(0.0, min(round(raw_score, 2), 100.0))


def determine_severity(risk_score: float) -> str:
    if risk_score <= 24:
        return "Low"
    if risk_score <= 49:
        return "Medium"
    if risk_score <= 74:
        return "High"
    return "Critical"
