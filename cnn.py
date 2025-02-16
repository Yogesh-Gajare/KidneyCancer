import os
import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from pdf2image import convert_from_path

app = Flask(__name__)

# Load the pre-trained CNN model
model = tf.keras.models.load_model('kidney_cancer_model.h5')

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow files larger than 16MB (if needed)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to process uploaded image for prediction
def process_image(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))  # Resize to match model input size
    image = np.array(image) / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'dataset' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['dataset']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # If PDF, convert it to image
    if file.filename.endswith('.pdf'):
        images = convert_from_path(filename)
        images[0].save(filename.replace('.pdf', '.jpg'), 'JPEG')
        filename = filename.replace('.pdf', '.jpg')
    
    # If it's an image file, process it directly
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image = process_image(filename)
        prediction = model.predict(image)
        result = np.argmax(prediction, axis=1)[0]
        
        # Assuming 0: 'No Cancer', 1: 'Cancer'
        if result == 0:
            return jsonify({"prediction": "No Cancer"})
        else:
            return jsonify({"prediction": "Cancer"})
    
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
