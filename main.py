import os
import shutil
import tempfile
import traceback
import webbrowser
from typing import List

import FreeSimpleGUI as sg
from psutil import disk_partitions

sg.change_look_and_feel("Reddit")

icon_file = "./icon.ico"

temp_directory = tempfile.gettempdir()

PATCH_FILE_DIR = "./PATCH_FILE"

patch_extensions = (".wad", ".cpk", ".patch",)

def get_disk_partitions():
    partitions = disk_partitions()
    drives = []
    for partition in partitions:
        if "fixed" in partition.opts:
            drives.append(partition.device)
    return drives

def check_dir(base_file, directory):

    if not os.path.isfile(full_path:=os.path.join(directory, base_file)):
        return None

    return full_path

def copy_examples(filenames: List[str]):
    for filename in filenames:
        if not os.path.isfile(filename):
            shutil.copy(f"{filename}.example", filename)

def detect_patch_base_file():
    for dir_, subdirs, files in os.walk(PATCH_FILE_DIR):
        for file in files:
            if file.endswith(patch_extensions):
                return os.path.join(dir_[len(PATCH_FILE_DIR) + 1:], file)
    return None

def scan_dir(directory: str, base_file):
    if not os.path.isdir(directory):
        return

    for d in os.listdir(directory):

        full_path = os.path.join(directory, d)

        if "danganronpa" not in d.lower():
            continue

        if not os.path.isfile(os.path.join(full_path, base_file)):
            continue

        return full_path

    return None

default_title_message = "Instalar Tradução: Danganronpa 2 PT-BR v4.2 beta"

default_install_message = """
Traduzido por Kibou Project

Visite o nosso servidor do Discord: https://discord.gg/aE7yGJz

-------- Notas da Versão 4.2 ---------------

- Versão beta - 34

- Melhorias no diálogo da personagem Sonia Nevermind

-------- Conteúdo Atual da tradução -------------

- História completa

- Modo ilha

- Novel

- Garota Mágica Monomi

- Freetimes

- Itens e Habilidades

- Descrição de personagens na Novel

- Gamefix: Animação do Monokuma file #3

- Novo Textbox (ainda em fase experimental)
"""

def run():

    copy_examples(["icon.ico", "logo.png"])

    try:
        with open("install_message.txt", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        sg.popup(f"{e}", title="Erro!", icon=icon_file)
        with open("install_message.txt", "w", encoding="utf-8") as f:
            f.write(default_install_message)
        text = "Verifique o arquivo install_message.txt"

    try:
        with open("title_message.txt", encoding="utf-8") as f:
            title = f.read()
    except Exception as e:
        sg.popup(f"{e}", title="Erro!", icon=icon_file)
        with open("title_message.txt", "w", encoding="utf-8") as f:
            f.write(default_title_message)
        title = "Verifique o arquivo title_message.txt"

    base_file = detect_patch_base_file()

    if not base_file:
        sg.popup("Não há arquivos do jogo nessa instalação!\n"
                 "Por favor entre em contato com a equipe de tradução do projeto.", title="Erro!", icon=icon_file)
        return

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
            sg.FolderBrowse("Procurar", font=("Helvetica", 10, "bold"), key="select_game_dir")
        ],
        [
            sg.Button("Discord Server", font=('Arial Black', 12), button_color="MediumPurple3", key="discord_server"),
            sg.Push(),
            sg.Button("Instalar", key="install", font=('Arial Black', 12), disabled=not game_dir),
            sg.Button("Cancelar", key="cancel", font=('Arial Black', 12)),
        ]
    ]

    layout = [
        [sg.Column(left_column, element_justification='center', expand_x=True, expand_y=True),
         sg.Column(right_column)],
        [sg.Text("", size=(62, 1), key="file_name", font=("Arial", 12), justification='center',
                 background_color="Black", text_color="White")]
    ]

    installer_window = sg.Window(
        title,
        layout=layout,
        icon=icon_file,
    )

    while True:

        try:

            event, values = installer_window.read()

            if event in (sg.WIN_CLOSED, 'exit', 'cancel', sg.WIN_CLOSE_ATTEMPTED_EVENT):
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

                installer_window["install"].update("Instalando...", disabled=True)
                installer_window["cancel"].update(disabled=True)
                installer_window["select_game_dir"].update(disabled=True)

                for root, _, patch_dir in os.walk(PATCH_FILE_DIR):

                    for file in patch_dir:

                        if not file.endswith(patch_extensions):
                            continue

                        f = os.path.join(root, file).rsplit(PATCH_FILE_DIR, 1)[-1]

                        installer_window["file_name"].update(f"Copiando: {f}")
                        installer_window.refresh()

                        if os.path.isfile(new_current_file:=f"{game_dir}/{(f.split('.wad')[0] + '_us.wad')}"):
                            dest_filename = new_current_file
                        else:
                            dest_filename = f"{game_dir}/{f}"

                        if not os.path.isfile(dest_bkp:=f"{game_dir}/.backup{os.path.dirname(f)}"):
                            os.makedirs(dest_bkp, exist_ok=True)
                            try:
                                shutil.move(f"{game_dir}{f}", f"{game_dir}/.backup{f}")
                            except:
                                traceback.print_exc()
                        else:
                            try:
                                os.remove(f"{game_dir}/{f}")
                            except FileNotFoundError:
                                pass

                        shutil.copy(f"{PATCH_FILE_DIR}/{f}", dest_filename)

                sg.popup("Não esqueça de selecionar a opção \"Keyboard and Mouse\" no launcher do game.", title="Instalação concluída!", icon=icon_file)
                return

        except Exception as e:
            traceback.print_exc()
            sg.popup(f"{repr(e)}", title="Erro!", icon=icon_file)

if __name__ == "__main__":
    run()
