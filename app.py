from flask import Flask, request, render_template, url_for, flash, redirect
from lung_cancer_model import predict_cancer
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = '123'  # Secret key for session management

# Directory to save uploaded images (optional)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Define the filename
            filename = file.filename
            
            # Save file to the uploads directory
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # Run the prediction function
            result = predict_cancer(save_path)

            # Create the path for the image to be displayed in the HTML
            image_path = url_for('static', filename='uploads/' + filename)

            # Render the result template with the prediction result and image path
            return render_template('result.html', prediction=result, image_path=image_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
