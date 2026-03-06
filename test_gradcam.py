import tensorflow as tf
from ai.explainability import generate_gradcam

model = tf.keras.models.load_model("models/leaf_mobilenet.h5")

input_image = r"C:\Users\lenovo\Desktop\SmartLeaf\dataset\train\Pepper__bell___healthy\0a3f2927-4410-46a3-bfda-5f4769a5aaf8___JR_HL 8275.JPG"
output_image = "gradcam_result.jpg"

generate_gradcam(
    image_path=input_image,
    model=model,
    last_conv_layer_name="Conv_1",
    output_path=output_image
)

print("Grad-CAM image generated:", output_image)
