from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import db
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Alexandray26"

db.init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analytics")
def analytics():
    if not session.get("admin"):
        return redirect("/login")

    bookings = db.get_bookings()

    total = len(bookings)

    today = datetime.now().strftime("%Y-%m-%d")
    today_bookings = [b for b in bookings if b["date"] == today]

    unique_customers = len(set([b["email"] for b in bookings]))

    # simple grouping by date
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/admin")

        return "Invalid login"

    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    bookings = db.get_bookings()
    return render_template("admin.html", bookings=bookings)


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


@app.route("/book", methods=["POST"])
def book():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        time = request.form.get("time")

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

        return "Booking confirmed ✅"

    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return "❌ This slot is already booked", 409

        print("ERROR:", e)
        return "Server error", 500


if __name__ == "__main__":
    app.run()
