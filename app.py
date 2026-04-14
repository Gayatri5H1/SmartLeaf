from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
import tensorflow as tf

app = Flask(__name__)

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "outputs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOAD MODEL ----------------
print("🔄 Loading model...")
model_path = os.path.join(BASE_DIR, "models", "leaf_mobilenet.h5")
model = tf.keras.models.load_model(model_path, compile=False)
print("✅ Model loaded")

# ---------------- IMPORT MODULES ----------------
from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from recommendation.recommender import get_recommendation

latest_results = []

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/detect")
def detect():
    return render_template("detect.html")

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    global latest_results
    latest_results = []

    files = request.files.getlist("images")

    if not files or files[0].filename == "":
        return "No images uploaded ❌"

    for file in files:
        try:
            print("📥 Processing file:", file.filename)

            filename = str(uuid.uuid4()) + "_" + file.filename
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)

            print("📁 File saved")

            disease, confidence = predict_disease(image_path, model)

            clean_disease = format_disease_label(disease)
            crop = extract_crop(disease)

            severity = "Normal" if disease.lower() == "healthy" else estimate_severity(confidence)

            recommendation = get_recommendation(disease, severity)

            latest_results.append({
                "image": filename,
                "image_path": f"outputs/{filename}",
                "crop": crop,
                "disease": clean_disease,
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "urgency": recommendation["urgency"],
                "chemical": recommendation["chemical"],
                "organic": recommendation["organic"],
                "prevention": recommendation["prevention"]
            })

            print("✅ One image processed")

        except Exception as e:
            print("❌ ERROR:", str(e))
            continue

    if not latest_results:
        return "Processing failed ❌ (Check logs)"

    print("🚀 Redirecting to result page")

    return redirect(url_for("result"))

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template(
        "result.html",
        results=latest_results,
        chemical_heading="Chemical Treatment",
        organic_heading="Organic Treatment",
        prevention_heading="Prevention",
        listen_text="",
        stop_text=""
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
