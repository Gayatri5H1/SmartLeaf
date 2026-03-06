import tensorflow as tf
import numpy as np
import cv2
import os


def generate_gradcam(image_path, model, output_path):
    print("[GradCAM] Starting Grad-CAM generation...")

    # Load and preprocess image
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # 🔍 Find last Conv2D layer explicitly
    last_conv_layer = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv_layer = layer.name
            break

    if last_conv_layer is None:
        print("[GradCAM] ❌ No Conv2D layer found")
        return

    print(f"[GradCAM] Using last conv layer: {last_conv_layer}")

    # Build Grad-CAM model
    grad_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=[model.get_layer(last_conv_layer).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)

    if grads is None:
        print("[GradCAM] ❌ Gradients are None")
        return

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap) + 1e-8

    # Load original image (OpenCV)
    original = cv2.imread(image_path)
    original = cv2.resize(original, (160, 160))

    heatmap = cv2.resize(heatmap, (160, 160))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    gradcam = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, gradcam)

    print(f"[GradCAM] ✅ Saved to {output_path}")
