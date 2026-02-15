from flask import Flask, render_template, request, redirect, session
from sheets import check_student_login, get_parent_dashboard_data, get_syllabus_for_student
from datetime import datetime
app = Flask(__name__)
app.secret_key = ""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form["student_id"]
        password = request.form["password"]

        student = check_student_login(student_id, password)
        if student:
            session["student_id"] = student["student_id"]
            session["student_name"] = student["name"]
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid Student ID or Name")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/")




    month = request.args.get(
    "month",
    datetime.now().strftime("%Y-%m"))
    data = get_parent_dashboard_data(session["student_id"], month)

    return render_template(
        "dashboard.html",
        data=data,
        student_name=session["student_name"]
    )

@app.route("/syllabus")
def syllabus():
    if "student_id" not in session:
        return redirect("/")

    syllabus = get_syllabus_for_student(session["student_id"])

    return render_template(
        "syllabus.html",
        syllabus=syllabus
    )



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/hafalan")
def hafalan_page():
    if "student_id" not in session:
        return redirect("/")

    from datetime import datetime
    month = datetime.now().strftime("%Y-%m")

    data = get_parent_dashboard_data(session["student_id"], month)

    return render_template(
        "hafalan.html",
        data=data,
        student_name=session["student_name"]
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    # app.run(host="0.0.0.0", port=8000, debug=True)


# http://141.11.25.251:8000/dashboard