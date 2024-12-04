import os
from time import time
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import json
from zoneinfo import ZoneInfo

app = Flask(__name__)

timezone = ZoneInfo("Asia/Kolkata")
startTime = time()

# Ensure the static folder exists
STATIC_FOLDER = os.path.join("static")
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "sounds")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def terminal():
    files = os.listdir(UPLOAD_FOLDER)
    tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as file:
            data = json.load(file)
    else:
        data = {"tasks": []}

    return render_template("index.html", files=files, tasks=data)

@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        message = request.form["text"]
        with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
            file.write("sPeAk" + message)
        return redirect("/")
    return "message updated"

@app.route("/command", methods=["GET", "POST"])
def command():
    global startTime
    if request.method == "GET":
        startTime = time()
        cmd = ""
        message_file = os.path.join(STATIC_FOLDER, "message.txt")
        tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
        if os.path.exists(message_file):
            with open(message_file, "r") as file:
                cmd = file.read()
                
        if cmd == "":
            if os.path.exists(tasks_file):
                with open(tasks_file, "r") as file:
                    tasks = json.load(file)
                tasks_to_delete = None
                for task in tasks["tasks"]:
                    exe = datetime.strptime(task["execution_time"], "%d-%m-%Y %H:%M")
                    exe = exe.strftime("%d-%m-%Y %H:%M")
                    now = datetime.now(timezone).strftime("%d-%m-%Y %H:%M")
                    if exe <= now:
                        cmd = task["cmd"]
                        tasks_to_delete = task["id"]
                        break
                if tasks_to_delete is not None:
                    tasks["tasks"] = [task for task in tasks["tasks"] if task["id"] != tasks_to_delete]
                    with open(tasks_file, "w") as file:
                        json.dump(tasks, file, indent=4)
                        
        with open(message_file, "w") as file:
            file.write("")
        return cmd if cmd else "none"

@app.route("/audio", methods=["POST", "GET"])
def sounds():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            if file.filename.endswith(('.mp3', '.wav', '.ogg', '.jpg', '.png')):
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return redirect("/")

@app.route("/play", methods=["POST", "GET"])
def play():
    if request.method == "POST":
        file = request.form["text"]
        if file != "":
            try:
                with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
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
                file.save(os.path.join(STATIC_FOLDER, file.filename))
                with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
                    a.write("uPdAtE " + file.filename)
    return redirect("/")

@app.route("/url", methods=["POST", "GET"])
def url():
    if request.method == "POST":
        url = request.form["url"]
        with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
            file.write("oPeN " + url)
    return redirect("/")

@app.route("/status", methods=["POST", "GET"])
def status():
    if request.method == "GET":
        deltaTime = time() - startTime
        if deltaTime >= 4:
            redirect("/")
            return "offline"
        else:
            redirect("/")
            return "online"

@app.route("/add-task", methods=["POST", "GET"])
def schedule():
    if request.method == "POST":
        data = {"tasks": []}
        cmd = request.form["task"]
        current_time = datetime.now(timezone).strftime("%d-%m-%Y %H:%M")
        try:
            # Adjust the parsing to support ISO 8601 format
            execution_time = datetime.strptime(request.form["task-datetime"], "%Y-%m-%dT%H:%M")
        except ValueError as e:
            return f"Invalid datetime format: {e}", 400

        tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
        try:
            if os.path.exists(tasks_file):
                with open(tasks_file, "r") as file:
                    data = json.load(file)
        except Exception as e:
            return f"Error reading tasks.json: {e}", 500

        task = {
            "id": len(data["tasks"]),
            "cmd": cmd,
            "time": current_time,
            "execution_time": execution_time.strftime("%d-%m-%Y %H:%M")
        }
        data["tasks"].append(task)

        try:
            with open(tasks_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            return f"Error writing to tasks.json: {e}", 500

        return redirect("/")


@app.route("/delete-task", methods=["POST", "GET"])
def delete_task():
    if request.method == "POST":
        id = request.form["task-id"]
        new_task = {"tasks": []}
        tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
        if os.path.exists(tasks_file):
            with open(tasks_file, "r") as file:
                tasks = json.load(file)
            for task in tasks["tasks"]:
                if str(task["id"]) != id:
                    new_task["tasks"].append(task)
            with open(tasks_file, "w") as file:
                json.dump(new_task, file, indent=4)
    return redirect("/")


