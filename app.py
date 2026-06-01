from flask import Flask, render_template, request, jsonify, session, redirect
import stripe
import uuid
import bcrypt

from db import init_db, add_booking, get_bookings, delete_booking, get_booked_times

from calendar_api import create_event
from emailer import send_email

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET"

stripe.api_key = "YOUR_STRIPE_KEY"

init_db()

ADMIN_USER = "admin"
ADMIN_PASS_HASH = b"PASTE_BCRYPT_HASH_HERE"


SLOTS = [
    "09:00","10:00","11:00","12:00",
    "13:00","14:00","15:00","16:00"
]


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- SLOTS ----------
@app.route("/slots/<date>")
def slots(date):
    booked = get_booked_times(date)
    available = [s for s in SLOTS if s not in booked]
    return jsonify(available)


# ---------- STRIPE ----------
@app.route("/create-session", methods=["POST"])
def create_session():
    data = request.json

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Booking"},
                "unit_amount": 5000
            },
            "quantity": 1
        }],
        success_url=f"http://localhost:5000/success?name={data['name']}&email={data['email']}&service={data['service']}&date={data['date']}&time={data['time']}",
        cancel_url="http://localhost:5000/"
    )

    return jsonify({"url": session.url})


# ---------- SUCCESS ----------
@app.route("/success")
def success():

    data = {
        "id": str(uuid.uuid4()),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "service": request.args.get("service"),
        "date": request.args.get("date"),
        "time": request.args.get("time"),
        "status": "paid"
    }

    try:
        add_booking(data)
    except:
        return "Slot already booked ❌"

    send_email(data)
    create_event(data)

    return "Booking Confirmed ✅"


# ---------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        if bcrypt.checkpw(request.form["password"].encode(), ADMIN_PASS_HASH):
            session["logged_in"] = True
            return redirect("/admin")

        return "Wrong password"

    return render_template("login.html")


# ---------- ADMIN ----------
@app.route("/admin")
def admin():

    if not session.get("logged_in"):
        return redirect("/login")

    bookings = get_bookings()

    revenue = len(bookings) * 50

    return render_template("admin.html",
        bookings=bookings,
        total=len(bookings),
        revenue=revenue
    )


# ---------- DELETE ----------
@app.route("/delete/<bid>")
def delete(bid):

    if not session.get("logged_in"):
        return redirect("/login")

    delete_booking(bid)

    return redirect("/admin")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
