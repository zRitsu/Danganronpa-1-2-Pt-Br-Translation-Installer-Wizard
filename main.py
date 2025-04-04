import os
import shutil
import traceback
import webbrowser

import FreeSimpleGUI as sg
from psutil import disk_partitions

sg.change_look_and_feel("Reddit")

icon_file = "./icon.ico"

def get_disk_partitions():
    partitions = disk_partitions()
    drives = []
    for partition in partitions:
        if "fixed" in partition.opts:
            drives.append(partition.device)
    return drives

def check_dir(base_file, directory):
    for f in reversed(os.listdir(directory)):
        if f.startswith(base_file):
            return f

def run():

    with open("install_message.txt", encoding="utf-8") as f:
        text = f.read()

    with open("title_message.txt", encoding="utf-8") as f:
        title = f.read()

    base_file = [f for f in os.listdir("PATCH_FILE") if f.endswith((".wad", ".patch"))][0].split("keyboard")[0] + "keyboard"

    current_file = None

    for drive_letter in get_disk_partitions():

        if not os.path.isdir((steam_apps_dir:=os.path.join(drive_letter, "/SteamLibrary/steamapps/common"))):
            continue

        for d in os.listdir(steam_apps_dir):

            if "danganronpa" not in d.lower():
                continue

            if file:=check_dir(base_file, game_dir:=os.path.join(steam_apps_dir, d)):
                current_file = os.path.join(game_dir, file)
                break

        if current_file:
            break

    if not current_file:

        for d in os.listdir(os.environ["PROGRAMFILES"]):

            if "danganronpa" not in d.lower():
                continue

            if file:=check_dir(base_file, game_dir:=os.path.join(os.environ["PROGRAMFILES"], d)):
                current_file = os.path.join(game_dir, file)
                break

    left_column = [
        [sg.Image("logo.png")]
    ]

    right_column = [
        [sg.Multiline(text, disabled=True, size=(60, 13), background_color="white",
                      font=("Helvetica", 10))],
        [sg.Text("Diretório do game:")],
        [
            sg.InputText(enable_events=True, key="game_dir", size=(51, 1), default_text=current_file, readonly=True),
            sg.FolderBrowse("Procurar", font=("Helvetica", 10, "bold"))
        ],
        [
            sg.Button("Discord Server", font=('Arial Black', 12), button_color="MediumPurple3", key="discord_server"),
            sg.Push(),
            sg.Button("Instalar", key="install", font=('Arial Black', 12)),
            sg.Button("Cancelar", font=('Arial Black', 12)),
        ]
    ]

    layout = [
        [sg.Column(left_column, element_justification='center', expand_x=True, expand_y=True),
         sg.Column(right_column)]
    ]

    installer_window = sg.Window(
        title,
        layout=layout,
        icon=icon_file,
    )

    while True:

        try:

            event, values = installer_window.read()

            if event in (sg.WIN_CLOSED, 'exit', 'Cancelar', sg.WIN_CLOSE_ATTEMPTED_EVENT):
                installer_window.close()
                return

            if event == "game_dir":
                if not (file:=check_dir(base_file, values["game_dir"])):
                    installer_window["install"].update(disabled=True)
                    sg.Popup('O diretório selecionado não contém os arquivos do jogo!', font=('Arial Black', 9), title="Erro!", icon=icon_file)
                else:
                    installer_window["install"].update(disabled=False)
                    current_file = os.path.join(values["game_dir"], file)

            elif event == "discord_server":
                webbrowser.open("https://discord.gg/gHqMmXRX3t")

            elif event == "install":

                current_dir = os.path.dirname(current_file)

                if not os.path.isdir(current_dir):
                    sg.Popup(f"O diretório selecionado não existe!", title="Erro!", icon=icon_file)
                    continue

                if not os.access(current_dir, os.W_OK):
                    sg.Popup(f"O instalador não está com permissão para alterar os arquivos do jogo no "
                                  f"diretório selecionado. Experimente executar o instalador como administrador", title="Erro!", icon=icon_file)
                    continue

                os.makedirs(f"{current_dir}/.backup", exist_ok=True)

                if not os.path.isfile(f"{current_dir}/.backup/{os.path.basename(current_file)}"):
                    shutil.move(current_file, f"{current_dir}/.backup")

                try:
                    os.remove(current_file)
                except FileNotFoundError:
                    pass

                for f in os.listdir(f"./PATCH_FILE"):
                    if not f.startswith(base_file) or not f.endswith(".wad"):
                        continue
                    shutil.copy(f"PATCH_FILE/{f}", current_file)
                    break

                sg.Popup("Não esqueça de selecionar a opção \"Keyboard and Mouse\" no launcher do game.", title="Instalação concluída!", icon=icon_file)
                return

        except Exception as e:
            traceback.print_exc()
            sg.Popup(f"{repr(e)}", title="Erro!", icon=icon_file)

run()
