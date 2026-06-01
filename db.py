import sqlite3

DB_NAME = "bookings.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        service TEXT,
        date TEXT,
        time TEXT,
        status TEXT,
        UNIQUE(date, time)
    )
    """)

    conn.commit()
    conn.close()


def add_booking(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO bookings (id, name, email, service, date, time, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["name"],
        data["email"],
        data["service"],
        data["date"],
        data["time"],
        data["status"]
    ))

    conn.commit()
    conn.close()


def get_bookings():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM bookings")
    rows = c.fetchall()

    conn.close()
    return [dict(r) for r in rows]


def delete_booking(bid):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM bookings WHERE id = ?", (bid,))

    conn.commit()
    conn.close()


def get_booked_times(date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT time FROM bookings WHERE date = ?", (date,))
    rows = c.fetchall()

    conn.close()
    return [r[0] for r in rows]
