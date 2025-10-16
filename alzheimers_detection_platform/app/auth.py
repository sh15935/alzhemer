from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import db from the package
from .database import User  # Import User from database

auth_bp = Blueprint('auth', __name__)

def create_admin_user():
    """Create default admin user if doesn't exist"""
    # Import here to avoid circular imports
    from .database import User

    admin_email = 'admin@neuroscan.ai'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password_hash=generate_password_hash('admin123'),
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Account is deactivated')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        flash('Logged in successfully!')

        # Redirect based on role
        if user.role == 'doctor':
            return redirect(url_for('main.worklist'))
        else:
            return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role', 'patient')

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))