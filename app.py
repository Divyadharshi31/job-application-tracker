from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "jobs.db"


# Create database and table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            app_date TEXT NOT NULL,
            status TEXT NOT NULL,
            location TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


# Dashboard
@app.route("/")
def home():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Counts
    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Applied'"
    )
    applied = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Interview'"
    )
    interview = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Selected'"
    )
    selected = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Rejected'"
    )
    rejected = cursor.fetchone()[0]

    # Get all applications
    cursor.execute("""
        SELECT id, company, role, app_date, status, location, notes
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        total=total,
        applied=applied,
        interview=interview,
        selected=selected,
        rejected=rejected,
        applications=applications
    )


# Add application
@app.route("/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        app_date = request.form["app_date"]
        status = request.form["status"]
        location = request.form["location"]
        notes = request.form["notes"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO applications
            (company, role, app_date, status, location, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company,
            role,
            app_date,
            status,
            location,
            notes
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


# Delete application
@app.route("/delete/<int:application_id>")
def delete_application(application_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Start application
if __name__ == "__main__":
    init_db()
    app.run(debug=False)
