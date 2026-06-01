import smtplib
from email.mime.text import MIMEText

def send_email(data):

    sender = "YOUR_EMAIL@gmail.com"
    password = "YOUR_APP_PASSWORD"

    msg = MIMEText(f"""
Booking Confirmed

Name: {data['name']}
Service: {data['service']}
Date: {data['date']}
Time: {data['time']}
""")

    msg["Subject"] = "Booking Confirmation"
    msg["From"] = sender
    msg["To"] = data["email"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
