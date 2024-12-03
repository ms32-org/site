import requests as rq
from threading import Thread
import os
from time import sleep
url = "http://127.0.0.1:5000/"
terminate = False
def hit(url:str):
    if not terminate:
        return rq.get(url)

def say(txt):
    with open("msg.txt", "wt") as msg:
        msg.write(txt)
    os.startfile("new.exe")
def main():
    while not terminate:
        cmd = hit(url+"command").content.decode("utf-8")
        print(cmd,type(cmd))
        if "sPeAk" in cmd:
            txt = cmd.replace("sPeAk","")
            saying = Thread(target=say,args=(txt,))
            saying.start()
            saying.join()
            
        sleep(1)

main()