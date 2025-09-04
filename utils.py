import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
import io

# --------------------------
# Lookup Patient
# --------------------------
def lookup_patient(name, dob):
    """
    Look up patient by Name + DOB in patients.csv
    Returns dict with patient details if found, else default new patient dict.
    """
    try:
        df = pd.read_csv("data/patients.csv")
    except Exception:
        return {
            "found": False,
            "id": None,
            "doctor": None,
            "patient_type": "New",
            "email": None,
            "phone": None,
        }

    row = df[(df["Name"].str.lower() == name.lower()) & (df["DOB"] == dob)]

    if not row.empty:
        return {
            "found": True,
            "id": row["ID"].values[0],
            "doctor": row["Doctor"].values[0],
            "patient_type": row["PatientType"].values[0],
            "email": row["Email"].values[0],
            "phone": row["Phone"].values[0],
        }
    else:
        return {
            "found": False,
            "id": None,
            "doctor": None,
            "patient_type": "New",
            "email": None,
            "phone": None,
        }


# --------------------------
# Schedule Appointment
# --------------------------
def schedule_appointment(doctor, patient_type, insurance=None):
    """
    Books first available slot for given doctor from doctors.xlsx
    Logs to appointments.xlsx and updates slots.
    """
    try:
        df = pd.read_excel("data/doctors.xlsx")
    except Exception:
        return None

    row = df[df["Doctor"] == doctor]
    if row.empty:
        return None

    # Safely handle Available Slots
    raw_slots = str(row["Available Slots"].values[0])
    if raw_slots == "nan" or raw_slots.strip() == "":
        return None  # No slots left

    slots = raw_slots.split(", ")
    duration = 60 if patient_type == "New" else 30
    chosen_slot = slots[0]  # first available slot

    # Log appointment
    try:
        appt_df = pd.read_excel("data/appointments.xlsx")
    except Exception:
        appt_df = pd.DataFrame(
            columns=[
                "Doctor",
                "Slot",
                "PatientType",
                "InsuranceCarrier",
                "MemberID",
                "GroupNumber",
            ]
        )

    # Default insurance info if missing
    insurance = insurance or {"carrier": "N/A", "member_id": "N/A", "group_number": "N/A"}

    appt_df.loc[len(appt_df)] = [
        doctor,
        chosen_slot,
        patient_type,
        insurance.get("carrier", "N/A"),
        insurance.get("member_id", "N/A"),
        insurance.get("group_number", "N/A"),
    ]
    appt_df.to_excel("data/appointments.xlsx", index=False)

    # Update doctor slots (remove booked one)
    slots.pop(0)
    df.loc[df["Doctor"] == doctor, "Available Slots"] = ", ".join(slots)
    df.to_excel("data/doctors.xlsx", index=False)

    return {"doctor": doctor, "slot": chosen_slot, "duration": duration}


# --------------------------
# Send Intake Form (Simulated)
# --------------------------
def send_intake_form(email, name):
    """
    Simulates sending an intake form by email.
    In real system integrate with SMTP / SendGrid / Twilio etc.
    """
    try:
        print(f"📨 Sending intake form to {email} for {name}...")
        return True
    except Exception as e:
        print("Error sending intake form:", e)
        return False


# --------------------------
# Generate Appointment PDF with QR + Insurance
# --------------------------
def generate_appointment_pdf(patient, appt, filename="appointment_slip.pdf"):
    """
    Generates a professional appointment slip PDF including patient ID, insurance, and QR Code.
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 80, "🏥 MediCare Appointment Slip")

    # Patient Info
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"Patient ID: {patient.get('id', 'N/A')}")
    c.drawString(100, height - 170, f"Name: {patient['name']}")
    c.drawString(100, height - 190, f"Email: {patient['email']}")
    c.drawString(100, height - 210, f"Phone: {patient.get('phone','N/A')}")
    c.drawString(100, height - 230, f"DOB: {patient['dob']}")

    # Appointment Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 270, "Appointment Details")
    c.setFont("Helvetica", 12)
    c.drawString(120, height - 290, f"Doctor: {appt['doctor']}")
    c.drawString(120, height - 310, f"Slot: {appt['slot']}")
    c.drawString(120, height - 330, f"Duration: {appt['duration']} minutes")

    # Insurance Info
    insurance = patient.get("insurance", {})
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 370, "Insurance Details")
    c.setFont("Helvetica", 12)
    c.drawString(120, height - 390, f"Carrier: {insurance.get('carrier','N/A')}")
    c.drawString(120, height - 410, f"Member ID: {insurance.get('member_id','N/A')}")
    c.drawString(120, height - 430, f"Group Number: {insurance.get('group_number','N/A')}")

    # QR Code
    qr_data = f"PatientID:{patient.get('id','N/A')}, Name:{patient['name']}, Doctor:{appt['doctor']}, Slot:{appt['slot']}, Insurance:{insurance.get('carrier','N/A')}"
    qr = qrcode.make(qr_data)

    qr_bytes = io.BytesIO()
    qr.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)
    qr_img = ImageReader(qr_bytes)

    c.drawImage(qr_img, width - 200, height - 400, width=100, height=100)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(
        width / 2,
        50,
        "Please bring this slip, your insurance card, and a valid ID at the time of your appointment.",
    )

    c.save()
    return filename
