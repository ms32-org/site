# import requests
# import time

# while True:
#     try:
#         cmd = requests.get("http://127.0.0.1:5000/command")
#         print(cmd.content.decode("utf-8"))
#     except: pass
#     time.sleep(1)
import pyttsx3
engine = pyttsx3.init()
with open("msg.txt") as file:
    txt = file.read()
engine.say(txt)
engine.runAndWait()