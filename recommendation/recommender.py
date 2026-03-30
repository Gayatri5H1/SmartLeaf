CHEMICAL_LIST = [
    "Mancozeb",
    "Chlorothalonil",
    "Copper hydroxide",
    "Copper oxychloride",
    "Azoxystrobin",
    "Metalaxyl",
    "Carbendazim",
    "Abamectin",
    "Spiromesifen",
    "Dicofol",
    "Imidacloprid",
    "Thiamethoxam",
    "Acetamiprid"
]

def extract_chemicals(text):
    found = []
    text_lower = text.lower()

    for chem in CHEMICAL_LIST:
        if chem.lower() in text_lower:
            found.append(chem)

    return list(set(found))
def get_recommendation(disease, severity):
    """
    Full disease-wise agricultural decision support system
    Supports ALL 15 PlantVillage classes
    """

    disease_db = {

        # ===================== PEPPER =====================
        "Pepper__bell___healthy": {
            "chemical": "No chemical treatment required. Avoid unnecessary pesticide application to maintain soil health.",
            "organic": "Apply Neem oil (2–3 ml/L) or compost tea once every 10–15 days to maintain plant immunity and overall health."
        },

        "Pepper__bell___Bacterial_spot": {
            "chemical": "Spray copper-based bactericides such as copper hydroxide or copper oxychloride. These can be combined with mancozeb to improve effectiveness. Apply every 7 to 10 days, starting at early stages of infection. Avoid excessive use to prevent leaf damage and resistance.",
            "organic": "Apply neem oil spray regularly to reduce bacterial spread. Use a baking soda solution (1 teaspoon baking soda in 1 liter water with a few drops of mild soap) as a foliar spray. Compost tea and biocontrol agents like Bacillus subtilis can also help suppress the disease. Apply every 5 to 7 days for best results.",
            "prevention": "Use disease-free seeds or seedlings. Maintain proper spacing between plants for good air circulation. Avoid overhead irrigation and prefer drip irrigation to keep leaves dry. Remove and destroy infected plant parts immediately. Practice crop rotation by avoiding peppers or tomatoes in the same field for 2 to 3 years. Apply mulch to reduce soil splashing and avoid working with plants when they are wet."
        },

        # ===================== TOMATO =====================
        "Tomato___healthy": {
            "chemical": "No chemical treatment is required as the plant is healthy. Avoid unnecessary pesticide or fungicide application to prevent resistance and environmental harm.",
            "organic": "Maintain plant health by applying organic compost or vermicompost to enrich soil nutrients. Use neem oil occasionally as a preventive measure against pests. Ensure proper watering and add biofertilizers like Trichoderma or Bacillus subtilis to promote growth.",
        },

        "Tomato___Bacterial_spot": {
            "chemical": "Spray copper-based bactericides such as copper hydroxide or copper oxychloride. These are often combined with mancozeb to enhance effectiveness. Apply every 7 to 10 days, especially during warm and wet conditions. Start application early to control spread and avoid overuse to prevent resistance.",
            "organic": "Use neem oil spray to help reduce bacterial growth and spread. Apply a baking soda solution (1 teaspoon baking soda in 1 liter water with a few drops of mild soap) as a preventive foliar spray. Compost tea and biocontrol agents like Bacillus subtilis can also help suppress the disease. Apply regularly at 5 to 7 day intervals.",
            "prevention": "Use certified disease-free seeds or seedlings. Avoid overhead irrigation and use drip irrigation to keep foliage dry. Maintain proper plant spacing for good air circulation. Remove and destroy infected leaves or plants immediately. Practice crop rotation and avoid planting tomatoes or related crops in the same area for 2 to 3 years. Avoid working with plants when they are wet."
        },

        "Tomato___Early_blight": {
            "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or azoxystrobin to control the disease. Spray at 7 to 10 day intervals, especially during humid conditions. Start treatment at the first sign of infection and ensure thorough coverage of foliage.",
            "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply compost tea or biofungicides containing Trichoderma or Bacillus subtilis to suppress the pathogen. Remove affected leaves and apply organic mulch to reduce soil-borne spores.",
            "prevention": "Use disease-free seeds or resistant varieties. Practice crop rotation by avoiding tomatoes or related crops in the same field for at least 2 to 3 years. Maintain proper spacing for good airflow and avoid overhead watering. Remove and destroy infected plant debris. Apply mulch to prevent soil splash and stake plants to keep foliage off the ground."
        },

        "Tomato___Late_blight": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or metalaxyl-based products to control the disease. Spray at 5 to 7 day intervals during cool and humid conditions. Begin applications at early signs of infection and ensure thorough coverage of leaves and stems.",
    "organic": "Use copper-based fungicides approved for organic farming. Neem oil can help slow disease spread in early stages. Biofungicides containing Bacillus subtilis or Trichoderma may also provide some control when applied regularly.",
    "prevention": "Use certified disease-free seeds or resistant varieties. Avoid overhead irrigation and ensure good drainage. Maintain proper plant spacing for airflow. Remove and destroy infected plants immediately to prevent spread. Practice crop rotation and avoid planting tomatoes or potatoes in the same area for 2 to 3 years. Avoid working with plants when they are wet."
},

        "Tomato___Leaf_Mold": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or copper-based fungicides to control the disease. Spray at 7 to 10 day intervals, especially in humid conditions. Ensure proper coverage on the underside of leaves where the fungus develops.",
    "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply biofungicides containing Bacillus subtilis or Trichoderma to suppress the pathogen. Improve ventilation and reduce humidity to limit disease spread.",
    "prevention": "Ensure good air circulation by proper spacing and pruning. Avoid overhead watering and water at the base of the plant. Grow resistant varieties if available. Remove and destroy infected leaves promptly. Maintain low humidity levels, especially in greenhouses, and avoid working with wet plants."
},

        "Tomato___Septoria_leaf_spot": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or copper-based fungicides to control the disease. Spray at 7 to 10 day intervals, especially during warm and humid conditions. Begin applications at the first sign of infection and ensure thorough coverage of foliage.",
    "organic": "Use neem oil as a preventive spray to reduce fungal spread. Apply biofungicides containing Bacillus subtilis or Trichoderma to suppress the pathogen. Compost tea may also help improve plant resistance when applied regularly.",
    "prevention": "Use disease-free seeds or seedlings. Avoid overhead irrigation and water at the base of the plant. Maintain proper spacing for good air circulation. Remove and destroy infected leaves and plant debris. Apply mulch to reduce soil splash and practice crop rotation by avoiding tomatoes in the same area for 2 to 3 years."
},

        "Tomato___Spider_mites_Two_spotted_spider_mite": {
    "chemical": "Use miticides such as abamectin, spiromesifen, or dicofol to control spider mites. Spray thoroughly on the underside of leaves where mites are present. Repeat applications at 5 to 7 day intervals depending on severity and follow recommended dosage instructions.",
    "organic": "Spray neem oil or insecticidal soap to control mites naturally. A strong water spray can help dislodge mites from leaves. Introduce natural predators like ladybugs or predatory mites to reduce populations. Apply treatments regularly for effective control.",
    "prevention": "Maintain proper watering as dry conditions favor spider mites. Regularly inspect the underside of leaves for early signs of infestation. Keep plants dust-free and healthy. Avoid excessive use of nitrogen fertilizers. Remove heavily infested leaves and maintain good field hygiene."
},

        "Tomato___Target_Spot": {
    "chemical": "Apply fungicides such as chlorothalonil, azoxystrobin, or mancozeb to control the disease. Spray at 7 to 10 day intervals, especially under warm and humid conditions. Ensure thorough coverage of foliage and rotate fungicides to prevent resistance.",
    "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply biofungicides containing Bacillus subtilis or Trichoderma to suppress the pathogen. Compost tea may help improve plant resistance when used regularly.",
    "prevention": "Use disease-free seeds or resistant varieties if available. Maintain proper plant spacing for good air circulation. Avoid overhead irrigation and water at the base of the plant. Remove and destroy infected leaves and crop debris. Practice crop rotation and avoid planting tomatoes in the same area for at least 2 to 3 years."
},

        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
    "chemical": "There is no direct chemical cure for viral diseases. Control the whitefly vectors using insecticides such as imidacloprid, thiamethoxam, or acetamiprid. Apply at recommended intervals to reduce virus spread.",
    "organic": "Use neem oil or insecticidal soap to control whiteflies naturally. Introduce biological control agents like ladybugs or parasitoid wasps. Yellow sticky traps can be used to monitor and reduce whitefly populations.",
    "prevention": "Use virus-resistant tomato varieties and healthy seedlings. Install insect-proof nets or row covers to prevent whitefly entry. Remove and destroy infected plants immediately to stop spread. Maintain field sanitation and control weeds that may host the virus. Avoid planting near previously infected fields."
},
        "Tomato___Tomato_mosaic_virus": {
    "chemical": "There is no chemical cure for viral diseases. Avoid using unnecessary pesticides. Disinfect tools using bleach or alcohol solutions to prevent mechanical transmission of the virus.",
    "organic": "Use neem oil sprays to help control insect vectors like aphids that may spread the virus. Maintain plant health with organic compost and biofertilizers such as Trichoderma or Bacillus subtilis to improve resistance.",
    "prevention": "Use certified virus-free seeds or resistant varieties. Avoid handling plants after using tobacco products, as the virus can spread through contact. Regularly disinfect tools and hands. Remove and destroy infected plants immediately. Control weeds and insect vectors to reduce disease spread."
},

        # ===================== POTATO =====================
        "Potato___healthy": {
            "chemical": "No chemical treatment is required as the plant is healthy. Avoid unnecessary use of pesticides or fungicides to prevent resistance and environmental damage.",
            "organic": "Maintain soil fertility by applying organic compost or well-rotted manure. Use biofertilizers such as Trichoderma or Bacillus subtilis to promote plant growth and root health. Ensure proper irrigation and balanced nutrition.",
        },

        "Potato___Early_blight": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or azoxystrobin to control the disease. Spray at 7 to 10 day intervals, especially during warm and humid conditions. Start applications at the first sign of infection and ensure thorough coverage of foliage.",
    "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply biofungicides containing Trichoderma or Bacillus subtilis to suppress the pathogen. Remove affected leaves and apply organic mulch to reduce soil-borne spores.",
    "prevention": "Use disease-free seed tubers and resistant varieties if available. Practice crop rotation by avoiding potatoes or related crops in the same field for 2 to 3 years. Maintain proper spacing for good air circulation and avoid overhead irrigation. Remove and destroy infected plant debris and keep the field clean."
},

        "Potato___Late_blight": {
    "chemical": "Apply fungicides such as mancozeb, chlorothalonil, or metalaxyl-based products to control the disease. Spray at 5 to 7 day intervals during cool and humid conditions. Begin applications at early signs of infection and ensure thorough coverage of foliage.",
    "organic": "Use copper-based fungicides approved for organic farming. Neem oil may help slow disease spread in early stages. Biofungicides containing Bacillus subtilis or Trichoderma can provide additional protection when applied regularly.",
    "prevention": "Use certified disease-free seed tubers and resistant varieties if available. Avoid overhead irrigation and ensure proper drainage. Maintain adequate plant spacing for airflow. Remove and destroy infected plants immediately to prevent spread. Practice crop rotation and avoid planting potatoes or tomatoes in the same area for 2 to 3 years."
}
    }

    # ---------------- NORMALIZATION FUNCTION ----------------
