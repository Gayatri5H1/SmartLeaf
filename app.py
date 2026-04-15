import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["OMP_NUM_THREADS"] = "1"

from flask import Flask, render_template, request, redirect, url_for, jsonify
import uuid
import tensorflow as tf
from gtts import gTTS
from googletrans import Translator

app = Flask(__name__)

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "outputs")
AUDIO_FOLDER = os.path.join(BASE_DIR, "static", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ---------------- MODEL ----------------
model = None
model_path = os.path.join(BASE_DIR, "models", "leaf_mobilenet.h5")

def get_model():
    global model
    if model is None:
        model = tf.keras.models.load_model(model_path, compile=False)
    return model

# ---------------- IMPORTS ----------------
from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from recommendation.recommender import get_recommendation

translator = Translator()
latest_results = []

# ---------------- ROUTES ----------------
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

    for index, file in enumerate(files):
        filename = str(uuid.uuid4()) + "_" + file.filename
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)

        model_instance = get_model()
        disease, confidence = predict_disease(image_path, model_instance)

        clean_disease = format_disease_label(disease)
        crop = extract_crop(disease)
        severity = "Normal" if disease.lower() == "healthy" else estimate_severity(confidence)

        try:
            recommendation = get_recommendation(disease, severity)
        except:
            recommendation = {
                "urgency": "Unknown",
                "chemical": "No data",
                "organic": "No data",
                "prevention": "No data"
            }

        chemical = recommendation.get("chemical", "")
        organic = recommendation.get("organic", "")
        prevention = recommendation.get("prevention", "")

        # -------- TRANSLATION --------
        try:
            chemical_hi = translator.translate(chemical, dest="hi").text
            organic_hi = translator.translate(organic, dest="hi").text
            prevention_hi = translator.translate(prevention, dest="hi").text

            chemical_te = translator.translate(chemical, dest="te").text
            organic_te = translator.translate(organic, dest="te").text
            prevention_te = translator.translate(prevention, dest="te").text
        except:
            chemical_hi = chemical
            organic_hi = organic
            prevention_hi = prevention
            chemical_te = chemical
            organic_te = organic
            prevention_te = prevention

        latest_results.append({
            "index": index,
            "image": filename,
            "image_path": f"outputs/{filename}",

            "crop": crop,
            "disease": clean_disease,
            "confidence": round(confidence * 100, 2),
            "severity": severity,
            "urgency": recommendation.get("urgency", "Unknown"),

            "chemical_en": chemical,
            "organic_en": organic,
            "prevention_en": prevention,

            "chemical_hi": chemical_hi,
            "organic_hi": organic_hi,
            "prevention_hi": prevention_hi,

            "chemical_te": chemical_te,
            "organic_te": organic_te,
            "prevention_te": prevention_te,

            "amazon_links": [
                {
                    "name": chemical,
                    "link": f"https://www.amazon.in/s?k={chemical.replace(' ', '+')}"
                }
            ] if chemical else [],

            "store_links": {
                "Agricultural Stores": "https://www.google.com/maps/search/agriculture+store+near+me",
                "Pesticide Shops": "https://www.google.com/maps/search/pesticide+shop+near+me",
                "Fertilizer Stores": "https://www.google.com/maps/search/fertilizer+shop+near+me"
            }
        })

    return redirect(url_for("result"))

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template("result.html", results=latest_results)

# ---------------- AUDIO ----------------
@app.route("/audio", methods=["POST"])
def audio():
    data = request.get_json()
    text = data.get("text", "")[:300]

    filename = f"audio_{abs(hash(text))}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    if not os.path.exists(filepath):
        tts = gTTS(text=text, lang="en")
        tts.save(filepath)

    return jsonify({"audio": f"/static/audio/{filename}"})

# ---------------- REPORT ----------------
@app.route("/download_report/<int:index>")
def download_report(index):
    return "Report feature coming soon 🚀"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
