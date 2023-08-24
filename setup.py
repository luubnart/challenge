import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "includes": ["tkinter", "shutil", "win10toast", "psutil", "watchdog", "signal"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Scythe Control - Anti Ransomware",
    version="0.1",
    description="Challenge FIAP 2022",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable("main.py", base=base)]
)
