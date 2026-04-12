from flask import Flask, render_template, request, redirect, url_for
import os
import tensorflow as tf
from monitoring.disease_logger import log_detection

# AI modules
from ai.label_formatter import format_disease_label, extract_crop
from ai.predictor import predict_disease
from ai.severity import estimate_severity
from ai.explanations import explain_disease
from recommendation.recommender import get_recommendation
from reports.report_generator import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "static/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ LAZY LOAD MODEL (IMPORTANT)
model = None

def get_model():
    global model
    if model is None:
        print("🚀 Loading model...")
        model = tf.keras.models.load_model("models/leaf_mobilenet.h5", compile=False)
        model.make_predict_function()
    return model


latest_results = []

translations = {
    "en": {
        "chemical": "Chemical Treatment",
        "organic": "Organic Treatment",
        "prevention": "Prevention",
        "listen": "Listen",
        "stop": "Stop"
    }
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

    # ✅ Load model only when needed
    model_instance = get_model()

    for file in files:
        if file and file.filename != "":

            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            # ✅ Pass model here
            disease, confidence = predict_disease(image_path, model_instance)

            raw_disease = disease
            clean_disease = format_disease_label(raw_disease)

            crop = extract_crop(raw_disease)

            log_detection("Telangana", crop, raw_disease)

            if raw_disease.lower() == "healthy":
                severity = "Normal"
            else:
                severity = estimate_severity(confidence)

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
                "Agricultural Supply Stores": "https://www.google.com/maps/search/agriculture+store+near+me",
                "Pesticide Shops": "https://www.google.com/maps/search/pesticide+shop+near+me",
                "Fertilizer Stores": "https://www.google.com/maps/search/fertilizer+shop+near+me",
                "Government Agri Centers": "https://www.google.com/maps/search/krishi+vigyan+kendra+near+me"
            }

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

                "chemicals": chemicals,
                "amazon_links": amazon_links,
                "store_links": store_links,

                "explanation": explanation
            })

    if len(latest_results) == 0:
        return "Processing failed ❌"

    return redirect(url_for("result"))


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    text_labels = translations["en"]

    return render_template(
        "result.html",
        results=latest_results,

        chemical_heading=text_labels["chemical"],
        organic_heading=text_labels["organic"],
        prevention_heading=text_labels["prevention"],
        listen_text=text_labels["listen"],
        stop_text=text_labels["stop"],
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
