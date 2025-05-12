import os
from cx_Freeze import setup, Executable

from main import default_title_message, copy_examples

copy_examples(["icon.ico"])

try:
    with open("title_message.txt", encoding='utf-8') as f:
        title = f.read()
except FileNotFoundError:
    with open("title_message.txt", "w", encoding="utf-8") as f:
        f.write(default_title_message)
    title = default_title_message

setup(
    name = title,
    version = "1.0",
    #description = "",
        options = {"build_exe": {
        'include_files': [],
        'include_msvcr': True,
        "build_exe": "dr_wizard",
    }},
    executables = [Executable("main.py", icon="icon.ico", target_name="setup.exe", base="Win32GUI")]
)
