from flask import Flask, request, render_template, jsonify
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Replicate API for Ghibli-style transformation (replace with your API key)
REPLICATE_API_URL = "https://replicate.com/grabielairu/ghibli/versions/4b82bb7dbb3b153882a0c34d7f2cbc4f7012ea7eaddb4f65c257a3403c9b3253"
REPLICATE_MODEL = "your-ghibli-style-model"
REPLICATE_API_TOKEN ="export REPLICATE_API_TOKEN=r8_Ro6PoxMghtEnxeAzHam50GxkgbVG2Jd3A2McI"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Process image
    output_url = process_image(file_path)
    return jsonify({"original": file_path, "processed": output_url})


def process_image(image_path):
    headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
    
    with open(image_path, "rb") as file:
        files = {"file": file}
        response = requests.post(REPLICATE_API_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json().get("output_url")
    return None

if __name__ == '__main__':
    app.run(debug=True)

