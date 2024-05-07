from flask import Flask, url_for, render_template, redirect, request
import os
import wikipedia
import numpy as np
import tensorflow as tf
from PIL import Image
from numpy import array
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        pass
    return render_template('testing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/upload', methods = ['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part"
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file"


    if file.mimetype.startswith('image'):
        # Read the image file from memory
        image_stream = BytesIO()
        file.save(image_stream)
        image_stream.seek(0)  # Rewind the stream to the beginning
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(image_stream)

    ans = process(image)
    processed_image = image_to_base64(image)

    disease_list = ['Eczema', 'Melanoma', 'Atopic Dermatitis', 'Basal-cell carcinoma', 'Melanocytic nevus',  'Keratosis', 'Psoriasis', 'Seborrheic keratosis', 'Tinea Corporis', 'Molluscum contagiosum']

    answer = disease_list[ans]
    lead_section = wikipedia.summary(answer)
    return render_template('upload.html', answer = answer, lead_section = lead_section, img = processed_image, file_extension = file_extension)

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Change the format
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_image

def process(img):
    model=tf.keras.models.load_model(r'model.h5')
    image_arrays = list(np.asarray(img.resize((100,75))))
    image_arrays = np.reshape(image_arrays, (-1, 75, 100, 3))
    a = array(image_arrays)
    a = a.reshape(a.shape[0], *(75, 100, 3))
    x_train_mean = np.mean(a)
    x_train_std = np.std(a)
    a = (a - x_train_mean)/x_train_std

    data = model.predict(a)
    return(np.argmax((data)))

if __name__ == "__main__":
    app.run(debug=True)