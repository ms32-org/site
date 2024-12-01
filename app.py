import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "sounds")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def terminal():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)

@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        message = request.form["text"]
        with open(os.path.join(os.getcwd(), "message.txt"), "w") as file:
            file.write("sPeAk '" + message)
        return redirect("/")
    return "message updated"

@app.route("/command", methods=["GET", "POST"])
def command():
    if request.method == "GET":
        with open(os.path.join(os.getcwd(), "message.txt"), "r") as file:
            cmd = file.read()
        return cmd

@app.route("/audio", methods=["POST"])
def sounds():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename:
            if file.filename.endswith(('.mp3', '.wav')):
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            else:
                return jsonify({"error": "Invalid file type. Please upload an audio file."}), 400
        return redirect("/")

@app.route("/play", methods=["POST", "GET"])
def play():
    if request.method == "POST":
        file = request.form["text"]
        if file != "":
            try:
                with open(os.path.join(os.getcwd(), "message.txt"), "w") as a:
                    a.write("pLaY " + file)
            except:
                pass
    return redirect("/")

@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        file = request.form["text"]
        if file != "":
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, file))
            except:
                pass
    return redirect("/")

@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            if file.filename.endswith(".exe"):
                file.save(os.path.join(os.getcwd(), file.filename))
                with open(os.path.join(os.getcwd(), "message.txt"), "w") as a:
                    a.write("uPdAtE " + file.filename)

@app.route("/url", methods=["POST", "GET"])
def url():
    if request.method == "POST":
        url = request.form["url"]
        with open(os.path.join(os.getcwd(), "message.txt"), "w") as file:
            file.write("oPeN " + url)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
