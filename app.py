import os
import uuid
import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

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
        print("Loading model...")
        model = tf.keras.models.load_model(model_path, compile=False)
        print("Model loaded")
    return model

# ---------------- IMPORTS ----------------
from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from recommendation.recommender import get_recommendation

latest_results = []

# ---------------- PRODUCT EXTRACTION (FIXED) ----------------
def extract_products_from_text(text):
    known_products = [
        "mancozeb",
        "chlorothalonil",
        "azoxystrobin",
        "copper hydroxide",
        "copper oxychloride",
        "neem oil",
        "bacillus subtilis",
        "trichoderma"
    ]

    found = []
    text_lower = text.lower()

    for product in known_products:
        if product in text_lower:
            found.append(product.title())

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

    if not files or files[0].filename == "":
        return "No images uploaded"

    for file in files:
        try:
            filename = str(uuid.uuid4()) + "_" + file.filename
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            model = get_model()
            disease, confidence = predict_disease(path, model)

            clean_disease = format_disease_label(disease)
            crop = extract_crop(disease)

            severity = "Normal" if disease.lower() == "healthy" else estimate_severity(confidence)

            recommendation = get_recommendation(disease, severity)

            # ✅ EXTRACT PRODUCTS CORRECTLY
            products = extract_products_from_text(recommendation["chemical"])

            amazon_links = [
                {
                    "name": p,
                    "link": f"https://www.amazon.in/s?k={p.replace(' ', '+')}"
                }
                for p in products
            ]

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
                "prevention": recommendation["prevention"],
                "amazon_links": amazon_links
            })

        except Exception as e:
            print("ERROR:", e)

    return redirect(url_for("result"))

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template("result.html", results=latest_results)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
