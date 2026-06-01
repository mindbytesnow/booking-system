from emailer import send_confirmation, notify_admin
from flask import Flask, render_template, request, jsonify, session, redirect
import db
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Alexandray26"

db.init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        time = request.form.get("time")

        print("🔥 BOOK REQUEST RECEIVED")
        print(name, email, date, time)

        # ✅ VALIDATION
        if not name or not email or not date or not time:
            return "Missing fields ❌", 400

        # 🚫 DOUBLE BOOKING CHECK (FIX)
        booked_times = db.get_booked_times(date)

        if time in booked_times:
            return "❌ This slot is already booked. Please choose another time.", 409

        data = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "service": "General",
            "date": date,
            "time": time,
            "status": "confirmed"
        }

        db.add_booking(data)

        # 📧 EMAIL SYSTEM (safe)
        try:
            send_confirmation(email, name, date, time)
            notify_admin(name, email, date, time)
            print("📧 EMAILS SENT")
        except Exception as mail_error:
            print("EMAIL ERROR:", mail_error)

        return "Booking confirmed ✅"

    except Exception as e:
        print("❌ BOOKING ERROR:", e)
        return f"Server error: {str(e)}", 500


@app.route("/available")
def available():
    date = request.args.get("date")

    if not date:
        return jsonify([])

    booked = db.get_booked_times(date)

    all_slots = [
        "10:00 AM",
        "11:00 AM",
        "12:00 PM",
        "2:00 PM",
        "3:00 PM",
        "4:00 PM"
    ]

    free_slots = [t for t in all_slots if t not in booked]

    return jsonify(free_slots)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/admin")

            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    bookings = db.get_bookings()
    return render_template("admin.html", bookings=bookings)


@app.route("/analytics")
def analytics():
    if not session.get("admin"):
        return redirect("/login")

    bookings = db.get_bookings()

    total = len(bookings)

    today = datetime.now().strftime("%Y-%m-%d")
    today_bookings = [b for b in bookings if b["date"] == today]

    unique_customers = len(set([b["email"] for b in bookings]))

    stats = {}
    for b in bookings:
        d = b["date"]
        stats[d] = stats.get(d, 0) + 1

    return render_template(
        "analytics.html",
        total=total,
        today=len(today_bookings),
        unique=unique_customers,
        stats=stats
    )


@app.route("/delete/<bid>")
def delete(bid):
    if not session.get("admin"):
        return redirect("/login")

    db.delete_booking(bid)
    return redirect("/admin")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
