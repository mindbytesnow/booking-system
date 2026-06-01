from flask import Flask, render_template, request, jsonify
import db
import uuid

app = Flask(__name__)

db.init_db()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/available")
def available():
    date = request.args.get("date")

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
