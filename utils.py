from models import Appointment
def prevent_double_booking(doctor_id, appt_date, appt_time):
    existing = Appointment.query.filter_by(doctor_id=doctor_id, date=appt_date, time=appt_time).first()
    return existing is not None

def doctor_is_available(doctor_profile, appt_date, appt_time):
    # availability stored as JSON: { "mon": ["09:00","10:00"], ... }
    try:
        import json, datetime
        avail = json.loads(doctor_profile.availability or '{}')
        weekday = appt_date.strftime('%a').lower()  # e.g., Mon -> mon
        slots = avail.get(weekday[:3].lower(), [])  # try keys like 'mon'
        # compare time strings 'HH:MM'
        tstr = appt_time.strftime('%H:%M')
        return tstr in slots
    except Exception:
        return doctor_profile.is_active
