from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(20))  # patient, doctor, nurse, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    preferred_language = db.Column(db.String(10), default='en')

    def __repr__(self):
        return f'<User {self.email}>'

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(50), unique=True)  # Medical Record Number
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_phone = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(100))
    preferred_language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Intake(db.Model):
    __tablename__ = 'intakes'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='draft')  # draft, submitted, reviewed
    consent_given = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)

    # Symptoms and history (stored as JSON for flexibility)
    symptoms = db.Column(db.JSON)
    medical_history = db.Column(db.JSON)
    cognitive_tests = db.Column(db.JSON)

    # AI prediction results
    ai_prediction = db.Column(db.JSON)
    ai_confidence = db.Column(db.Float)

    # Doctor review
    doctor_notes = db.Column(db.Text)
    final_assessment = db.Column(db.String(50))  # normal, mci, alzheimers, other
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)

    patient = db.relationship('Patient', backref='intakes')
    creator = db.relationship('User', foreign_keys=[created_by])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])