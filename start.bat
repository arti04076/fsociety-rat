@echo off
echo installing all required python modules

REM Sicherstellen, dass pip funktioniert
python -m ensurepip --upgrade
python -m pip install --upgrade pip

REM Python-Module über pip installieren

pip install discord.py pillow pyautogui requests cryptography
REM Optional: falls Pillow mehrfach erwähnt wurde
pip install --upgrade pillow

REM Optional: Installiere wichtige Tools
pip install --upgrade git+https://github.com/sherlock-project/sherlock.git
pip install --upgrade git+https://github.com/Datalux/Osintgram.git

echo.
echo all modules have been installed
python fsocietyrat.py
pause