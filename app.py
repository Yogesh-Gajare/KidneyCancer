
import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename

# Constants
IMG_SIZE = (128, 128)
MODEL_PATH = "kidney_cancer_model.h5"
UPLOAD_FOLDER = "uploads/"
CSV_PATH = "kidneyData_filtered.csv"  # Path to CSV dataset

# Load Model & Dataset
model = load_model(MODEL_PATH)
df = pd.read_csv(CSV_PATH)  # Load the database

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def predict_image(image):
    # Resize and process the image for the model
    img = image.resize(IMG_SIZE)
    img_array = img_to_array(img) / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict the class using the model
    prediction = model.predict(img_array)
    class_names = ["Normal", "Tumor",]  # Define your classes here
    predicted_class = class_names[np.argmax(prediction)]  # Get the predicted class

    # Fetch additional information from the CSV dataset
    if predicted_class in df['Class'].values:
        # Get the row that matches the predicted class
        info = df[df['Class'] == predicted_class].iloc[0].to_dict()

        # Remove unwanted fields from the info dictionary
        unwanted_fields = ['Unnamed: 0', 'full_path', 'image_id', 'path', 'target']
        for field in unwanted_fields:
            if field in info:
                del info[field]  # Delete unwanted field from the dictionary

    else:
        info = {"Note": "No extra info available in database"}

    return {"class": predicted_class, "database_info": info}

# Web Interface
@app.route('/')
def index():
    return render_template('cnnprediction.html')

@app.route('/cnnprediction')
def cnnprediction():
    return render_template('cnnprediction.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')  # Ensure this matches your actual upload page file name

@app.route('/open')
def open():
    return render_template('open.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/annpredict')
def annpredict():
    return render_template('annpredict.html')



@app.route('/predict', methods=['POST'])
def predict():
    # Get the base64 image from the form data
    base64_image = request.form.get('image')
    
    if not base64_image:
        return jsonify({"error": "No image data provided"}), 400
    
    try:
        # Decode the base64 string to image
        image_data = base64.b64decode(base64_image.split(',')[1])  # Skip the "data:image/png;base64,"
        image = Image.open(BytesIO(image_data))

        # Process the image using the prediction logic
        result = predict_image(image)

        # Return the prediction and database information
        return jsonify({
            "prediction": result["class"],
            "database_info": result["database_info"]
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": "Prediction failed"}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


