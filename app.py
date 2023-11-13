from flask import Flask, session, render_template, redirect, request
from users_functions import login_verification, get_user_id, register_verification, restore_verification, get_first_name
from tasks_functions import read_tasks, update_task, update_status, delete_task, add_task
from data import setup

setup()

app = Flask(__name__)

app.secret_key="FireRat"

@app.route('/')
def home_page():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    return render_template("home.html")

# Login routes

@app.route('/log_out')
def clear_session():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    session.clear()
    return "Log Out Succeeded"

@app.route('/login')
def login_page():
    if session.get("user_id", "") != "":
        return redirect("/")
    
    return render_template("login.html")

@app.route('/login_verification', methods=['POST'])
def login_ver():
    if session.get("user_id", "") != "":
        return redirect("/")
    
    email = request.form["email"]
    password = request.form["password"]
    login_verification_msg = login_verification(email=email, password=password)

    if login_verification_msg[0]:
        user_id = get_user_id(email=email)
        session["user_id"] = user_id
        return redirect("/")
    
    message = login_verification_msg[1]
    return render_template("login.html", message=message, email=email)

# Restore password routes

@app.route('/restore')
def restore_page():
    if session.get("user_id", "") != "":
        return redirect("/")
    
    return render_template("restore.html")

@app.route('/restore_verification', methods=['POST'])
def restore_ver():
    if session.get("user_id", "") != "":
        return redirect("/")
    
    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    restore_verification_msg = restore_verification(email=email, password=password,
                    first_name=first_name, last_name=last_name)
    
    if restore_verification_msg[0]:
        return redirect("/login")
    
    message = restore_verification_msg[1]
    return render_template("restore.html", message=message,
                           first_name=first_name,  last_name=last_name,
                           email=email)

# Register routes

@app.route('/register')
def register_page():
    if session.get("user_id", "") != "":
        return redirect("/")
    
    return render_template("register.html")

@app.route('/register_verification', methods=['POST'])
def register_ver():
    if session.get("user_id", "") != "":
        return redirect("/")
    
    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    register_verification_msg = register_verification(email=email, password=password,
                    first_name=first_name, last_name=last_name)
    
    if register_verification_msg[0]:
        return redirect("/login")
    
    message = register_verification_msg[1]
    return render_template("register.html", message=message,
                           first_name=first_name,  last_name=last_name,
                           email=email)

# Home tasks api routes

@app.route('/read_name')
def read_first_name():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    user_id = session['user_id'][0][0]
    name = get_first_name(user_id)
    return name

@app.route('/read_tasks', methods=['GET'])
def read():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    user_id = session['user_id'][0][0]
    rows = read_tasks(user_id=user_id)
    return rows

@app.route('/add_task', methods=['POST'])
def add():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    user_id = session['user_id'][0][0]
    data = request.get_json()
    add_task(user_id, data)
    return "Add task succeeded"

@app.route('/delete_task', methods=['POST'])
def delete():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    data = request.get_json()
    delete_task(data)
    return "Delete task succeeded"

@app.route('/update_status', methods=['POST'])
def status_update():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    data = request.get_json()
    update_status(data)
    return "Update status succeeded"

@app.route('/update_task', methods=['POST'])
def update():
    if session.get("user_id", "") == "":
        return redirect("/login")
    
    data = request.get_json()
    update_task(data)
    return "Update task succeeded"
    
    
if __name__ == '__main__':
    app.run(debug=True)