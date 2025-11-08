from extensions import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app import db
from datetime import date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))  # admin, doctor, patient

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)

class DoctorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    specialization = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    availability = db.Column(db.String(50), nullable=False)

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    contact = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)  # Date of Birth


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    status = db.Column(db.String(20), default='Booked')

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)

class DoctorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    # Relationship to availability
    availabilities = db.relationship('DoctorAvailability', backref='doctor', cascade="all, delete-orphan")

class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # e.g., Monday
    start_time = db.Column(db.String(5), nullable=False)    # e.g., 09:00
    end_time = db.Column(db.String(5), nullable=False)      # e.g., 13:00

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50))
    age = db.Column(db.Integer)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Booked")
    
    doctor = db.relationship('DoctorProfile')
    patient = db.relationship('PatientProfile')
