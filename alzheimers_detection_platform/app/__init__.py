from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from .routes import main_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Load ML model
    from .models import load_model
    app.config['MODEL_PATH'] = os.path.join('models', 'best_model.h5')
    load_model(app.config['MODEL_PATH'])

    # Setup database
    with app.app_context():
        # Import models
        from .database import User, Patient, Intake

        # Create tables
        db.create_all()

        # Create admin user
        from .auth import create_admin_user
        create_admin_user()

        # Setup user loader
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app