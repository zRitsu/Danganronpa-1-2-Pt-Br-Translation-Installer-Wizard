import subprocess
import os


if not os.path.isfile("./dist/main.exe"):
    os.system("pyinstaller -F -i icon.ico -c --noconsole main.py")
os.rename("./dist/main.exe", "setup.exe")

if not [w for w in os.listdir("./PATCH_FILE") if w.endswith((".wad", ".patch")) and os.path.isfile(f"./PATCH_FILE/{w}")]:
    raise Exception(
        "Você deve incluir o arquivo de tradução na pasta PATCH_FILE (que inicie com nome dr1_data_keyboard ou dr2_data_keyboard que termine com extensão .wad ou .patch)"
    )

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
