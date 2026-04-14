import json
import numpy as np
import cv2

# ✅ MODEL WILL BE PASSED FROM app.py

# Load class labels
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LABEL_PATH = os.path.join(BASE_DIR, "..", "models", "class_labels.json")

with open(LABEL_PATH) as f:
    class_labels = json.load(f)


def predict_disease(image_path, model):
    print("📸 Reading image:", image_path)

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("❌ Image not loaded properly")

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

    disease_name = class_labels[str(index)]

    print("✅ Prediction done:", disease_name, confidence)

    return disease_name, confidence
