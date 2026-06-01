import smtplib
from email.mime.text import MIMEText

EMAIL = "mindbytesnow@gmail.com"
PASSWORD = "dzip yqiw xjva wfeg"

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

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()
def notify_admin(name, email, date, time):

    msg = MIMEText(f"""
New Booking Received

Name: {name}
Email: {email}
Date: {date}
Time: {time}
""")

    msg["Subject"] = "New Booking Alert 🚀"
    msg["From"] = EMAIL

    # Your email address
    msg["To"] = "mindbytesnow@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
