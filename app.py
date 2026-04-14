from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import uuid
import tensorflow as tf
from gtts import gTTS
from googletrans import Translator

# ---------------- INIT ----------------
app = Flask(__name__)
translator = Translator()

# ---------------- PATH FIX ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "outputs")
AUDIO_FOLDER = os.path.join(BASE_DIR, "static", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ---------------- LOAD MODEL (ONLY ONCE ✅) ----------------
model_path = os.path.join(BASE_DIR, "models", "leaf_mobilenet.h5")
model = tf.keras.models.load_model(model_path, compile=False)

# ---------------- IMPORT AI MODULES ----------------
from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from ai.explanations import explain_disease
from recommendation.recommender import get_recommendation
from ai.explainability import generate_gradcam
from monitoring.disease_logger import log_detection
from reports.report_generator import generate_report

latest_results = []

# ---------------- TRANSLATIONS ----------------
translations = {
    "en": {"chemical": "Chemical Treatment", "organic": "Organic Treatment", "prevention": "Prevention", "listen": "Listen", "stop": "Stop"},
    "hi": {"chemical": "रासायनिक उपचार", "organic": "जैविक उपचार", "prevention": "रोकथाम", "listen": "सुनें", "stop": "रोकें"},
    "te": {"chemical": "రసాయన చికిత్స", "organic": "సేంద్రీయ చికిత్స", "prevention": "నివారణ", "listen": "వినండి", "stop": "ఆపండి"}
}

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

# ---------------- PREDICT ----------------
@app.route('/predict', methods=['POST'])
def predict():
    global latest_results
    latest_results = []

    files = request.files.getlist("images")

    if not files or files[0].filename == "":
        return "No images uploaded ❌"

    for file in files:
        if file and file.filename != "":

            # ✅ UNIQUE FILE NAME (FIX)
            filename = str(uuid.uuid4()) + "_" + file.filename
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)

            try:
                # ✅ PASS MODEL (FIX)
                disease, confidence = predict_disease(image_path, model)
            except Exception as e:
                print("Prediction Error:", e)
                continue

            raw_disease = disease
            clean_disease = format_disease_label(raw_disease)
            crop = extract_crop(raw_disease)

            log_detection("India", crop, raw_disease)

            severity = "Normal" if raw_disease.lower() == "healthy" else estimate_severity(confidence)

            recommendation = get_recommendation(raw_disease, severity)
            explanation = explain_disease(raw_disease, severity)

            chemicals = recommendation.get("chemicals", [])

            amazon_links = [
                {
                    "name": chem,
                    "link": f"https://www.amazon.in/s?k={chem.replace(' ', '+')}+pesticide"
                }
                for chem in chemicals
            ] if chemicals else []

            store_links = {
                "Agricultural Stores": "https://www.google.com/maps/search/agriculture+store+near+me",
                "Pesticide Shops": "https://www.google.com/maps/search/pesticide+shop+near+me",
                "Fertilizer Stores": "https://www.google.com/maps/search/fertilizer+shop+near+me"
            }

            # ---------------- GRADCAM ----------------
            gradcam_filename = f"gradcam_{filename}"
            gradcam_output_path = os.path.join("static", "outputs", gradcam_filename)

            try:
                generate_gradcam(image_path=image_path, model=model, output_path=gradcam_output_path)
            except:
                gradcam_filename = None

            # ---------------- AUDIO ----------------
            full_text_en = (
                f"Crop: {crop}\n"
                f"Disease: {clean_disease}\n\n"
                f"Chemical Treatment: {recommendation['chemical']}\n"
                f"Organic Treatment: {recommendation['organic']}\n"
                f"Prevention: {recommendation['prevention']}"
            )

            audio_file = f"{filename}_en.mp3"
            audio_path = os.path.join(AUDIO_FOLDER, audio_file)

            try:
                if not os.path.exists(audio_path):
                    tts = gTTS(text=full_text_en[:1000], lang="en")  # ✅ limit text
                    tts.save(audio_path)
            except:
                audio_file = None

            latest_results.append({
                "image": filename,
                "image_path": f"outputs/{filename}",
                "gradcam": f"outputs/{gradcam_filename}" if gradcam_filename else None,

                "crop": crop,
                "disease": clean_disease,
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "urgency": recommendation["urgency"],

                "chemical_en": recommendation["chemical"],
                "organic_en": recommendation["organic"],
                "prevention_en": recommendation["prevention"],

                "chemical": recommendation["chemical"],
                "organic": recommendation["organic"],
                "prevention": recommendation["prevention"],

                "chemicals": chemicals,
                "amazon_links": amazon_links,
                "store_links": store_links,

                "explanation": explanation,
                "audio_en": f"/static/audio/{audio_file}" if audio_file else None
            })

    if not latest_results:
        return "Processing failed ❌"

    return redirect(url_for("result"))

# ---------------- TRANSLATE ----------------
@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    text_data = data.get("text")
    lang = data.get("lang")

    translated = {}
    for key, value in text_data.items():
        try:
            translated[key] = translator.translate(value, dest=lang).text
        except:
            translated[key] = value  # fallback

    return jsonify(translated)

# ---------------- AUDIO ----------------
@app.route("/audio", methods=["POST"])
def audio():
    data = request.get_json()
    text = data.get("text")[:1000]
    lang = data.get("lang", "en")

    filename = f"audio_{lang}_{abs(hash(text))}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    if not os.path.exists(filepath):
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(filepath)
        except:
            return jsonify({"audio": ""})

    return jsonify({"audio": f"/static/audio/{filename}"})

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template(
        "result.html",
        results=latest_results,
        chemical_heading="Chemical Treatment",
        organic_heading="Organic Treatment",
        prevention_heading="Prevention",
        listen_text="Listen",
        stop_text="Stop"
    )

# ---------------- REPORT ----------------
@app.route("/download_report/<int:index>")
def download_report(index):
    result = latest_results[index]
    report_path = f"static/reports/report_{index}.pdf"
    generate_report(result, report_path)
    return redirect("/" + report_path)

# ---------------- EXPLAIN ----------------
@app.route("/explain")
def explain():
    return render_template("explain.html", results=latest_results)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
