import smtplib
from email.mime.text import MIMEText

EMAIL = "mindbytesnow@gmail.com"
PASSWORD = "dzipyqiwxjvawfeg"


def send_email(msg):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("EMAIL ERROR:", e)


def send_confirmation(to_email, name, date, time):

    body = f"""
Hi {name},

Your booking has been confirmed.

Date: {date}
Time: {time}

Thank you.
"""

    msg = MIMEText(body)
    msg["Subject"] = "Booking Confirmation"
    msg["From"] = EMAIL
    msg["To"] = to_email

    send_email(msg)


def notify_admin(name, email, date, time):

    body = f"""
New Booking Received

Name: {name}
Email: {email}
Date: {date}
Time: {time}
"""

    msg = MIMEText(body)
    msg["Subject"] = "New Booking Alert 🚀"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    send_email(msg)
