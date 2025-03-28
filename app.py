from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

USER_DATA = {"finmighty1112@gmail.com": "fin0021@10"}
EXCEL_FILE = "static/data.xlsx"

if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists(EXCEL_FILE):
    pd.DataFrame(columns=["Column1", "Column2"]).to_excel(EXCEL_FILE, index=False)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email, password = data["email"], data["password"]
    
    if email in USER_DATA and USER_DATA[email] == password:
        session["user"] = email
        return jsonify({"status": "success", "redirect": "/download_excel"})
    return jsonify({"status": "fail"})

@app.route("/download_excel")
def download_excel():
    if "user" not in session:
        return redirect(url_for("home"))
    
    return send_file(EXCEL_FILE, as_attachment=True)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
