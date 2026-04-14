import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["OMP_NUM_THREADS"] = "1"
from gtts import gTTS
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for
import uuid
import tensorflow as tf

app = Flask(__name__)

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "outputs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- MODEL (LAZY LOAD) ----------------
model = None
model_path = os.path.join(BASE_DIR, "models", "leaf_mobilenet.h5")

def get_model():
    global model
    if model is None:
        print("🔄 Loading model...")
        model = tf.keras.models.load_model(model_path, compile=False)
        print("✅ Model loaded")
    return model

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

    try:
        files = request.files.getlist("images")

        if not files or files[0].filename == "":
            return "No images uploaded ❌"

        for file in files:
            try:
                print("📥 Processing:", file.filename)

                # Save file
                filename = str(uuid.uuid4()) + "_" + file.filename
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(image_path)

                print("📁 Saved:", image_path)

                # Prediction
                model_instance = get_model()
                disease, confidence = predict_disease(image_path, model_instance)

                clean_disease = format_disease_label(disease)
                crop = extract_crop(disease)

                severity = "Normal" if disease.lower() == "healthy" else estimate_severity(confidence)

                # Recommendation (SAFE)
                try:
                    recommendation = get_recommendation(disease, severity)
                except Exception as e:
                    print("❌ Recommendation Error:", e)
                    recommendation = {
                        "urgency": "Unknown",
                        "chemical": "No data available",
                        "organic": "No data available",
                        "prevention": "No data available"
                    }

                latest_results.append({
                    "image": filename,
                    "image_path": f"outputs/{filename}",
                    "crop": crop,
                    "disease": clean_disease,
                    "confidence": round(confidence * 100, 2),
                    "severity": severity,
                    "urgency": recommendation.get("urgency", "Unknown"),
                    "chemical": recommendation.get("chemical", "No data"),
                    "organic": recommendation.get("organic", "No data"),
                    "prevention": recommendation.get("prevention", "No data")
                })

                print("✅ Processed successfully")

            except Exception as e:
                print("❌ IMAGE ERROR:", str(e))
                return f"Image Error: {str(e)}"   # 🔥 IMPORTANT FIX

        if not latest_results:
            return "Processing failed ❌"

        print("🚀 Redirecting to result page")
        return redirect(url_for("result"))

    except Exception as e:
        print("❌ FULL ERROR:", str(e))
        return f"Server Error: {str(e)}"

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
@app.route("/audio", methods=["POST"])
def audio():
    try:
        data = request.get_json()
        text = data.get("text", "")[:500]  # limit size

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
