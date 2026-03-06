import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

IMG_SIZE = 160        # smaller = faster
BATCH_SIZE = 32
EPOCHS = 3            # fast dev training

# -----------------------------
# Data generators
# -----------------------------
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    "dataset/train",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_data = val_gen.flow_from_directory(
    "dataset/val",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

# -----------------------------
# Base model (pretrained AI)
# -----------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

base_model.trainable = False  # VERY IMPORTANT (speed + stability)

# -----------------------------
# Custom classifier
# -----------------------------
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# -----------------------------
# Training
# -----------------------------
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# -----------------------------
# Save model + labels
# -----------------------------
model.save("models/leaf_mobilenet.h5")

labels = {v: k for k, v in train_data.class_indices.items()}
with open("models/class_labels.json", "w") as f:
    json.dump(labels, f, indent=4)

print("✅ MobileNet model trained and saved")
