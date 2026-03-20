def calculate_risk(prompt_detected, hidden_detected, action_text=""):
    score = 0
    reasons = []

    if prompt_detected:
        score += 0.5
        reasons.append("Prompt injection detected")

    if hidden_detected:
        score += 0.3
        reasons.append("Hidden suspicious content")

    risky_words = ["login", "password", "verify", "confirm", "submit"]

    for word in risky_words:
        if word in action_text.lower():
            score += 0.4
            reasons.append(f"Sensitive action: {word}")
            break

    return min(score, 1.0), reasons