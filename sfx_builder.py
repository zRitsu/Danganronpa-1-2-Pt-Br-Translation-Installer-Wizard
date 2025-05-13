import hashlib
import subprocess
import os

from main import default_install_message, default_title_message, copy_examples, detect_patch_base_file

if not detect_patch_base_file():
    os.makedirs("PATCH_FILE", exist_ok=True)
    raise Exception(
        "Você deve incluir o arquivo de tradução na pasta PATCH_FILE (que termine com a extensão .wad ou .patch ou .cpk)"
    )

if not os.path.isfile("install_message.txt"):
    with open("install_message.txt", "w", encoding="utf-8") as f:
        f.write(default_install_message)

if not os.path.isfile("title_message.txt"):
    with open("title_message.txt", "w", encoding="utf-8") as f:
        f.write(default_title_message)

copy_examples(["icon.ico", "logo.png"])

filelist = [
    "install_message.txt",
    "title_message.txt",
    "icon.ico",
    "logo.png",
]

winrar_path = os.path.join(os.environ["PROGRAMFILES"], "WinRAR/WinRAR.exe")

config_text = f"""
; Instalador da tradução.
Setup=dr_wizard\\setup.exe
TempMode
Silent=2
Overwrite=1
"""

with open("config.sfx", "w") as config_file:
    config_file.write(config_text)

try:
    os.remove("DR_trad_installer.exe")
except FileNotFoundError:
    pass

patch_file_extensions = ('.wad', '.patch', '.cpk')

for root, dirs, files in os.walk("dr_wizard"):
    for file in files:
        filelist.append(os.path.join(root, file))

for root, _, patch_dir in os.walk("PATCH_FILE"):
    for file in patch_dir:
        if file.lower().endswith(patch_file_extensions):
            filepath = os.path.join(root, file)
            filelist.append(filepath)

with open("filelist.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(filelist))

subprocess.run([
    winrar_path, "a", "-sfx", r"-iiconicon.ico", "-zconfig.sfx", "DR_trad_installer.exe", "-v4000m",
    "@filelist.txt",
], check=True)

os.remove("config.sfx")
os.remove("filelist.txt")

sha256 = hashlib.sha256()

with open("DR_trad_installer.exe", "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256.update(chunk)

hash_value  = sha256.hexdigest()

with open("sha256.txt", "w") as sha_file:
    sha_file.write(hash_value)
