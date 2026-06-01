from flask import Flask, render_template, request
import db

app = Flask(__name__)

db.init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    try:
        import uuid

        name = request.form.get("name")
        email = request.form.get("email")
        time = request.form.get("time")

        date = "2026-01-01"  # temporary (we can upgrade to real calendar later)

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
        # THIS catches double booking error
        if "UNIQUE constraint failed" in str(e):
            return "❌ This time slot is already booked", 409

        print("ERROR:", e)
        return "Server error", 500

if __name__ == "__main__":
    app.run()
