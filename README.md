# Fabric App — Backend

FastAPI-based backend for the Fabric App. It provides APIs for fabric classification, image processing, and AI-powered features, connecting the React Native (Expo) frontend with the trained machine learning model.

## Features

* 🔌 **REST API** — connects the React Native frontend to backend services
* 🧵 **Fabric Prediction** — identifies the fabric type from an uploaded image and returns a confidence score
* 🖼️ **Image Processing** — receives and processes uploaded images before prediction
* 🤖 **AI Chatbot** — provides AI-powered assistance using the Groq API
* ⚡ **FastAPI Backend** — lightweight Python API for handling frontend requests and ML inference Show Image
 

## Demo 
(https://github.com/user-attachments/assets/31d20799-9a76-40d9-adda-9d50140cb805)

## Tech Stack

* **Language:** Python
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Machine Learning:** TensorFlow / Keras
* **Model:** MobileNetV2 (Transfer Learning)
* **Image Processing:** PIL, NumPy
* **AI API:** Groq API
* **Model Storage:** Google Drive

## API Endpoints

| Method | Endpoint   | Description                                                                 |
| ------ | ---------- | --------------------------------------------------------------------------- |
| `GET`  | `/`        | Checks whether the backend is running                                       |
| `POST` | `/upload`  | Receives and saves an uploaded image                                        |
| `POST` | `/predict` | Accepts an image and returns the predicted fabric type and confidence score |

## Getting Started

```bash
# Clone the repo
git clone https://github.com/sum123-run/[your-backend-repo-name].git
cd [your-backend-repo-name]

# Install dependencies
pip install -r requirements.txt

# Add environment variables
# Create a .env file with the required API keys

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend will be available locally at:

```text
http://localhost:8000
```

FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

## Environment Variables
```env
GROQ_API_KEY
```
## Model

The Fabric App uses a **MobileNetV2 transfer learning model** for fabric classification.

### Model Details

* **Architecture:** MobileNetV2
* **Approach:** Transfer Learning
* **Input Size:** 224 × 224 pixels
* **Framework:** TensorFlow / Keras
* **Dataset:** The Fabrics Dataset by iBUG
* **Classes:** 23 fabric classes
* **Preprocessing:** MobileNetV2 `preprocess_input`
* **Image Processing:** PIL and NumPy
* **Inference:** The trained model is loaded by the FastAPI backend and used to classify uploaded fabric images.

The model returns:

```json
{
  "success": true,
  "prediction": "fabric_type",
  "confidence": 0.85
}
```

## Backend Structure

```text
fabric-backend/
│
├── main.py
├── requirements.txt
├── class_names.json
├── .env
├── .gitignore
└── README.md
```

>

## Related Repos

* Frontend: https://github.com/sum123-run/fabric-frontend

## License

MIT
