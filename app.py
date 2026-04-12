from flask import Flask, render_template, request, redirect, url_for
import os
import tensorflow as tf
from monitoring.disease_logger import log_detection

from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from ai.explanations import explain_disease
from recommendation.recommender import get_recommendation
from reports.report_generator import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "static/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = None

def get_model():
    global model
    if model is None:
        print("🚀 Loading model...")
        model = tf.keras.models.load_model("models/leaf_mobilenet.h5", compile=False)
        model.make_predict_function()
    return model

latest_results = []


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- PREDICT ----------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == "GET":
        return redirect(url_for("home"))  # prevent 502 crash

    print("🔥 PREDICT HIT")

    global latest_results
    latest_results = []

    files = request.files.getlist("images")

    if not files or files[0].filename == "":
        return "No images uploaded ❌"

    model_instance = get_model()

    for file in files:
        if file and file.filename != "":

            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            disease, confidence = predict_disease(image_path, model_instance)

            raw_disease = disease
            clean_disease = format_disease_label(raw_disease)
            crop = extract_crop(raw_disease)

            log_detection("Telangana", crop, raw_disease)

            severity = "Normal" if raw_disease.lower() == "healthy" else estimate_severity(confidence)

            recommendation = get_recommendation(raw_disease, severity)
            explanation = explain_disease(raw_disease, severity)

            latest_results.append({
                "image": file.filename,
                "image_path": f"outputs/{file.filename}",
                "crop": crop,
                "disease": clean_disease,
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "urgency": recommendation["urgency"],
                "chemical": recommendation["chemical"],
                "organic": recommendation["organic"],
                "prevention": recommendation["prevention"],
                "explanation": explanation
            })

    return redirect(url_for("result"))


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template("result.html", results=latest_results)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
