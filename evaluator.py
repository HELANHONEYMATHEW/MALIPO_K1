from detector import detect_prompt_injection
from test_cases import test_data

def evaluate():
    TP = FP = TN = FN = 0

    for case in test_data:
        text = case["text"]
        actual = case["label"]

        detected, _ = detect_prompt_injection(text)
        predicted = 1 if detected else 0

        if predicted == 1 and actual == 1:
            TP += 1
        elif predicted == 1 and actual == 0:
            FP += 1
        elif predicted == 0 and actual == 0:
            TN += 1
        elif predicted == 0 and actual == 1:
            FN += 1

    # Metrics
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

    print("\n📊 Evaluation Results")
    print("---------------------")
    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall (Detection Rate): {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")