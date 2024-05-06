from flask import Flask, url_for, render_template, redirect, request
import os
import wikipedia
import random

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

    disease_list = ['Melanoma', 'Melanocytic nevus', 'Basal-cell carcinoma', 'Actinic keratosis', 'Seborrheic keratosis', 'Dermatofibroma', 'Hemangioma', 'Squamous-cell carcinoma']

    answer = random.choice(disease_list)
    lead_section = wikipedia.summary(answer)
    # Optionally, you can redirect to another page after successful upload
    return render_template('upload.html', answer = answer, lead_section = lead_section)


if __name__ == "__main__":
    app.run(debug=True)