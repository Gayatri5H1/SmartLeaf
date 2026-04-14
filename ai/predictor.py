import json
import numpy as np
import cv2
import os

# ---------------- PATH FIX ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go to project root safely
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

LABEL_PATH = os.path.join(ROOT_DIR, "models", "class_labels.json")

print("📁 Loading labels from:", LABEL_PATH)

# ---------------- LOAD LABELS ----------------
if not os.path.exists(LABEL_PATH):
    raise FileNotFoundError(f"❌ Labels file not found at {LABEL_PATH}")

with open(LABEL_PATH) as f:
    class_labels = json.load(f)

print("✅ Labels loaded successfully")

# ---------------- PREDICTION FUNCTION ----------------
def predict_disease(image_path, model):
    print("📸 Reading image:", image_path)

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("❌ Image not loaded properly")

    # Preprocessing
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (160, 160))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    print("🧠 Running model prediction...")

    predictions = model.predict(img)

    if predictions is None or len(predictions) == 0:
        raise ValueError("❌ Model returned empty predictions")

    predictions = predictions[0]

    index = int(np.argmax(predictions))
    confidence = float(predictions[index])

    # Safety check
    if str(index) not in class_labels:
        raise KeyError(f"❌ Class index {index} not found in labels")

    disease_name = class_labels.get(str(index), "Unknown Disease")

    print("✅ Prediction done:", disease_name, confidence)

    return disease_name, confidence
