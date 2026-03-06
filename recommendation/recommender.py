def get_recommendation(disease, severity):
    """
    Full disease-wise agricultural decision support system
    Supports ALL 15 PlantVillage classes
    """

    disease_db = {

        # ===================== PEPPER =====================
        "Pepper__bell___healthy": {
            "chemical": "No chemical treatment required",
            "organic": "Apply compost and biofertilizers",
            "prevention": "Maintain balanced irrigation and soil nutrients"
        },

        "Pepper__bell___Bacterial_spot": {
            "chemical": "Copper hydroxide or streptomycin spray",
            "organic": "Neem oil or turmeric extract spray",
            "prevention": "Use certified seeds and avoid overhead irrigation"
        },

        # ===================== TOMATO =====================
        "Tomato___healthy": {
            "chemical": "No chemical treatment required",
            "organic": "Use vermicompost and organic manure",
            "prevention": "Regular field monitoring"
        },

        "Tomato___Bacterial_spot": {
            "chemical": "Copper-based bactericides",
            "organic": "Neem oil or garlic extract",
            "prevention": "Avoid wet foliage and remove infected leaves"
        },

        "Tomato___Early_blight": {
            "chemical": "Azoxystrobin or Difenoconazole fungicide",
            "organic": "Neem oil spray, mulching",
            "prevention": "Crop rotation and debris removal"
        },

        "Tomato___Late_blight": {
            "chemical": "Mancozeb or Chlorothalonil fungicide",
            "organic": "Baking soda spray, compost tea",
            "prevention": "Destroy infected plants and improve air circulation"
        },

        "Tomato___Leaf_Mold": {
            "chemical": "Copper fungicide or chlorothalonil",
            "organic": "Garlic extract spray",
            "prevention": "Reduce humidity and increase ventilation"
        },

        "Tomato___Septoria_leaf_spot": {
            "chemical": "Chlorothalonil fungicide",
            "organic": "Neem oil spray",
            "prevention": "Remove infected leaves and avoid overhead watering"
        },

        "Tomato___Spider_mites_Two_spotted_spider_mite": {
            "chemical": "Abamectin or bifenthrin",
            "organic": "Neem oil or soap water spray",
            "prevention": "Maintain humidity and regular leaf inspection"
        },

        "Tomato___Target_Spot": {
            "chemical": "Azoxystrobin or Mancozeb",
            "organic": "Neem oil or compost tea",
            "prevention": "Ensure proper spacing and airflow"
        },

        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
            "chemical": "Imidacloprid for whitefly control",
            "organic": "Neem oil spray",
            "prevention": "Control whiteflies and use resistant varieties"
        },

        "Tomato___Tomato_mosaic_virus": {
            "chemical": "No direct chemical cure",
            "organic": "Remove infected plants immediately",
            "prevention": "Disinfect tools and avoid plant handling"
        },

        # ===================== POTATO =====================
        "Potato___healthy": {
            "chemical": "No chemical treatment required",
            "organic": "Apply organic manure",
            "prevention": "Maintain proper soil drainage"
        },

        "Potato___Early_blight": {
            "chemical": "Mancozeb or chlorothalonil",
            "organic": "Neem oil spray",
            "prevention": "Crop rotation and remove infected debris"
        },

        "Potato___Late_blight": {
            "chemical": "Metalaxyl + Mancozeb combination",
            "organic": "Bordeaux mixture (copper-based)",
            "prevention": "Avoid wet conditions and destroy infected tubers"
        }
    }

    # ---------------- FALLBACK (safety) ----------------
    info = disease_db.get(disease, {
        "chemical": "Consult agricultural expert",
        "organic": "Use eco-friendly pest management",
        "prevention": "Maintain crop hygiene"
    })

    # ---------------- SEVERITY INTELLIGENCE ----------------
    urgency_map = {
        "Mild": "Low – Preventive care sufficient",
        "Moderate": "Medium – Treatment recommended",
        "Severe": "High – Immediate action required"
    }

    dosage_map = {
        "Mild": "Apply once every 7–10 days",
        "Moderate": "Apply once every 5–7 days",
        "Severe": "Apply immediately and repeat after 3–5 days"
    }

    return {
        "severity": severity,
        "urgency": urgency_map[severity],
        "chemical": f"{info['chemical']} ({dosage_map[severity]})",
        "organic": f"{info['organic']} ({dosage_map[severity]})",
        "prevention": info["prevention"]
    }
