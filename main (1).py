import os
import io
import json
from dotenv import load_dotenv
load_dotenv()
import gdown
import numpy as np
from PIL import Image
from ai_edge_litert.interpreter import Interpreter

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# =========================
# STEP 1: DOWNLOAD MODEL IF MISSING
# =========================
MODEL_PATH = "final_fabric_model_v2.tflite"

if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    url = "https://drive.google.com/uc?id=1n80l9g4d1-t0ANC-EqE04vIffJ6V4jro"
    gdown.download(url, MODEL_PATH, quiet=False)

# =========================
# STEP 2: LOAD MODEL (TFLITE)
# =========================
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Model loaded successfully")
print("MODEL OUTPUT SHAPE:", output_details[0]['shape'])

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


def preprocess_input(x: np.ndarray) -> np.ndarray:
    """
    Manual replacement for tf.keras.applications.mobilenet_v2.preprocess_input
    MobileNetV2 preprocessing scales pixels from [0, 255] to [-1, 1]
    """
    x = x.astype(np.float32)
    x = x / 127.5
    x = x - 1.0
    return x


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
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

        # Prediction (TFLITE)
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

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
