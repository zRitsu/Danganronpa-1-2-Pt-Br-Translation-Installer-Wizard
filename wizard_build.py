import os
from cx_Freeze import setup, Executable

if os.path.isfile("./icon.ico"):
    icon_file = "icon.ico"
else:
    icon_file = None

with open("title_message.txt", encoding='utf-8') as f:
    title = f.read()

setup(
    name = title,
    version = "1.0",
    #description = "",
        options = {"build_exe": {
        'include_files': [],
        'include_msvcr': True,
        "build_exe": "dr_wizard",
    }},
    executables = [Executable("main.py", icon=icon_file, target_name="setup.exe", base="Win32GUI")]
)
