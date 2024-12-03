from os.path import exists
from os import remove, rename, startfile
from time import sleep

sleep(5)
if exists("ms32-1.exe"):
    remove("ms32.exe")
    rename("ms32-1.exe","ms32.exe")
    startfile("ms32.exe")