import pyttsx3
engine = pyttsx3.init()
with open("msg.txt") as file:
    txt = file.read()
engine.say(txt)
engine.runAndWait()
engine.