import os
import io
import json
from dotenv import load_dotenv
load_dotenv()
import gdown
import numpy as np
import tensorflow as tf
from PIL import Image

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# =========================
# STEP 1: DOWNLOAD MODEL IF MISSING
# =========================
MODEL_PATH = "final_fabric_model_v2.keras"

if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    url = "https://drive.google.com/uc?id=1PgHQOnqVtESMeiqo5VR7N0Foe7eDJWc0"
    gdown.download(url, MODEL_PATH, quiet=False)

# =========================
# STEP 2: LOAD MODEL
# =========================
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully")
print("MODEL OUTPUT SHAPE:", model.output_shape)

# Image size (MATCH TRAINING)
IMG_SIZE = (224, 224)

# =========================
# STEP 3: LOAD CLASS NAMES
# =========================
with open("class_names.json", "r") as f:
    CLASS_NAMES = json.load(f)
    print("CLASS COUNT:", len(CLASS_NAMES))
print("CLASS NAMES:", CLASS_NAMES)

# =========================
# STEP 4: FASTAPI APP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read image sent from react native
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Resize
        image = image.resize(IMG_SIZE)

        # Convert to array
        img_array = np.array(image)

        # MobileNetV2 preprocessing (IMPORTANT)
        img_array = preprocess_input(img_array)

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)

        predicted_class = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        # SAFE CHECK
        if predicted_class >= len(CLASS_NAMES):
            return {
                "success": False,
                "error": f"Invalid class index {predicted_class}",
                "prediction": None,
                "confidence": None,
            }

        label = CLASS_NAMES[predicted_class]

        return {
            "success": True,
            "prediction": label,
            "confidence": confidence,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "prediction": None,
            "confidence": None,
        }
