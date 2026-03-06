def estimate_severity(confidence):
    confidence = confidence * 100

    if confidence < 50:
        return "Mild"
    elif confidence < 75:
        return "Moderate"
    else:
        return "Severe"
