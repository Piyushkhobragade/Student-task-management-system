from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from datetime import date
from config import DB_CONFIG, SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = SECRET_KEY   

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students WHERE email=%s",
            (email,)
        )
        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if student and check_password_hash(student["password"], password):
            session["student_id"] = student["student_id"]
            session["name"] = student["name"]
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/") # Redirect to login page

    return render_template("register.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/")

    student_id = session["student_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch assignments
    cursor.execute("""
        SELECT a.assignment_id, a.title, a.due_date, a.status, s.subject_name
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.subject_id
        WHERE s.student_id = %s
        ORDER BY a.due_date
    """, (student_id,))
    assignments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dashboard.html", assignments=assignments)

# ---------------- ADD SUBJECT ----------------
@app.route("/subject", methods=["GET", "POST"])
def subject():
    if "student_id" not in session:
        return redirect("/")

    if request.method == "POST":
        subject_name = request.form["subject_name"]
        student_id = session["student_id"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO subjects (subject_name, student_id) VALUES (%s, %s)",
            (subject_name, student_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/dashboard")

    return render_template("subject.html")

# ---------------- ADD ASSIGNMENT ----------------
@app.route("/assignment", methods=["GET", "POST"])
def assignment():
    if "student_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM subjects WHERE student_id=%s",
        (session["student_id"],)
    )
    subjects = cursor.fetchall()

    if request.method == "POST":
        title = request.form["title"]
        due_date = request.form["due_date"]
        subject_id = request.form["subject_id"]

        cursor.execute("""
            INSERT INTO assignments (title, due_date, status, subject_id)
            VALUES (%s, %s, 'Pending', %s)
        """, (title, due_date, subject_id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/dashboard")

    cursor.close()
    conn.close()

    return render_template("assignment.html", subjects=subjects)

# ---------------- MARK ASSIGNMENT COMPLETED ----------------
@app.route("/complete/<int:assignment_id>")
def complete_assignment(assignment_id):
    if "student_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE assignments SET status='Completed' WHERE assignment_id=%s",
        (assignment_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/dashboard")

# ---------------- DELETE ASSIGNMENT ----------------
@app.route("/delete/<int:assignment_id>")
def delete_assignment(assignment_id):
    if "student_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM assignments WHERE assignment_id = %s",
        (assignment_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    print("Assignment Tracker Starting...")
    print("Features Loaded:")
    print("✅ Keep Track of Assignments")
    print("✅ Mark Assignment as Done when Completed")
    print("\n🌐 Server running on http://localhost:5000")
    app.run(debug=True)
