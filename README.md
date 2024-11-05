# Danganronpa 1/2 Pt-Br Translation Installer Wizard
 Um pequeno instalador da tradução do danganronpa 1 e 2 que fiz para o projeto de tradução da Kibou Project

[![](https://discordapp.com/api/guilds/420923628222414859/embed.png?style=banner2)](https://discord.gg/gHqMmXRX3t)

## Preview:
[![2xrPAnS.md.png](https://iili.io/2xrPAnS.png)](https://iili.io/2xrPAnS.png)

## Features:
* Detecção automática do diretório de instalação de jogos do Daganronpa 1 e 2 da steam ou em diretórios comuns (Não há suporte pra instalação da versão da ms-store).
* Aviso sobre a seleção de diretório inválido do game (evitando possíveis instalações incorretas ocupando espaço em disco).
* No build_sfx: Geração automática do arquivo sha256.txt após build do instalador.
* Em breve: Alteração automática do executável do game pra lidar com a alteração necessária da senha do puzzle: Final Dead Room.

## Como fazer build do instalador sfx com o wizard desse repositório:

* Ter o [Python](https://www.python.org/) 3.9 ou superior instalado e configurado no [PATH](https://entredatos.es/wp-content/uploads/2021/05/word-image-13.png)
* Ter WinRar instalado ([download aqui](https://www.win-rar.com/predownload.html?&L=9)).
* Baixe o conteudo desse repositório pelo botão Code -> Download zip
* Extraia o arquivo baixado
* Caso necessário, edite os arquivos install_message.txt e title_message.txt pra atualizar informações sobre a tradução/projeto
* Copie o arquivo de tradução com nome "dr1_data_keyboard.wad" (ou dr2... etc) pra pasta PATCH_FILES que está nos arquivos extraidos
* Execute o arquivo build_sfx.bat e aguarde o processo concluir, será gerado o arquivo DR_Trad_installer.exe

[![Discord Presence](https://lanyard.cnrad.dev/api/184889853102653440?borderRadius=10px&idleMessage=Nenhuma%20atividade)](https://discord.com/users/184889853102653440)