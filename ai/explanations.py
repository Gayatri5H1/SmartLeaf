def explain_disease(disease, severity):

    explanations = {

        # ================= PEPPER =================
        "Pepper__bell___healthy":
        "The leaf shows uniform green coloration with no visible spots or texture irregularities. "
        "This indicates normal chlorophyll activity and healthy cellular structure. "
        "Grad-CAM does not focus on any specific region because no disease patterns are present.",

        "Pepper__bell___Bacterial_spot":
        "Bacterial spot creates small, dark, water-soaked lesions that often appear scattered. "
        "The bacteria invade leaf tissue through pores, causing localized cell death. "
        "Grad-CAM highlights multiple small regions where bacterial damage disrupts leaf texture.",

        # ================= TOMATO =================
        "Tomato___healthy":
        "The tomato leaf displays consistent color and vein structure. "
        "There are no distortions or abnormal patterns, indicating healthy photosynthesis. "
        "Grad-CAM shows diffuse attention without concentrated disease regions.",

        "Tomato___Early_blight":
        "Early blight produces circular brown lesions with concentric rings, often starting on older leaves. "
        "The disease slowly spreads by weakening leaf tissue. "
        "Grad-CAM highlights ring-shaped regions corresponding to early lesion development.",

        "Tomato___Late_blight":
        "Late blight is an aggressive disease that causes large, irregular dark patches. "
        "It rapidly destroys leaf tissue by blocking nutrient and water movement. "
        "Grad-CAM focuses on broad connected regions, indicating fast-spreading infection.",

        "Tomato___Leaf_Mold":
        "Leaf mold develops mainly on the underside of leaves in humid environments. "
        "It alters leaf surface texture rather than creating clear spots. "
        "Grad-CAM highlights textured regions where mold growth changes leaf structure.",

        "Tomato___Septoria_leaf_spot":
        "Septoria leaf spot causes many small, circular lesions with defined borders. "
        "These lesions reduce the leaf’s functional area. "
        "Grad-CAM highlights numerous tiny regions reflecting widespread spot distribution.",

        "Tomato___Spider_mites_Two_spotted_spider_mite":
        "Spider mites damage leaves by sucking out plant fluids, leaving fine speckled patterns. "
        "This leads to gradual leaf drying. "
        "Grad-CAM highlights fine-grained speckled regions rather than large patches.",

        "Tomato___Target_Spot":
        "Target spot produces brown lesions with a target-like appearance and layered rings. "
        "The fungal infection expands outward from the center. "
        "Grad-CAM highlights concentric circular regions aligned with lesion growth.",

        "Tomato___Tomato_Yellow_Leaf_Curl_Virus":
        "This viral disease causes upward curling and yellowing of leaves. "
        "It disrupts normal leaf development rather than creating spots. "
        "Grad-CAM focuses on distorted leaf edges and vein regions.",

        "Tomato___Tomato_mosaic_virus":
        "Tomato mosaic virus causes irregular light and dark green mottling. "
        "The virus interferes with chlorophyll production. "
        "Grad-CAM highlights color-variant regions across the leaf surface.",

        # ================= POTATO =================
        "Potato___healthy":
        "The potato leaf shows normal shape, color, and texture. "
        "No disease-related patterns are detected. "
        "Grad-CAM attention remains evenly distributed.",

        "Potato___Early_blight":
        "Early blight in potatoes forms dark circular lesions with concentric rings. "
        "The disease progresses gradually, reducing leaf efficiency. "
        "Grad-CAM highlights ring-patterned regions associated with early tissue damage.",

        "Potato___Late_blight":
        "Late blight causes rapid tissue collapse, producing large darkened areas. "
        "The infection spreads quickly in moist conditions. "
        "Grad-CAM highlights extensive regions where severe tissue destruction occurs."
    }

    base = explanations.get(
        disease,
        "The AI detected abnormal visual patterns indicating disease-related damage. "
        "Grad-CAM highlights regions that contributed most to the prediction."
    )

    severity_note = {
        "Mild": "The disease appears to be in an early stage with limited spread.",
        "Moderate": "The disease is actively spreading and requires timely treatment.",
        "Severe": "The disease is widespread and may significantly impact crop yield."
    }

    return base + " " + severity_note[severity]
