from flask import Flask, render_template, request
import db

app = Flask(__name__)

db.init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    email = request.form["email"]
    time = request.form["time"]

    db.add_booking(name, email, time)

    return "Booking confirmed ✅"

if __name__ == "__main__":
    app.run()
