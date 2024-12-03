import requests
import time

while True:
    try:
        cmd = requests.get("http://127.0.0.1:5000/command")
        print(cmd)
    except: pass
    time.sleep(2)