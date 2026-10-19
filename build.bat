@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ============================================================
echo   Registro Clinico de Brigadas Medicas - Crear el programa .exe
echo ============================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] No se encontro Python. Instale Python 3.10 o superior desde python.org
    echo         y marque la casilla "Add python.exe to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo [1/4] Creando entorno virtual...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 goto :error
)
call ".venv\Scripts\activate.bat"

echo [2/4] Instalando dependencias...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [3/4] Ejecutando pruebas automaticas...
python -m unittest tests.test_all
if errorlevel 1 (
    echo [ERROR] Las pruebas fallaron. No se genera el .exe.
    pause
    exit /b 1
)

echo [4/4] Generando el .exe (puede tardar unos minutos)...
pyinstaller --noconfirm --clean BrigadasMedicas.spec
if errorlevel 1 goto :error

echo.
echo ============================================================
echo   LISTO. Su programa esta en:  dist\BrigadasMedicas\BrigadasMedicas.exe
echo   Puede copiar la carpeta dist\BrigadasMedicas completa a otra computadora.
echo   Sus datos se guardan en: %%LOCALAPPDATA%%\BrigadasMedicas
echo ============================================================
pause
exit /b 0

:error
echo.
echo [ERROR] Algo fallo. Revise los mensajes de arriba.
pause
exit /b 1
