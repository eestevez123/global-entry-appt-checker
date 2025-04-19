from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
from datetime import datetime
import random
from zoneinfo import ZoneInfo
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

######################### CONFIG ##########################################
LOCATIONS = {
    "CHICAGO (Chicago O'Hare International Global Entry EC )": 5183,
    "CHICAGO (Chicago Field Office Enrollment Center)": 11981,
    "Milwaukee (Milwaukee Enrollment Center)": 7740,
}
THRESHOLD_DATE = datetime(2025, 4, 28)
CHECK_INTERVAL_MINUTES = 20
MAX_LOCATIONS = 10

# SMS CONFIG
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

###########################################################################

# Memory storage
latest_slots = {}  # { location_name: datetime }

app = Flask(__name__)

def cst_now():
    return datetime.now(tz=ZoneInfo("America/Chicago"))

app.jinja_env.globals.update(now=cst_now, threshold_date=THRESHOLD_DATE)


def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def check_appointments():
    global latest_slots
    print(f"[{datetime.now()}] Checking appointment availability...")
    for name, loc_id in LOCATIONS.items():
        try:
            headers = {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                    "Mozilla/5.0 (X11; Linux x86_64)"
                ])
            }
            url = f"https://ttp.cbp.dhs.gov/schedulerapi/slot-availability?locationId={loc_id}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                slots = response.json().get("availableSlots", [])
                if slots:
                    first_slot = min(slots, key=lambda s: s["startTimestamp"])
                    dt = datetime.fromisoformat(first_slot["startTimestamp"])
                    previous = latest_slots.get(name)

                    if dt < THRESHOLD_DATE:
                        send_email(
                        f"🚨 Early Appointment Found at {name}",
                        f"An earlier appointment is available at {name} on {dt.strftime('%B %d, %Y at %I:%M %p')}.\n\nVisit https://ttp.dhs.gov/"
                        )
                    if not previous or dt < previous:
                        latest_slots[name] = dt
            else:
                print(f"Error from {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error for {name}: {e}")

# SCHEDULE BACKGROUND JOB
scheduler = BackgroundScheduler()
scheduler.add_job(check_appointments, "interval", minutes=CHECK_INTERVAL_MINUTES)
scheduler.start()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", slots=latest_slots, threshold_date=THRESHOLD_DATE)

@app.route("/refresh", methods=["POST"])
def manual_refresh():
    check_appointments()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    check_appointments()  # initial run
    app.run(host="0.0.0.0", port=3005)
