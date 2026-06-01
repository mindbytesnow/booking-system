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
