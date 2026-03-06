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
    """
    Extracts crop name from label.

    Pepper__bell___Bacterial_spot -> Pepper Bell
    Tomato___Early_blight -> Tomato
    """

    crop = label.split("___")[0]
    crop = crop.replace("_", " ").title()

    return crop
