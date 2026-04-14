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
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- MODEL ----------------
model = None
model_path = os.path.join(BASE_DIR, "models", "leaf_mobilenet.h5")

def get_model():
    global model
    if model is None:
        print("🔄 Loading model...")
        model = tf.keras.models.load_model(model_path, compile=False)
        print("✅ Model loaded")
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

    try:
        files = request.files.getlist("images")

        if not files or files[0].filename == "":
            return "No images uploaded ❌"

        for file in files:
            try:
                # ✅ FIX: correct filename
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
                        "chemical": "No data available",
                        "organic": "No data available",
                        "prevention": "No data available"
                    }

                # ✅ SAFE TEXT
                chemical = recommendation.get("chemical", "")
                organic = recommendation.get("organic", "")
                prevention = recommendation.get("prevention", "")

                # ✅ TRANSLATION (safe)
                try:
                    chemical_hi = translator.translate(chemical, dest="hi").text
                    organic_hi = translator.translate(organic, dest="hi").text
                    prevention_hi = translator.translate(prevention, dest="hi").text
                except:
                    chemical_hi = chemical
                    organic_hi = organic
                    prevention_hi = prevention

                latest_results.append({
                    "image": filename,
                    "image_path": f"outputs/{filename}",

                    # Prediction tab
                    "crop": crop,
                    "disease": clean_disease,
                    "confidence": round(confidence * 100, 2),
                    "severity": severity,
                    "urgency": recommendation.get("urgency", "Unknown"),

                    # Treatment tab
                    "chemical_en": chemical,
                    "organic_en": organic,
                    "prevention_en": prevention,

                    "chemical_hi": chemical_hi,
                    "organic_hi": organic_hi,
                    "prevention_hi": prevention_hi,

                    # Audio
                    "audio": "",

                    # Actions tab
                    "amazon_links": [
                        {
                            "name": chemical,
                            "link": f"https://www.amazon.in/s?k={chemical.replace(' ', '+')}"
                        }
                    ] if chemical else [],

                    "store_links": {
                        "Agricultural Supply Stores": "https://www.google.com/maps/search/agriculture+store+near+me",
                        "Pesticide Shops": "https://www.google.com/maps/search/pesticide+shop+near+me",
                        "Fertilizer Stores": "https://www.google.com/maps/search/fertilizer+shop+near+me",
                        "Government Agri Centers": "https://www.google.com/maps/search/agriculture+office+near+me"
                    }
                })

            except Exception as e:
                print("❌ Image Error:", str(e))
                continue

        if not latest_results:
            return "Processing failed ❌"

        return redirect(url_for("result"))

    except Exception as e:
        return f"Server Error: {str(e)}"

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template("result.html", results=latest_results)

# ---------------- AUDIO ----------------
@app.route("/audio", methods=["POST"])
def audio():
    try:
        data = request.get_json()
        text = data.get("text", "")[:300]

        filename = f"audio_{abs(hash(text))}.mp3"
        filepath = os.path.join("static", filename)

        if not os.path.exists(filepath):
            tts = gTTS(text=text, lang="en")
            tts.save(filepath)

        return jsonify({"audio": "/" + filepath})

    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
