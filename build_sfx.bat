if not exist venv (
  py -3 -m venv venv
  call "venv\scripts\activate"
  pip install -r requirements.txt
) else (
  call "venv\scripts\activate"
)

python wizard_build.py build
python sfx_builder.py
pause