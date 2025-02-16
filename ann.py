import os
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

app = Flask(__name__)

# Folder to store uploaded datasets and trained model
UPLOAD_FOLDER = 'uploads/'
MODEL_PATH = 'kidney_model.h5'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to handle model training from the uploaded dataset
@app.route('/upload', methods=['POST'])
def upload_dataset():
    if 'dataset' not in request.files:
        return jsonify({"error": "No dataset part"}), 400
    
    file = request.files['dataset']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Load and preprocess the dataset
    df = pd.read_csv(filename)

    # Assuming the last column is the target variable (kidney disease: 0/1)
    X = df.drop(columns=['kidney_disease'])  # Drop the target column
    y = df['kidney_disease']  # Target variable (0: no disease, 1: disease)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features (important for neural networks)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Build the ANN model
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Sigmoid for binary classification

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    # Save the model for future predictions
    model.save(MODEL_PATH)

    return jsonify({"message": "Model trained successfully!"}), 200

# Route to handle predictions from user input
@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the user
    data = request.json

    # Extract features from the request
    features = np.array([
        data['age'],
        data['blood_pressure'],
        1 if data['albumin'] == 'Low' else 0,
        data['sugar'],
        1 if data['red_blood_cells'] == 'Low' else 0,
        1 if data['pus_cell'] == 'Present' else 0,
        1 if data['bacteria'] == 'Yes' else 0,
        data['blood_glucose'],
        data['serum_creatinine'],
        data['potassium'],
        1 if data['anaemia'] == 'Yes' else 0
    ])

    # Reshape the data into the form expected by the model
    features = features.reshape(1, -1)

    # Load the trained model
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Model is not trained yet."}), 400

    model = load_model(MODEL_PATH)

    # Standardize the input features (same scaler used during training)
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Predict the result (0 = no cancer, 1 = cancer)
    prediction = model.predict(features)
    result = "Cancer" if prediction[0] > 0.5 else "No Cancer"

    return jsonify({"prediction": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
