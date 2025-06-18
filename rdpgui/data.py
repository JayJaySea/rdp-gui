from pathlib import Path
import subprocess
import os
import shutil

DEBUG=os.getenv("DEBUG")
DATA_DIR=os.path.join(Path.home(), ".local", "share", "rdpgui")
MEMORY_FILE=os.path.join(DATA_DIR, "memory.json")

if DEBUG:
    DATA_DIR=os.path.join(Path.cwd(), "data")

def init():
    if os.path.exists(DATA_DIR) and not DEBUG:
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    root_dir = Path(__file__).resolve().parent

    fonts_src = os.path.join(root_dir, "fonts")
    fonts_dest = os.path.join(DATA_DIR, "fonts")
    shutil.copytree(fonts_src, fonts_dest, dirs_exist_ok=True)

    style_src = os.path.join(root_dir, "style", "main.scss")
    style_dest = os.path.join(DATA_DIR, "style.css")
    command = ["sassc", style_src, style_dest]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)
        exit(result.returncode)
