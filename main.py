from flask import Flask, request, jsonify
import os
import uuid

from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
# Initialize Roboflow client
import requests

API_KEY = "ydflWRS9udM9GpC10fEe"
MODEL_ID = "multi-retinal-disease-classifica/1"



@app.route('/')
def home():
    return jsonify({"message": "API is running!"})


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    image_path = "uploaded_image.jpg"
    
    # حفظ الصورة مؤقتًا
    image.save(image_path)

    try:
        # فتح الصورة وإرسالها إلى Roboflow API
        with open(image_path, "rb") as img_file:
            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"
            files = {"file": img_file}
            response = requests.post(url, files=files)
        
        return jsonify(response.json())  # إرسال النتيجة
    
    finally:
        # حذف الملف بعد إغلاقه
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True)
