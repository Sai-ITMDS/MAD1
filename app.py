from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# ------------------ Flask App ------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ Login Manager ------------------
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# ------------------ Models ------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50))  # 'admin' only for now

class DoctorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    specialization = db.Column(db.String(150))
    availability = db.Column(db.String(50), nullable=False)

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    contact = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Booked')

# ------------------ User Loader ------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ Routes ------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ------------------ Login/Logout ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ------------------ Admin Dashboard ------------------
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    doctors = DoctorProfile.query.all()
    patients = PatientProfile.query.all()
    appointments = Appointment.query.all()
    return render_template('admin_dashboard.html', doctors=doctors, patients=patients, appointments=appointments)

# ------------------ DOCTORS CRUD ------------------
@app.route('/admin/doctor/manage')
@login_required
def manage_doctors():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    doctors = DoctorProfile.query.all()
    return render_template('manage_doctors.html', doctors=doctors)

@app.route('/admin/doctor/add', methods=['POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    name = request.form['name']
    specialization = request.form['specialization']
    availability = request.form['availability']  
    doctor = DoctorProfile(name=name, specialization=specialization, availability=availability)
    db.session.add(doctor)
    db.session.commit()
    flash('Doctor added successfully!', 'success')
    return redirect(url_for('manage_doctors'))

@app.route('/admin/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.name = request.form['name']
        doctor.specialization = request.form['specialization']
        doctor.availability = request.form['availability']
        db.session.commit()
        flash('Doctor updated!', 'success')
        return redirect(url_for('manage_doctors'))
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/admin/delete_doctor/<int:doctor_id>')
@login_required
def delete_doctor(doctor_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted!', 'success')
    return redirect(url_for('manage_doctors'))

# ------------------ PATIENTS CRUD ------------------
@app.route('/admin/patients')
def manage_patients():
    patients = PatientProfile.query.all()
    return render_template('manage_patients.html', patients=patients)

@app.route('/admin/patients/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    address = request.form['address']
    dob_str = request.form['dob']
    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    patient = PatientProfile(name=name, email=email, contact=contact, address=address, dob=dob)
    db.session.add(patient)
    db.session.commit()
    flash('Patient added successfully!', 'success')
    return redirect(url_for('manage_patients'))

@app.route('/admin/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = PatientProfile.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.email = request.form['email']
        patient.contact = request.form['contact']
        patient.address = request.form['address']
        dob_str = request.form['dob']
        patient.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('manage_patients'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/admin/patients/delete/<int:patient_id>')
def delete_patient(patient_id):
    patient = PatientProfile.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted!', 'success')
    return redirect(url_for('manage_patients'))

# ------------------ APPOINTMENTS CRUD ------------------
@app.route('/admin/manage_appointments')
@login_required
def manage_appointments():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    appointments = Appointment.query.all()
    doctors = DoctorProfile.query.all() 
    patients = PatientProfile.query.all()
    
    return render_template('manage_appointments.html',
                           appointments=appointments,
                           doctors=doctors,
                           patients=patients)

@app.route('/admin/edit_appointment/<int:appt_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appt_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    appt = Appointment.query.get_or_404(appt_id)
    doctors = DoctorProfile.query.all()
    patients = PatientProfile.query.all()
    if request.method == 'POST':
        appt.doctor_id = request.form['doctor_id']
        appt.patient_id = request.form['patient_id']
        appt.date = request.form['date']
        appt.time = request.form['time']
        appt.status = request.form['status']
        db.session.commit()
        flash('Appointment updated!', 'success')
        return redirect(url_for('manage_appointments'))
    return render_template('edit_appointment.html', appt=appt, doctors=doctors, patients=patients)

@app.route('/admin/delete_appointment/<int:appt_id>')
@login_required
def delete_appointment(appt_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    appt = Appointment.query.get_or_404(appt_id)
    db.session.delete(appt)
    db.session.commit()
    flash('Appointment deleted!', 'success')
    return redirect(url_for('manage_appointments'))


# --- Add Appointment from Manage Page ---
@app.route('/admin/add_appointment', methods=['POST'])
@login_required
def add_appointment():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    doctor_id = request.form['doctor_id']
    patient_id = request.form['patient_id']
    date = request.form['date']
    time = request.form['time']
    status = request.form['status']
    appt = Appointment(doctor_id=doctor_id, patient_id=patient_id, date=date, time=time, status=status)
    db.session.add(appt)
    db.session.commit()
    flash('Appointment added successfully!', 'success')
    return redirect(url_for('manage_appointments'))

@app.route('/admin/appointments/update/<int:appt_id>', methods=['POST'])
def update_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    appt.doctor_id = int(request.form['doctor_id'])
    appt.patient_id = int(request.form['patient_id'])
    appt.date = request.form['date']
    appt.time = request.form['time']
    appt.status = request.form['status']
    db.session.commit()
    flash('Appointment updated successfully!')
    return redirect(url_for('manage_appointments'))


# ------------------ Run App ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password='admin', role='admin')
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)
