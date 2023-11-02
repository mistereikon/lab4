from flask import request, render_template, redirect, url_for, session, flash, jsonify
from app import app
import json
from datetime import datetime, timedelta

def load_users():
    try:
        with open("users.json", "r") as users_file:
            return json.load(users_file)
    except FileNotFoundError:
        return {}

def load_cookies():
    try:
        with open("cookies.json", "r") as cookies_file:
            return json.load(cookies_file)
    except FileNotFoundError:
        return {}

users = load_users()
cookies = load_cookies()

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username] == password:
        session["username"] = username
        flash("Login successful!", "success")
        return redirect("/info")
    else:
        flash("Login failed. Please check your credentials.", "error")
        return redirect("/")

@app.route("/info")
def info():
    if "username" in session:
        username = session["username"]
        user_cookies = cookies.get(username, {})
        cookie_data = [{"key": key, "value": value, "expiry": expiry, "created_at": created_at}
                       for key, (value, expiry, created_at) in user_cookies.items()]
        return render_template("info.html", username=username, cookies=cookie_data)
    else:
        flash("You need to log in first.", "error")
        return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    if "username" in session:
        session.pop("username")
        flash("You have been logged out.", "success")
    return redirect("/")

@app.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" in session:
        username = session["username"]
        key = request.form.get("key")
        value = request.form.get("value")
        expiry = int(request.form.get("expiry"))

        if username not in cookies:
            cookies[username] = {}
        cookies[username][key] = (value, expiry, datetime.now().isoformat())
        save_cookies()
        flash("Cookie added successfully.", "success")
    return redirect("/info")

@app.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "username" in session:
        username = session["username"]
        key = request.form.get("key")

        if username in cookies and key in cookies[username]:
            del cookies[username][key]
            save_cookies()
            flash("Cookie deleted successfully.", "success")
    return redirect("/")

@app.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" in session:
        username = session["username"]

        if username in cookies:
            cookies[username] = {}
            save_cookies()
            flash("All cookies deleted successfully.", "success")
    return redirect("/")

@app.route("/change_password", methods=["POST"])
def change_password():
    if "username" in session:
        username = session["username"]
        new_password = request.form.get("new_password")
        users[username] = new_password
        save_users()
        flash("Password changed successfully.", "success")
    return redirect("/")

def save_users():
    with open("users.json", "w") as users_file:
        json.dump(users, users_file)

def save_cookies():
    with open("cookies.json", "w") as cookies_file:
        json.dump(cookies, cookies_file)

if __name__ == '__main__':
    app.run(debug=True)
