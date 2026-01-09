from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from db_config import get_db_connection
import random

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return render_template("login.html")
# ---------------- LOGIN API ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM admin WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        return render_template("dashboard.html")
    else:
        return jsonify({"status": "fail"})


# ---------------- TIMETABLE GENERATION API ----------------
@app.route("/generate", methods=["POST"])
def generate_timetable():
    data = request.json
    days = int(data["days"])
    periods = int(data["periods"])

    subjects = ["Maths", "DBMS", "OS", "AI", "CN"]

    timetable = {}

    for d in range(1, days + 1):
        day_list = []
        for p in range(periods):
            day_list.append(random.choice(subjects))
        timetable[f"Day {d}"] = day_list

    return jsonify(timetable)


# ---------------- DASHBOARD COUNTS API ----------------
@app.route("/dashboard", methods=["GET"])
def dashboard():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM faculty")
    faculty_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM subject")
    subject_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM classroom")
    room_count = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return jsonify({
        "faculty": faculty_count,
        "subjects": subject_count,
        "rooms": room_count
    })

# ---------------- NOTIFICATIONS ----------------
@app.route("/notifications", methods=["GET"])
def get_notifications():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM notification ORDER BY created_at DESC")
    data = cursor.fetchall()

    cursor.close()
    db.close()
    return jsonify(data)


# ---------------- CHANGE REQUEST (FACULTY) ----------------
@app.route("/change-request", methods=["POST"])
def change_request():
    data = request.json
    timetable_id = data["timetable_id"]
    reason = data["reason"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO change_request (timetable_id, reason) VALUES (%s, %s)",
        (timetable_id, reason)
    )

    cursor.execute(
        "INSERT INTO notification (message) VALUES (%s)",
        (f"New change request for timetable ID {timetable_id}",)
    )

    db.commit()
    cursor.close()
    db.close()

    return {"status": "Change request submitted"}


# ---------------- VIEW CHANGE REQUESTS (ADMIN) ----------------
@app.route("/change-requests", methods=["GET"])
def view_change_requests():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM change_request")
    data = cursor.fetchall()

    cursor.close()
    db.close()
    return jsonify(data)


# ---------------- EMERGENCY RESCHEDULE (ADMIN) ----------------
@app.route("/emergency-reschedule", methods=["POST"])
def emergency_reschedule():
    data = request.json
    tid = data["id"]
    faculty = data["faculty"]
    room = data["room"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE timetable SET faculty=%s, room=%s WHERE id=%s",
        (faculty, room, tid)
    )

    cursor.execute(
        "UPDATE change_request SET status='Approved' WHERE timetable_id=%s",
        (tid,)
    )

    cursor.execute(
        "INSERT INTO notification (message) VALUES (%s)",
        (f"Emergency reschedule done for timetable ID {tid}",)
    )

    db.commit()
    cursor.close()
    db.close()

    return {"status": "Rescheduled successfully"}



if __name__ == "__main__":
    app.run(debug=True)