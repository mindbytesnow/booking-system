import smtplib
from email.mime.text import MIMEText

EMAIL = "mindbytesnow@gmail.com"
PASSWORD = "dzipyqiwxjvawfeg"  # keep your Gmail app password here

# ---------- EMAIL TEMPLATE ----------
def build_customer_email(name, date, time):
    return f"""
    <html>
    <body style="font-family:Arial;background:#f6f8fb;padding:20px;">

        <div style="max-width:500px;margin:auto;background:white;padding:25px;border-radius:12px;">

            <h2 style="color:#111;">Booking Confirmed ✅</h2>

            <p>Hi <b>{name}</b>,</p>

            <p>Your appointment has been successfully booked.</p>

            <div style="background:#f4f6f8;padding:12px;border-radius:8px;margin:15px 0;">
                <p><b>Date:</b> {date}</p>
                <p><b>Time:</b> {time}</p>
            </div>

            <p style="color:#555;">
                Please arrive 5–10 minutes early.
            </p>

            <hr>

            <p style="font-size:12px;color:#999;">
                Powered by Booking System
            </p>

        </div>

    </body>
    </html>
    """


def build_admin_email(name, email, date, time):
    return f"""
    <html>
    <body style="font-family:Arial;background:#f6f8fb;padding:20px;">

        <div style="max-width:500px;margin:auto;background:white;padding:25px;border-radius:12px;">

            <h2 style="color:#111;">New Booking Alert 🚀</h2>

            <p>A new booking has been created:</p>

            <div style="background:#f4f6f8;padding:12px;border-radius:8px;">
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Date:</b> {date}</p>
                <p><b>Time:</b> {time}</p>
            </div>

        </div>

    </body>
    </html>
    """


# ---------- SEND CUSTOMER EMAIL ----------
def send_confirmation(to_email, name, date, time):
    msg = MIMEText(build_customer_email(name, date, time), "html")

    msg["Subject"] = "Your Booking is Confirmed"
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


# ---------- SEND ADMIN EMAIL ----------
def notify_admin(name, email, date, time):
    msg = MIMEText(build_admin_email(name, email, date, time), "html")

    msg["Subject"] = "New Booking Received"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
