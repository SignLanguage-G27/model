import os 
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# تحميل الموديل
model_path = "C:\\Users\\Mohab\\Downloads\\Telegram Desktop\\my_model\\my_model.keras" 
if not os.path.exists(model_path): 
    raise FileNotFoundError(f"Model file not found at: {model_path}")

model = load_model(model_path)

# تعريف الفئات
categories = sorted([
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
    "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
    "w", "x", "y", "z"
])

# دالة التنبؤ بالصورة
def predict_image(image_bytes):
    image = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    img = cv2.resize(img, (64, 64)) 
    img = img.reshape(1, 64, 64, 1) 
    img = img / 255.0  

    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    
    return categories[predicted_class], float(prediction[0][predicted_class])


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    label, confidence = predict_image(image_bytes)
    return {"predicted_label": label, "confidence": f"{confidence * 100:.2f}%"}

@app.get("/")
def home():
    return {"message": "API is running! Upload an image to /predict/"}
