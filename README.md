# global-entry-appt-checker

![Global Entry Checker UI](static/preview.png "Live dashboard showing appointment availability")

This is a python application that helps track and notify the user if an early appointment has been found at their selected locations.

## Running Locally and Preparation for Deployment

### Important Commands Running Locally
`python3 -m venv venv` : installs ability to create and get into a virtual local environment

`source venv/bin/activate` : gets you into the virtual env

`deactivate` : gets you out of the virtual env

`pip install -r requirements.txt` : install required python libraries for this project

`python3 app.py` : runs the application

### Creating a .env file locally
Make sure you create a .env within this repository's directory in order for this application to work for you
The following should be filled in:

`EMAIL_ADDRESS=your_email@gmail.com`

`EMAIL_PASSWORD=your_gmail_app_password`

`TO_EMAIL=your_email@gmail.com   # Or any other email address you want alerts sent to`

`ALERTS_ENABLED=false #if you would like email notification about earlier appointments found compared to threshold date`

For help getting your app password if you are using G-mail, I suggest following this video: [How To Set Up Gmail SMTP Server - Full Guide
](https://www.youtube.com/watch?v=ZfEK3WP73eY).

These environment variables will need to be created and set when deploying this code.

### Testing Email Sending Locally
Once you set up your .env file, run the following command: `python3 test_send_email.py`

You will know you have the correct values once you receive the test email in your inbox

## Deployment

I recommend using a free platform such as [Render](https://render.com/) which is what I used for this project.

### Render Deployment Instructions

Deploy the code out as a Web Service. You can either connect your GitHub account with the repository that holds this code, or upload this code manually.

Make sure to set up the .env variables as described earlier while setting up the project within Render.

Name: *whatever you'd like, e.g. global-entry-checker*

Environment: Python

Build Command: `pip install -r requirements.txt`

Start command for application: `python app.py`

Instance Type: Free (for personal/light usage)

Region: Closest to your location (e.g., Oregon or Ohio)

Make sure to include the .env variables as detailed above in this readme


### Using UptimeRobot to keep application alive and working

I recommend using [UptimeRobot](https://uptimerobot.com/) to keep the website alive and preventing it from going to sleep which is a risk when deploying this code using a free tier account.

This application has a `/heath` endpoint that can be tapped into to check the static of the website and also keep it alive.

