from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import certifi

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB client setup
client = MongoClient(
    "mongodb+srv://aruneshfelix:5799@skin-lesion-detection.3igty.mongodb.net/?retryWrites=true&w=majority&appName=Skin-Lesion-Detection",
    tlsCAFile=certifi.where()
)
db = client['derma_app']
users = db['users']

# Define class names for predictions
verbose_name = {
    0: 'Actinic Keratosis',
    1: 'Basal Cell Carcinoma',
    2: 'Benign keratosis-like lesions',
    3: 'Dermatofibroma',
    4: 'Nevus',
    5: 'Vascular Lesion',
    6: 'Melanoma',
}

# Lazy model loading to save memory
model = None

def load_skin_model():
    global model
    if model is None:
        dependencies = {'auc_roc': tf.keras.metrics.AUC}
        model = load_model('model/skin.h5', custom_objects=dependencies)
    return model

# Function to preprocess image and predict label
def predict_label(img_path):
    model = load_skin_model()
    try:
        test_image = image.load_img(img_path, target_size=(28, 28))  # Resize to the model input size
        test_image = image.img_to_array(test_image) / 255.0  # Normalize the image
        test_image = np.expand_dims(test_image, axis=0)  # Reshape to fit model input

        predictions = model.predict(test_image)
        predicted_class = np.argmax(predictions, axis=1)[0]
        return verbose_name[predicted_class]
    except Exception as e:
        return f"Error in prediction: {str(e)}"

# Routes for user authentication
@app.route("/signup", methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if users.find_one({"email": email}):
        flash("Email already exists. Please log in.", "error")
        return redirect(url_for('login_page'))

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for('login_page'))

    hashed_password = generate_password_hash(password)
    users.insert_one({
        "name" : name,
        "email": email,
        "password": hashed_password
    })    
    return redirect(url_for('register_success'))

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = users.find_one({"email": email})

    if user and check_password_hash(user['password'], password):
        session['user_email'] = email
        session['user_name'] = user['name']
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login_page'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('first'))

# Routes for skin cancer prediction functionality

@app.route("/")
@app.route("/first")
def first():
    return render_template('first.html')

@app.route("/login_page")
def login_page():
    return render_template('login.html')

@app.route("/register_success")
def register_success():
    return render_template('register_success.html')

@app.route("/index", methods=['GET', 'POST'])

@app.route("/index", methods=['GET', 'POST'])
def index():
    if 'user_name' in session:
        return render_template("index.html", user_name=session['user_name'])
    else:
        return redirect(url_for('first'))

@app.route("/submit", methods=['POST'])
def get_output():
    if request.method == 'POST':
        if 'my_image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        img = request.files['my_image']

        if img.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if img:
            # Save image to the static folder
            img_path = os.path.join('static/tests/', img.filename)
            img.save(img_path)
            print(img_path)

            # Get prediction
            prediction_result = predict_label(img_path)

            return render_template("prediction.html", prediction=prediction_result, img_path=img_path , user_name=session['user_name'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable if available
    app.run(debug=True, host='0.0.0.0', port=port)
