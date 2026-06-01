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

        if not name or not email or not time:
            return "Missing fields", 400

        data = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "service": "General",
            "date": "2026-01-01",
            "time": time,
            "status": "confirmed"
        }

        db.add_booking(data)

        return "Booking confirmed ✅"

    except Exception as e:
        print("ERROR:", e)
        return "Server error", 500

if __name__ == "__main__":
    app.run()
