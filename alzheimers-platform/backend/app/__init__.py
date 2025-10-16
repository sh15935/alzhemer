from flask import Flask
import os

def create_app():
    # Get absolute paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    print(f"Static directory: {static_dir}")
    print(f"Static exists: {os.path.exists(static_dir)}")

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir,
                static_url_path='/static')

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MODEL_PATH'] = os.path.join('models', 'best_model.h5')

    # Create uploads directory
    uploads_dir = os.path.join(static_dir, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"Uploads directory: {uploads_dir}")
    print(f"Uploads exists: {os.path.exists(uploads_dir)}")

    # Import and initialize model
    from .models import load_model
    load_model(app.config['MODEL_PATH'])

    # Import and register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app