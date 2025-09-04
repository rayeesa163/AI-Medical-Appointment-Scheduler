import streamlit as st
import pandas as pd
from utils import (
    lookup_patient,
    schedule_appointment,
    send_intake_form,
    generate_appointment_pdf,
    send_reminders,
)

st.set_page_config(page_title="AI Scheduling Agent", page_icon="🩺", layout="wide")

# --------------------------
# Custom CSS for CEO Dashboard Look
# --------------------------
st.markdown(
    """
    <style>
    /* Background */
    .main {
        background-color: #f5f7fa;
    }
    /* White card container */
    .stApp {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 25px;
        box-shadow: 0px 6px 14px rgba(0,0,0,0.08);
    }
    /* Section Headings */
    h2 {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #222222 !important;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 6px;
        margin-bottom: 20px;
    }
    /* Subheadings */
    h3 {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #333333 !important;
    }
    /* Buttons */
    div.stButton > button {
        background-color: #ffffff;
        color: #333333;
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #f0f0f0;
        border: 1px solid #bbb;
    }
    /* Admin Panel Table Styling */
    .stDataFrame table {
        border: 1px solid #ddd;
        border-collapse: collapse;
    }
    .stDataFrame th {
        background-color: #4CAF50;
        color: white;
        font-weight: 700;
        padding: 8px;
    }
    .stDataFrame td {
        padding: 8px;
        border: 1px solid #ddd;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to:", ["Patient Flow", "Admin Panel"])

# --------------------------
# PATIENT FLOW
# --------------------------
if page == "Patient Flow":

    if "step" not in st.session_state:
        st.session_state.step = "greet"
    if "patient" not in st.session_state:
        st.session_state.patient = None
    if "appointment" not in st.session_state:
        st.session_state.appointment = None

    st.sidebar.write("📌 Current Step:", st.session_state.step)

    # ------------------ Greeting Step ------------------
    if st.session_state.step == "greet":
        st.markdown("## 👤 Patient Information")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            dob = st.text_input("Date of Birth (YYYY-MM-DD)")
        with col2:
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")

        if st.button("➡️ Next", use_container_width=True):
            if name and dob and email:
                patient = lookup_patient(name, dob)
                st.session_state.patient = {
                    "id": patient["id"] if patient and patient["found"] else None,
                    "name": name,
                    "dob": dob,
                    "email": email if not (patient and patient["found"]) else patient["email"],
                    "phone": phone if not (patient and patient["found"]) else patient["phone"],
                    "doctor": patient["doctor"] if patient else None,
                    "patient_type": patient["patient_type"] if patient else "New",
                    "found": patient["found"] if patient else False,
                }
                st.session_state.step = "schedule"
            else:
                st.warning("⚠️ Please enter Name, DOB, and Email.")

    # ------------------ Scheduling Step ------------------
    elif st.session_state.step == "schedule":
        st.markdown("## 📅 Schedule Your Appointment")
        patient = st.session_state.patient

        if patient["found"]:
            doctor = patient["doctor"]
            patient_type = patient["patient_type"]
            st.info(f"Assigned Doctor: **{doctor}** | Status: **{patient_type} Patient**")
        else:
            try:
                df_doctors = pd.read_excel("data/doctors.xlsx")
                doctors = df_doctors["Doctor"].tolist()
            except Exception:
                doctors = ["Dr. Smith", "Dr. Johnson", "Dr. Lee"]

            doctor = st.selectbox("Choose your preferred doctor:", doctors)
            patient_type = "New"

        if st.button("➡️ Next", use_container_width=True):
            appt = schedule_appointment(doctor, patient_type)
            if appt:
                st.session_state.appointment = appt
                st.session_state.step = "insurance"
            else:
                st.error("❌ No available slots. Please try another doctor.")

    # ------------------ Insurance Step ------------------
    elif st.session_state.step == "insurance":
        st.markdown("## 🏦 Insurance Information")
        st.markdown("Please provide your insurance details to proceed:")

        carrier = st.text_input("Insurance Carrier")
        member_id = st.text_input("Member ID")
        group_number = st.text_input("Group Number")

        if st.button("➡️ Next", use_container_width=True):
            st.session_state.patient["insurance"] = {
                "carrier": carrier,
                "member_id": member_id,
                "group_number": group_number,
            }

            st.session_state.appointment = schedule_appointment(
                st.session_state.appointment["doctor"],
                st.session_state.patient["patient_type"],
                st.session_state.patient["insurance"],
            )

            st.session_state.step = "confirmation"

    # ------------------ Confirmation Step ------------------
    elif st.session_state.step == "confirmation":
        st.markdown("## 🎉 Appointment Confirmation")

        appt = st.session_state.appointment
        patient = st.session_state.patient

        if appt is None:
            st.error("⚠️ Appointment details not found. Please try booking again.")
        else:
            insurance = patient.get("insurance", {})

            st.markdown(
                f"""
                <div style="background-color:#E8F6F3; padding:15px; border-radius:10px; font-size:16px;">
                <b>Patient ID:</b> {patient.get('id', 'N/A')} <br>
                <b>Name:</b> {patient['name']} <br>
                <b>Email:</b> {patient['email']} <br>
                <b>Phone:</b> {patient['phone']} <br><br>
                <b>Doctor:</b> {appt['doctor']} <br>
                <b>Slot:</b> {appt['slot']} <br>
                <b>Duration:</b> {appt['duration']} minutes <br><br>
                <b>Insurance Carrier:</b> {insurance.get('carrier','N/A')} <br>
                <b>Member ID:</b> {insurance.get('member_id','N/A')} <br>
                <b>Group Number:</b> {insurance.get('group_number','N/A')}
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("📨 Send Intake Form", use_container_width=True):
                if send_intake_form(patient["email"], patient["name"]):
                    st.success(f"✅ Intake form sent to {patient['email']} (simulated).")
                else:
                    st.error("❌ Failed to send intake form.")

            if st.button("📄 Generate Appointment Slip", use_container_width=True):
                pdf_file = generate_appointment_pdf(patient, appt)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Appointment Slip",
                        data=f,
                        file_name=pdf_file,
                        mime="application/pdf",
                    )

            if st.button("🔔 Send Reminders (Simulated)", use_container_width=True):
                if send_reminders(patient, appt):
                    st.success("✅ Reminders sent (simulated). Check console logs.")
                else:
                    st.error("❌ Failed to send reminders.")

# --------------------------
# ADMIN PANEL
# --------------------------
elif page == "Admin Panel":
    st.markdown("## 🗂️ Admin Panel – Appointment Records")

    try:
        df = pd.read_excel("data/appointments.xlsx")
        st.dataframe(df)

        st.download_button(
            "⬇️ Download Appointments (Excel)",
            data=open("data/appointments.xlsx", "rb").read(),
            file_name="appointments.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.download_button(
            "⬇️ Download Appointments (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="appointments.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.warning(f"⚠️ No appointment records found yet. Error: {e}")
