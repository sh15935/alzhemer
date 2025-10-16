from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import predict_image

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error='No file selected')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Make prediction
        prediction = predict_image(filepath)

        return render_template('index.html',
                              prediction=prediction,
                              img_path=f"uploads/{filename}")

    return render_template('index.html', error='Error processing file')