def get_recommendation(disease, severity):

    disease_db = {

        # ===================== PEPPER =====================
        "Pepper__bell___healthy": {
            "chemical": "No chemical treatment required. Avoid unnecessary pesticide application to maintain soil health.",
            "organic": "Apply Neem oil (2–3 ml/L) or compost tea once every 10–15 days to maintain plant immunity and overall health."
        },

        "Pepper__bell___Bacterial_spot": {
            "chemical": "Spray copper-based bactericides such as copper hydroxide or copper oxychloride. These can be combined with mancozeb to improve effectiveness. Apply every 7 to 10 days, starting at early stages of infection. Avoid excessive use to prevent leaf damage and resistance.",
            "organic": "Apply neem oil spray regularly to reduce bacterial spread. Use a baking soda solution (1 teaspoon baking soda in 1 liter water with a few drops of mild soap) as a foliar spray. Compost tea and biocontrol agents like Bacillus subtilis can also help suppress the disease. Apply every 5 to 7 days for best results.",
            "prevention": "Use disease-free seeds or seedlings. Maintain proper spacing between plants for good air circulation. Avoid overhead irrigation and prefer drip irrigation to keep leaves dry. Remove and destroy infected plant parts immediately. Practice crop rotation by avoiding peppers or tomatoes in the same field for 2 to 3 years. Apply mulch to reduce soil splashing and avoid working with plants when they are wet."
        },

        # ===================== TOMATO =====================
        "Tomato___healthy": {
            "chemical": "No chemical treatment is required as the plant is healthy. Avoid unnecessary pesticide or fungicide application to prevent resistance and environmental harm.",
            "organic": "Maintain plant health by applying organic compost or vermicompost to enrich soil nutrients. Use neem oil occasionally as a preventive measure against pests. Ensure proper watering and add biofertilizers like Trichoderma or Bacillus subtilis to promote growth.",
        },

        "Tomato___Bacterial_spot": {
            "chemical": "Spray copper-based bactericides such as copper hydroxide or copper oxychloride. These are often combined with mancozeb to enhance effectiveness. Apply every 7 to 10 days, especially during warm and wet conditions. Start application early to control spread and avoid overuse to prevent resistance.",
            "organic": "Use neem oil spray to help reduce bacterial growth and spread. Apply a baking soda solution (1 teaspoon baking soda in 1 liter water with a few drops of mild soap) as a preventive foliar spray. Compost tea and biocontrol agents like Bacillus subtilis can also help suppress the disease. Apply regularly at 5 to 7 day intervals.",
            "prevention": "Use certified disease-free seeds or seedlings. Avoid overhead irrigation and use drip irrigation to keep foliage dry. Maintain proper plant spacing for good air circulation. Remove and destroy infected leaves or plants immediately. Practice crop rotation and avoid planting tomatoes or related crops in the same area for 2 to 3 years. Avoid working with plants when they are wet."
        },

        "Tomato___Early_blight": {
            "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or azoxystrobin to control the disease. Spray at 7 to 10 day intervals, especially during humid conditions. Start treatment at the first sign of infection and ensure thorough coverage of foliage.",
            "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply compost tea or biofungicides containing Trichoderma or Bacillus subtilis to suppress the pathogen. Remove affected leaves and apply organic mulch to reduce soil-borne spores.",
            "prevention": "Use disease-free seeds or resistant varieties. Practice crop rotation by avoiding tomatoes or related crops in the same field for at least 2 to 3 years. Maintain proper spacing for good airflow and avoid overhead watering. Remove and destroy infected plant debris. Apply mulch to prevent soil splash and stake plants to keep foliage off the ground."
        },

        "Tomato___Late_blight": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or metalaxyl-based products to control the disease. Spray at 5 to 7 day intervals during cool and humid conditions. Begin applications at early signs of infection and ensure thorough coverage of leaves and stems.",
    "organic": "Use copper-based fungicides approved for organic farming. Neem oil can help slow disease spread in early stages. Biofungicides containing Bacillus subtilis or Trichoderma may also provide some control when applied regularly.",
    "prevention": "Use certified disease-free seeds or resistant varieties. Avoid overhead irrigation and ensure good drainage. Maintain proper plant spacing for airflow. Remove and destroy infected plants immediately to prevent spread. Practice crop rotation and avoid planting tomatoes or potatoes in the same area for 2 to 3 years. Avoid working with plants when they are wet."
},

        "Tomato___Leaf_Mold": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or copper-based fungicides to control the disease. Spray at 7 to 10 day intervals, especially in humid conditions. Ensure proper coverage on the underside of leaves where the fungus develops.",
    "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply biofungicides containing Bacillus subtilis or Trichoderma to suppress the pathogen. Improve ventilation and reduce humidity to limit disease spread.",
    "prevention": "Ensure good air circulation by proper spacing and pruning. Avoid overhead watering and water at the base of the plant. Grow resistant varieties if available. Remove and destroy infected leaves promptly. Maintain low humidity levels, especially in greenhouses, and avoid working with wet plants."
},

        "Tomato___Septoria_leaf_spot": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or copper-based fungicides to control the disease. Spray at 7 to 10 day intervals, especially during warm and humid conditions. Begin applications at the first sign of infection and ensure thorough coverage of foliage.",
    "organic": "Use neem oil as a preventive spray to reduce fungal spread. Apply biofungicides containing Bacillus subtilis or Trichoderma to suppress the pathogen. Compost tea may also help improve plant resistance when applied regularly.",
    "prevention": "Use disease-free seeds or seedlings. Avoid overhead irrigation and water at the base of the plant. Maintain proper spacing for good air circulation. Remove and destroy infected leaves and plant debris. Apply mulch to reduce soil splash and practice crop rotation by avoiding tomatoes in the same area for 2 to 3 years."
},

        "Tomato___Spider_mites_Two_spotted_spider_mite": {
    "chemical": "Use miticides such as abamectin, spiromesifen, or dicofol to control spider mites. Spray thoroughly on the underside of leaves where mites are present. Repeat applications at 5 to 7 day intervals depending on severity and follow recommended dosage instructions.",
    "organic": "Spray neem oil or insecticidal soap to control mites naturally. A strong water spray can help dislodge mites from leaves. Introduce natural predators like ladybugs or predatory mites to reduce populations. Apply treatments regularly for effective control.",
    "prevention": "Maintain proper watering as dry conditions favor spider mites. Regularly inspect the underside of leaves for early signs of infestation. Keep plants dust-free and healthy. Avoid excessive use of nitrogen fertilizers. Remove heavily infested leaves and maintain good field hygiene."
},

        "Tomato___Target_Spot": {
    "chemical": "Apply fungicides such as chlorothalonil, azoxystrobin, or mancozeb to control the disease. Spray at 7 to 10 day intervals, especially under warm and humid conditions. Ensure thorough coverage of foliage and rotate fungicides to prevent resistance.",
    "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply biofungicides containing Bacillus subtilis or Trichoderma to suppress the pathogen. Compost tea may help improve plant resistance when used regularly.",
    "prevention": "Use disease-free seeds or resistant varieties if available. Maintain proper plant spacing for good air circulation. Avoid overhead irrigation and water at the base of the plant. Remove and destroy infected leaves and crop debris. Practice crop rotation and avoid planting tomatoes in the same area for at least 2 to 3 years."
},

        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
    "chemical": "There is no direct chemical cure for viral diseases. Control the whitefly vectors using insecticides such as imidacloprid, thiamethoxam, or acetamiprid. Apply at recommended intervals to reduce virus spread.",
    "organic": "Use neem oil or insecticidal soap to control whiteflies naturally. Introduce biological control agents like ladybugs or parasitoid wasps. Yellow sticky traps can be used to monitor and reduce whitefly populations.",
    "prevention": "Use virus-resistant tomato varieties and healthy seedlings. Install insect-proof nets or row covers to prevent whitefly entry. Remove and destroy infected plants immediately to stop spread. Maintain field sanitation and control weeds that may host the virus. Avoid planting near previously infected fields."
},
        "Tomato___Tomato_mosaic_virus": {
    "chemical": "There is no chemical cure for viral diseases. Avoid using unnecessary pesticides. Disinfect tools using bleach or alcohol solutions to prevent mechanical transmission of the virus.",
    "organic": "Use neem oil sprays to help control insect vectors like aphids that may spread the virus. Maintain plant health with organic compost and biofertilizers such as Trichoderma or Bacillus subtilis to improve resistance.",
    "prevention": "Use certified virus-free seeds or resistant varieties. Avoid handling plants after using tobacco products, as the virus can spread through contact. Regularly disinfect tools and hands. Remove and destroy infected plants immediately. Control weeds and insect vectors to reduce disease spread."
},

        # ===================== POTATO =====================
        "Potato___healthy": {
            "chemical": "No chemical treatment is required as the plant is healthy. Avoid unnecessary use of pesticides or fungicides to prevent resistance and environmental damage.",
            "organic": "Maintain soil fertility by applying organic compost or well-rotted manure. Use biofertilizers such as Trichoderma or Bacillus subtilis to promote plant growth and root health. Ensure proper irrigation and balanced nutrition.",
        },

        "Potato___Early_blight": {
    "chemical": "Apply fungicides such as chlorothalonil, mancozeb, or azoxystrobin to control the disease. Spray at 7 to 10 day intervals, especially during warm and humid conditions. Start applications at the first sign of infection and ensure thorough coverage of foliage.",
    "organic": "Use neem oil as a preventive spray to reduce fungal growth. Apply biofungicides containing Trichoderma or Bacillus subtilis to suppress the pathogen. Remove affected leaves and apply organic mulch to reduce soil-borne spores.",
    "prevention": "Use disease-free seed tubers and resistant varieties if available. Practice crop rotation by avoiding potatoes or related crops in the same field for 2 to 3 years. Maintain proper spacing for good air circulation and avoid overhead irrigation. Remove and destroy infected plant debris and keep the field clean."
},

        "Potato___Late_blight": {
    "chemical": "Apply fungicides such as mancozeb, chlorothalonil, or metalaxyl-based products to control the disease. Spray at 5 to 7 day intervals during cool and humid conditions. Begin applications at early signs of infection and ensure thorough coverage of foliage.",
    "organic": "Use copper-based fungicides approved for organic farming. Neem oil may help slow disease spread in early stages. Biofungicides containing Bacillus subtilis or Trichoderma can provide additional protection when applied regularly.",
    "prevention": "Use certified disease-free seed tubers and resistant varieties if available. Avoid overhead irrigation and ensure proper drainage. Maintain adequate plant spacing for airflow. Remove and destroy infected plants immediately to prevent spread. Practice crop rotation and avoid planting potatoes or tomatoes in the same area for 2 to 3 years."
}
    }

    # ---------------- NORMALIZATION FUNCTION ----------------
    def normalize_disease_name(name):
        import re

        print("RAW:", repr(name))

        name = name.strip().lower()
        name = name.replace("_", " ")   # convert underscores to spaces
        name = re.sub(r'\s+', ' ', name)

        print("CLEANED:", repr(name))

        mapping = {
            "tomato spider mites two spotted spider mite": "Tomato___Spider_mites_Two_spotted_spider_mite",
            "tomato bacterial spot": "Tomato___Bacterial_spot",
            "tomato early blight": "Tomato___Early_blight",
            "tomato late blight": "Tomato___Late_blight",
            "tomato leaf mold": "Tomato___Leaf_Mold",
            "tomato septoria leaf spot": "Tomato___Septoria_leaf_spot",
            "tomato target spot": "Tomato___Target_Spot",
            "tomato yellow leaf curl virus": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "tomato mosaic virus": "Tomato___Tomato_mosaic_virus",
            "tomato healthy": "Tomato___healthy",

            "potato healthy": "Potato___healthy",
            "potato early blight": "Potato___Early_blight",
            "potato late blight": "Potato___Late_blight",

            "pepper bell bacterial spot": "Pepper__bell___Bacterial_spot",
            "pepper bell healthy": "Pepper__bell___healthy"
        }

        # Direct match
        if name in mapping:
            return mapping[name]

        # Partial match
        for key in mapping:
            if key in name:
                print("Matched using partial:", key)
                return mapping[key]

        print("No mapping found")
        return None

    # ---------------- APPLY NORMALIZATION ----------------
    disease_key = normalize_disease_name(disease)
    print("Final key:", disease_key)

    # ---------------- LOOKUP (FIXED 🔥) ----------------
    info = None

    if disease_key is not None:
        for key in disease_db:
            if key.lower() == disease_key.lower():
                info = disease_db[key]
                print("Matched DB key:", key)
                break

    # ---------------- FALLBACK ----------------
    if not info:
        print("Fallback triggered for:", disease_key)
        info = {
            "chemical": "Consult agricultural expert",
            "organic": "Use eco-friendly pest management",
            "prevention": "Maintain crop hygiene"
        }

    # ---------------- SEVERITY ----------------
    urgency_map = {
        "Mild": "Low – Preventive care sufficient",
        "Moderate": "Medium – Treatment recommended",
        "Severe": "High – Immediate action required"
    }

    # ---------------- RETURN ----------------
    chemical_text = info.get("chemical", "")
    if "no chemical" in chemical_text.lower():
        chemical_list = []
    else:
        chemical_list = extract_chemicals(chemical_text)

# 🔥 NEW: extract chemicals
    chemical_list = extract_chemicals(chemical_text)

    return {
    "severity": severity,
    "urgency": urgency_map.get(severity, "Unknown"),

    "chemical": chemical_text,

    # 🔥 ADD THIS
    "chemicals": chemical_list,

    "organic": info.get("organic", ""),
    "prevention": info.get("prevention", "No prevention measures required.")
}