from flask import Flask, render_template, request, redirect, url_for
import os
import tensorflow as tf

# AI modules
from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from ai.explanations import explain_disease
from recommendation.recommender import get_recommendation
from ai.explainability import generate_gradcam

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = "static/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model once
model = tf.keras.models.load_model("models/leaf_mobilenet.h5")

# Temporary in-memory storage (batch results)
latest_results = []


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- DETECT PAGE (MULTI-IMAGE UPLOAD) ----------------
@app.route("/detect", methods=["GET", "POST"])
def detect():
    global latest_results
    latest_results = []

    if request.method == "POST":
        files = request.files.getlist("images")

        for file in files:
            # Save original image
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            # AI prediction
            disease, confidence = predict_disease(image_path)

            # Severity logic (FIX)
            if disease.lower() == "healthy":
                severity = "Normal"
            else:
                severity = estimate_severity(confidence)

            # Generate Grad-CAM
            gradcam_output_path = os.path.join(
                "static", "outputs", f"gradcam_{file.filename}"
            )

            generate_gradcam(
                image_path=image_path,
                model=model,
                output_path=gradcam_output_path
            )

            # Recommendation logic
            recommendation = get_recommendation(disease, severity)

            # Textual explanation
            explanation = explain_disease(disease, severity)

            latest_results.append({
                "image": file.filename,
                "image_path": f"outputs/{file.filename}",
                "gradcam": f"outputs/gradcam_{file.filename}",
                "crop": extract_crop(disease),
                "disease": format_disease_label(disease),
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "urgency": recommendation["urgency"],
                "chemical": recommendation["chemical"],
                "organic": recommendation["organic"],
                "prevention": recommendation["prevention"],
                "explanation": explanation
            })

        return redirect(url_for("result"))

    return render_template("detect.html")


# ---------------- RESULT PAGE ----------------
@app.route("/result")
def result():
    return render_template("result.html", results=latest_results)


# ---------------- EXPLAINABLE AI PAGE ----------------
@app.route("/explain")
def explain():
    return render_template("explain.html", results=latest_results)


if __name__ == "__main__":
    app.run(debug=True)
