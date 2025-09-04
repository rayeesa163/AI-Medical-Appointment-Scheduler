# test_backend.py
from utils import lookup_patient, schedule_appointment

# Test lookup
print("🔎 Checking patient...")
patient = lookup_patient("John Doe", "1980-05-12")
print(patient)

# Test scheduling
if patient["found"]:
    appt = schedule_appointment(patient["doctor"], patient["patient_type"])
    print("📅 Appointment booked:", appt)
