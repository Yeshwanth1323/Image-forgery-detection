from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from ela import convert_to_ela_image
from prediction import prepare_image, predict_ela_image



# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limit upload size to 5MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Ensure upload and static folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        flash('No file part in the form.')
        return redirect(request.url)

    file = request.files['image']
    if file.filename == '':
        flash('No file selected.')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            ela_image_path = os.path.join('static', 'ela_image.jpg')
            convert_to_ela_image(filepath, ela_image_path)

            image = prepare_image(ela_image_path)
            result = predict_ela_image(image)

            return render_template('result.html', result=result)

        except Exception as e:
            app.logger.error(f"Error processing image: {e}")
            flash("An error occurred while processing the image.")
            return redirect(url_for('index'))

    else:
        flash("Invalid file type. Please upload a .jpg or .jpeg image.")
        return redirect(url_for('index'))

# Proper main entry point
if __name__ == '__main__':
    app.run(debug=True)
