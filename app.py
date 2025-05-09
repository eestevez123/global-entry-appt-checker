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

# Location IDs can be found using the TTP Appointment finder website 
# (https://ttp.dhs.gov/schedulerui/schedule-interview/location?lang=en&vo=true&returnUrl=ttp-external&service=up)
# Using Dev Tools, you can find the ID via checking the GET request made when manually checking available appointments on a location
# Location Key Names can be whatever you'd like
LOCATIONS = {
    "CHICAGO (Chicago O'Hare International Global Entry EC )": 5183,
    "CHICAGO (Chicago Field Office Enrollment Center)": 11981,
    "Rockford (Rockford-Chicago International Airport)" : 11001,
    "Milwaukee (Milwaukee Enrollment Center)": 7740,
    "MILWAUKEE (Mitchell International Airport)" : 16645
    }

# You can find the list of timezones here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = "America/Chicago"

# This is the date new appointments will be compared to
# If an earlier date is found, email notification is triggered
# Format: datetime(year, month, day) e.g datetime(2025, 4, 24)
THRESHOLD_DATE = datetime(2025, 4, 25)

# Integer, in minutes, for example: 20
CHECK_INTERVAL_MINUTES = 20

# Max number of locations is set to be 10 currently, but it is up to your discretion if you would like to increase
# this number
MAX_LOCATIONS = 10

# EMAIL CONFIG
# Refer to the readme for help finding the right values
# Please populate these variables in the .env file
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
ALERTS_ENABLED = os.getenv("ALERTS_ENABLED", "true").lower() == "true"

# If you want to run the app on a different port, change this
LOCAL_PORT = 3005

###########################################################################

# Memory storage
latest_slots = {}  # { location_name: datetime }
alerted_slots = {}  # { location_name: datetime }

app = Flask(__name__)

def cst_now():
    return datetime.now(tz=ZoneInfo(TIME_ZONE))

app.jinja_env.globals.update(
    now=cst_now,
    threshold_date=THRESHOLD_DATE,
    alerts_enabled=ALERTS_ENABLED
)


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

    # Limit the number of locations to MAX_LOCATIONS
    for i, (name, loc_id) in enumerate(LOCATIONS.items()):
        if i >= MAX_LOCATIONS:
            break  # Stop processing if the limit is reached
        
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
                data = response.json()
                slots = data.get("availableSlots", [])

                if slots:
                    first_slot = min(slots, key=lambda s: s["startTimestamp"])
                    dt = datetime.fromisoformat(first_slot["startTimestamp"])
                    latest_slots[name] = { "date": dt, "status": "available" }

                    previous_alert = alerted_slots.get(name)

                    # Only send an alert if it's before the threshold and is new
                    if dt < THRESHOLD_DATE and (previous_alert is None or dt != previous_alert):
                        if ALERTS_ENABLED:
                            send_email(
                                f"🚨 Early Appointment Found at {name}",
                                f"An earlier appointment is available at {name} on {dt.strftime('%B %d, %Y at %I:%M %p')}.\n\nVisit https://ttp.dhs.gov/"
                            )
                            alerted_slots[name] = dt  # Update alert history
                        else:
                            print(f"📬 Would alert for {name} on {dt} but alerts are disabled.")
                    else:
                        print(f"ℹ️ No new earlier appointment for {name}.")
                else:
                    last_pub = data.get("lastPublishedDate")
                    if last_pub:
                        dt = datetime.fromisoformat(last_pub)
                        latest_slots[name] = { "date": dt, "status": "full" }
                    else:
                        latest_slots[name] = { "date": None, "status": "unknown" }
            else:
                print(f"Error for {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")

# SCHEDULE BACKGROUND JOB
scheduler = BackgroundScheduler()
scheduler.add_job(check_appointments, "interval", minutes=CHECK_INTERVAL_MINUTES)
scheduler.start()

@app.route("/", methods=["GET"])
def index():
    # Sort the slots by date (ignoring None dates)
    sorted_slots = dict(
        sorted(
            latest_slots.items(),
            key=lambda item: item[1]["date"] if item[1]["date"] else datetime.max
        )
    )
    return render_template("index.html", slots=sorted_slots, threshold_date=THRESHOLD_DATE)

@app.route("/refresh", methods=["POST"])
def manual_refresh():
    check_appointments()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    check_appointments()  # initial run
    app.run(host="0.0.0.0", port=LOCAL_PORT)
