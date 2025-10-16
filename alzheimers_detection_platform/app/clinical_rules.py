
def apply_clinical_rules(clinical_data):
    """
    Apply clinical rules based on patient data
    Returns a risk score between 0 and 1
    """
    risk_score = 0.0
    risk_factors = []

    # Age-based risk
    age = clinical_data.get('age', 0)
    if age >= 65:
        risk_score += 0.2
        risk_factors.append(f"Age ({age})")

    # Family history
    if clinical_data.get('family_history', False):
        risk_score += 0.15
        risk_factors.append("Family history")

    # Cardiovascular issues
    if clinical_data.get('cardiovascular_issues', False):
        risk_score += 0.1
        risk_factors.append("Cardiovascular issues")

    # Diabetes
    if clinical_data.get('diabetes', False):
        risk_score += 0.1
        risk_factors.append("Diabetes")

    # Depression
    if clinical_data.get('depression', False):
        risk_score += 0.05
        risk_factors.append("Depression")

    # Head trauma
    if clinical_data.get('head_trauma', False):
        risk_score += 0.1
        risk_factors.append("Head trauma")

    # Cap risk score at 0.95
    risk_score = min(risk_score, 0.95)

    return {
        "risk_score": risk_score,
        "risk_factors": risk_factors
    }