@echo off
set PYTHONIOENCODING=utf8

if not exist ".git" (
    git init
    if "%SOURCE_REPO%"=="" (
        git remote add origin https://github.com/zRitsu/Danganronpa-1-2-Pt-Br-Translation-Installer-Wizard.git
    ) else (
        git remote add origin %SOURCE_REPO%
    )
    git fetch origin
    git checkout -b main -f --track origin/main
) else (
    git reset --hard
    git pull --allow-unrelated-histories -X theirs
)
