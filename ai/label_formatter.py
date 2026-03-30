def format_disease_label(label):
    """
    Converts model labels into clean user-friendly disease names.

    Examples:
    Tomato___Early_blight -> Early Blight
    Potato___Late_blight -> Late Blight
    Pepper__bell___Bacterial_spot -> Bacterial Spot
    """

    # Split crop and disease
    parts = label.split("___")

    # Disease part is always the last
    disease = parts[-1]

    # Beautify text
    disease = disease.replace("_", " ").title()

    return disease


def extract_crop(label):
    if "___" in label:
        return label.split("___")[0]

    # fallback (if crop missing)
    known_crops = ["Potato", "Tomato", "Pepper", "Corn", "Apple"]

    for crop in known_crops:
        if label.lower().startswith(crop.lower()):
            return crop

    return "Unknown"
