

# **AI Medical Appointment Scheduler**

An intelligent **AI-powered medical appointment scheduling system** that automates patient bookings, reduces no-shows, and streamlines clinic operations.

---

## **🚀 Features**

* **Patient Management**

  * Store and manage patient details (Name, DOB, Phone Number)
  * Track appointment history and upcoming appointments

* **Smart Scheduling**

  * Schedule and reschedule appointments efficiently
  * Handles double-booking conflicts

* **Reminders & Notifications**

  * Sends automated appointment reminders to patients
  * Optional SMS/email integration

* **PDF Download**

  * Generate patient appointment summaries as PDFs for records

* **Next Doctor Appointment Tracking**

  * Automatically suggest next follow-up appointments

* **Demo Video**

  * Showcase workflow in human-friendly 4–5 min video

---

## **💻 Tech Stack**

* **Backend:** Python, Flask / Django
* **Frontend:** Streamlit / React (if web app)
* **Database:** SQLite / PostgreSQL
* **PDF Generation:** ReportLab / FPDF
* **AI Integration:** ChatGPT for scheduling guidance
* **Deployment:** Heroku / Streamlit Cloud

---

## **📂 Project Structure**

```
AI-Medical-Appointment-Scheduler/
│
├── app.py                 # Main application
├── models.py              # Database models
├── utils.py               # Helper functions
├── templates/             # HTML templates (if using Flask)
├── static/                # CSS / JS files
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── demo_video.mp4         # Demo video of app workflow
```

---

## **📌 Installation**

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/AI-Medical-Appointment-Scheduler.git
cd AI-Medical-Appointment-Scheduler
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python app.py
```

4. Open your browser and go to `http://localhost:5000` (Flask) or Streamlit URL.

---

## **🎯 Usage**

1. Enter patient details (Name, DOB, Phone Number).
2. Schedule a new appointment or view existing ones.
3. Generate PDF summaries for patient records.
4. View suggested next appointments automatically.
5. Send reminders to reduce no-shows.

---

## **📹 Demo**

Check out the [demo video]:https://www.loom.com/share/ecff1eabb9dd437a9e8f662a2958dc8c?sid=2c1cb23a-855d-4f2c-861f-41603d23972d

---

## **⚙️ Future Enhancements**

* Integrate **SMS and email reminders** via Twilio/SendGrid.
* Add **voice assistant support** for appointment booking.
* Implement **AI-based scheduling optimization** to minimize conflicts.
* Add **multi-doctor and multi-clinic support**.

---

## **📝 License**

MIT License – feel free to use and modify the code.

---

