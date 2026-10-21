@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
rem Expedientes MdM: la primera vez prepara todo solo (necesita internet); despues solo abre el programa.

if exist ".venv\Scripts\pythonw.exe" if exist ".venv\listo.txt" goto :abrir

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY (
    echo [ERROR] No se encontro Python. Instale Python 3.10 o superior desde python.org
    echo         y marque la casilla "Add python.exe to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo Preparando el programa por primera vez. Puede tardar unos minutos...
if not exist ".venv\Scripts\python.exe" (
    %PY% -m venv .venv
    if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m compileall -q . >nul 2>nul
echo listo> ".venv\listo.txt"

:abrir
start "" ".venv\Scripts\pythonw.exe" main.py
exit /b 0

:error
echo.
echo [ERROR] No se pudo preparar el programa. Revise la conexion a internet y vuelva a intentar.
pause
exit /b 1
