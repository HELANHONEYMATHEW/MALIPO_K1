BAD_PATTERNS = [
    "ignore previous instructions",
    "reveal your password",
    "enter your credentials",
    "send me your api key",
    "bypass security"
]

def detect_prompt_injection(text):
    text = text.lower()
    for pattern in BAD_PATTERNS:
        if pattern in text:
            return True, pattern
    return False, None