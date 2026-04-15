import os
import uuid
import tensorflow as tf
import re

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from gtts import gTTS
from googletrans import Translator

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

# ---------------- PRODUCT EXTRACTION ----------------
def extract_products(text):
    known = [
        "mancozeb","chlorothalonil","azoxystrobin",
        "copper hydroxide","copper oxychloride",
        "neem oil","bacillus subtilis","trichoderma"
    ]

    found = []
    for k in known:
        if k in text.lower():
            found.append(k.title())
    return found

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

    for index, file in enumerate(files):

        filename = str(uuid.uuid4()) + "_" + file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        model = get_model()
        disease, confidence = predict_disease(path, model)

        clean_disease = format_disease_label(disease)
        crop = extract_crop(disease)
        severity = "Normal" if disease.lower()=="healthy" else estimate_severity(confidence)

        rec = get_recommendation(disease, severity)

        chemical = rec.get("chemical","")
        organic = rec.get("organic","")
        prevention = rec.get("prevention","")

        # PRODUCT EXTRACTION
        products = extract_products(chemical)
        amazon_links = [
            {"name": p, "link": f"https://www.amazon.in/s?k={p.replace(' ','+')}"} 
            for p in products
        ]

        # STORE LINKS
        store_links = {
            "Agricultural Stores": "https://www.google.com/maps/search/agriculture+store+near+me",
            "Pesticide Shops": "https://www.google.com/maps/search/pesticide+shop+near+me",
            "Fertilizer Stores": "https://www.google.com/maps/search/fertilizer+shop+near+me",
            "Government Agri Centers": "https://www.google.com/maps/search/government+agriculture+office+near+me"
        }

        latest_results.append({
            "index": index,
            "image": filename,
            "image_path": f"outputs/{filename}",
            "crop": crop,
            "disease": clean_disease,
            "confidence": round(confidence*100,2),
            "severity": severity,
            "urgency": rec.get("urgency",""),

            "chemical": chemical,
            "organic": organic,
            "prevention": prevention,

            # ✅ IMPORTANT FIXES
            "chemical_en": chemical,
            "organic_en": organic,
            "prevention_en": prevention,

            "amazon_links": amazon_links,
            "store_links": store_links
        })

    return redirect(url_for("result"))

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template(
        "result.html",
        results=latest_results,

        # ✅ REQUIRED VARIABLES
        chemical_heading="Chemical Treatment",
        organic_heading="Organic Treatment",
        prevention_heading="Prevention",
        listen_text="Listen",
        stop_text="Stop"
    )

# ---------------- AUDIO ----------------
@app.route("/audio", methods=["POST"])
def audio():
    data = request.json
    text = data["text"]

    file_path = os.path.join(AUDIO_FOLDER, "audio.mp3")
    gTTS(text).save(file_path)

    return jsonify({"audio": "/static/audio/audio.mp3"})

# ---------------- TRANSLATE ----------------
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json

    text_data = data["text"]  # dict now

    translated = {}
    for key in text_data:
        translated[key] = translator.translate(text_data[key], dest=data["lang"]).text

    return jsonify(translated)

# ---------------- DOWNLOAD REPORT ----------------
@app.route("/download_report/<int:index>")
def download(index):
    r = latest_results[index]

    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"Crop: {r['crop']}", styles["Normal"]),
        Paragraph(f"Disease: {r['disease']}", styles["Normal"]),
        Paragraph(f"Chemical: {r['chemical']}", styles["Normal"]),
        Paragraph(f"Organic: {r['organic']}", styles["Normal"]),
        Paragraph(f"Prevention: {r['prevention']}", styles["Normal"])
    ]

    doc.build(content)
    return send_file(file_path, as_attachment=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
