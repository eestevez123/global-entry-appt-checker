# Global Entry Appointment Checker

![Global Entry Checker UI](static/preview.png "Live dashboard showing appointment availability")

Monitor Global Entry appointment availability at selected locations and get notified by email when earlier slots appear.

👉 [Live Demo](https://global-entry-appt-checker.onrender.com/)

## ⚠️ Disclaimer

This is an unofficial tool designed to help users monitor Global Entry appointment availability more efficiently.

- This project is not affiliated with or endorsed by U.S. Customs and Border Protection (CBP) or the U.S. government.
- All data is obtained from publicly available endpoints without authentication.
- Please use this tool responsibly and avoid excessive or abusive traffic to government services.

Please view this document for further information: [Legal Notice & Disclaimers](./docs/legal.md)

## 🛠️ Getting Started (Local Setup)

### 1. Set Up Virtual Environment

```bash
python3 -m venv venv       # Create virtual environment
source venv/bin/activate   # Activate it (use venv\Scripts\activate on Windows)
pip install -r requirements.txt # install required python libraries for this project
```

To deactivate:
```bash
deactivate
```

### 2. Creating a .env file locally
Create a .env file in the root directory and add the following:

```dotenv
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
TO_EMAIL=recipient_email@gmail.com
ALERTS_ENABLED=true
```

`ALERTS_ENABLED` is used to control whether you would like email notification about earlier appointments found compared to threshold date

For help getting your app password if you are using G-mail, I suggest following this video: [How To Set Up Gmail SMTP Server - Full Guide
](https://www.youtube.com/watch?v=ZfEK3WP73eY).

These environment variables will need to be created and set when deploying this code.

### 3. Run Locally

#### Testing Email Sending Locally
Once you set up your .env file, run the following command: `python3 test_send_email.py`

You will know you have the correct values once you receive the test email in your inbox

Use `python3 app.py` to run the actual application. The default port is 3005, but this can be modified.

## 🚀 Deploying on Render

This project works well as a [Render](https://render.com/) Web Service (free tier).

### ✅ Recommended Settings

| Setting         | Value                          |
|----------------|----------------------------------|
| Environment     | Python                         |
| Build Command   | `pip install -r requirements.txt` |
| Start Command   | `python app.py`                |
| Instance Type   | Free                            |
| Region          | Closest to you                  |
| Environment Vars| Set as in `.env` above          |

You can deploy by linking your GitHub repo or uploading manually.

---

### 🛡️ Keep It Alive with UptimeRobot

On Render’s free tier, your app may go to sleep without traffic.

To keep it alive:
- Sign up at [UptimeRobot](https://uptimerobot.com/)
- Create a monitor that pings: https://your-app-name.onrender.com/health (change this according to what you named your project). This triggers your `/health` endpoint and keeps the scheduler running.

---

Made with ❤️ by [Eddie Estevez](mailto:estevez.eduardo111@gmail.com) • [View source](https://github.com/eestevez123/global-entry-appt-checker)