import hashlib
import subprocess
import os


if not [w for w in os.listdir("./PATCH_FILE") if w.endswith((".wad", ".patch")) and os.path.isfile(f"./PATCH_FILE/{w}")]:
    raise Exception(
        "Você deve incluir o arquivo de tradução na pasta PATCH_FILE (que inicie com nome dr1_data_keyboard ou dr2_data_keyboard que termine com extensão .wad ou .patch)"
    )

os.system("pyinstaller -F -i icon.ico -c --noconsole main.py")

try:
    os.remove("./setup.exe")
except (FileExistsError, FileNotFoundError):
    pass

os.rename("./dist/main.exe", "setup.exe")

filelist = [
    "install_message.txt",
    "title_message.txt",
    "setup.exe",
    "icon.ico",
    "logo.png",
    "PATCH_FILE/"
]

winrar_path = os.path.join(os.environ["PROGRAMFILES"], "WinRAR/WinRAR.exe")

config_text = f"""
; Instalador da tradução.
Setup=setup.exe
TempMode
Silent=2
Overwrite=1
"""

with open("config.sfx", "w") as config_file:
    config_file.write(config_text)

subprocess.run([
    winrar_path, "a", "-sfx", r"-iiconicon.ico", "-zconfig.sfx", "DR_trad_installer.exe", *filelist
], check=True)

os.remove("setup.exe")
os.remove("config.sfx")

sha256 = hashlib.sha256()

with open("DR_trad_installer.exe", "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256.update(chunk)

hash_value  = sha256.hexdigest()

with open("sha256.txt", "w") as sha_file:
    sha_file.write(hash_value)
