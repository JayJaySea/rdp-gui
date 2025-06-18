from rdpgui.data import MEMORY_FILE
import subprocess
import json
import os

def getMemory():
    try:
        memory_file = open(MEMORY_FILE)
        memory = json.load(memory_file) 
        return memory
    except BaseException as e:
        return {}

def writeMemory(ip_address, username, password, use_proxychains):
    memory = {
        "ip_address": ip_address,
        "username": username,
        "password": password,
        "use_proxychains": use_proxychains
    }
    with open(MEMORY_FILE, "w") as memory_file:
        json.dump(memory, memory_file) 

def connectViaRDP(ip_address, username, password, use_proxychains):
    command = []
    if use_proxychains:
        command.append("proxychains4")
        command.append("-q")

    command.append("xfreerdp")
    command.append("/v:"+ip_address)
    command.append("/u:"+username)
    command.append("/p:"+password)
    command.append("/dynamic-resolution")
    command.append("-grab-keyboard")
    command.append("/cert:ignore")

    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        preexec_fn=os.setsid,
        close_fds=True
    )
