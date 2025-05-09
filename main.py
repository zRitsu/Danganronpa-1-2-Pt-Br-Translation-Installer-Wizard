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

def scan_dir(directory: str, base_file):

    if not os.path.isdir(directory):
        return

    for d in os.listdir(directory):

        if "danganronpa" not in d.lower():
            continue

        if check_dir(base_file, dr_dir := os.path.join(directory, d)):
            return dr_dir

def run():

    with open("install_message.txt", encoding="utf-8") as f:
        text = f.read()

    with open("title_message.txt", encoding="utf-8") as f:
        title = f.read()

    base_file = [f for f in os.listdir("PATCH_FILE") if f.endswith((".wad", ".patch"))][0].rsplit(".", 1)[0].replace("_us", "")

    game_dir = scan_dir(os.environ["PROGRAMFILES"], base_file) or \
        scan_dir(f'{os.environ["PROGRAMFILES(X86)"]}/Steam/steamapps/common/', base_file)

    if not game_dir:
        for drive_letter in get_disk_partitions():
            if dr_dir:=scan_dir(os.path.join(drive_letter, "/SteamLibrary/steamapps/common"), base_file):
                game_dir = dr_dir
                break

    left_column = [
        [sg.Image("logo.png")]
    ]

    right_column = [
        [sg.Multiline(text, disabled=True, size=(60, 13), background_color="white",
                      font=("Helvetica", 10))],
        [sg.Text("Diretório do game:")],
        [
            sg.InputText(enable_events=True, key="game_dir", size=(51, 1), default_text=game_dir, readonly=True),
            sg.FolderBrowse("Procurar", font=("Helvetica", 10, "bold"))
        ],
        [
            sg.Button("Discord Server", font=('Arial Black', 12), button_color="MediumPurple3", key="discord_server"),
            sg.Push(),
            sg.Button("Instalar", key="install", font=('Arial Black', 12), disabled=not game_dir),
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
                if not check_dir(base_file, values["game_dir"]):
                    installer_window["install"].update(disabled=True)
                    sg.popup('O diretório selecionado não contém os arquivos do jogo!', font=('Arial Black', 9), title="Erro!", icon=icon_file)
                else:
                    installer_window["install"].update(disabled=False)
                    game_dir = values["game_dir"]

            elif event == "discord_server":
                webbrowser.open("https://discord.gg/gHqMmXRX3t")

            elif event == "install":

                if not os.path.isdir(game_dir):
                    sg.popup(f"O diretório selecionado não existe!", title="Erro!", icon=icon_file)
                    continue

                if not os.access(game_dir, os.W_OK):
                    sg.popup(f"O instalador não está com permissão para alterar os arquivos do jogo no "
                                  f"diretório selecionado. Experimente executar o instalador como administrador", title="Erro!", icon=icon_file)
                    continue

                os.makedirs(f"{game_dir}/.backup", exist_ok=True)

                for f in os.listdir(f"./PATCH_FILE"):

                    if not f.startswith(base_file) or not f.endswith(".wad"):
                        continue

                    if os.path.isfile(new_current_file:=f"{game_dir}/{(f.split('.wad')[0] + '_us.wad')}"):
                        dest_filename = new_current_file
                    else:
                        dest_filename = f

                    wad_filename = os.path.basename(dest_filename)

                    if not os.path.isfile(f"{game_dir}/.backup/{wad_filename}"):
                        try:
                            shutil.move(f"{game_dir}/{wad_filename}", f"{game_dir}/.backup/{wad_filename}")
                        except:
                            traceback.print_exc()
                    else:
                        try:
                            os.remove(f"{game_dir}/{wad_filename}")
                        except FileNotFoundError:
                            pass
                    shutil.copy(f"PATCH_FILE/{f}", dest_filename)
                    break

                sg.popup("Não esqueça de selecionar a opção \"Keyboard and Mouse\" no launcher do game.", title="Instalação concluída!", icon=icon_file)
                return

        except Exception as e:
            traceback.print_exc()
            sg.popup(f"{repr(e)}", title="Erro!", icon=icon_file)

run()
