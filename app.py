from flask import Flask, url_for, render_template, redirect, request
import os
import wikipedia
import numpy as np
import tensorflow as tf
from PIL import Image
from numpy import array

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        # Handle the form submission here, if needed
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
    
    # Extract file extension
    _, file_extension = os.path.splitext(file.filename)
    
    # Save the file with a static filename 'image' and the original file extension
    filename = 'image' + file_extension
    file.save(os.path.join('uploads', filename))
    ans = process(os.path.join('uploads', filename))
    disease_list = ['Eczema', 'Melanoma', 'Atopic Dermatitis', 'Basal-cell carcinoma', 'Melanocytic nevus',  'Keratosis', 'Psoriasis', 'Seborrheic keratosis', 'Tinea Corporis', 'Molluscum contagiosum']

    answer = disease_list[ans]
    lead_section = wikipedia.summary(answer)
    # Optionally, you can redirect to another page after successful upload
    return render_template('upload.html', answer = answer, lead_section = lead_section)

def process(image_path):
    model=tf.keras.models.load_model(r'model.h5')
    image_arrays = list(np.asarray(Image.open(image_path).resize((100,75))))
    image_arrays = np.reshape(image_arrays, (-1, 75, 100, 3))  # -1 infers batch size
    a = array(image_arrays)
    a = a.reshape(a.shape[0], *(75, 100, 3))
    x_train_mean = np.mean(a)
    x_train_std = np.std(a)
    a = (a - x_train_mean)/x_train_std

    data = model.predict(a)
    return(np.argmax((data)))
if __name__ == "__main__":
    app.run(debug=True)