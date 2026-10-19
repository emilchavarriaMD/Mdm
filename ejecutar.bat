@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
    echo Primero ejecute build.bat una vez para instalar las dependencias.
    pause
    exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" main.py
