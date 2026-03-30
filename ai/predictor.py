import json
import numpy as np
import tensorflow as tf
import cv2

# Load trained model
model = tf.keras.models.load_model("models/leaf_mobilenet.h5", compile=False)
# Load class labels
with open("models/class_labels.json") as f:
    class_labels = json.load(f)

def predict_disease(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (160, 160))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)[0]
    index = int(np.argmax(predictions))
    confidence = float(predictions[index])

    disease_name = class_labels[str(index)]
    return disease_name, confidence
