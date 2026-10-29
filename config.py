"""Configuración global y rutas persistentes del programa.

Los datos se guardan en una carpeta del usuario (no en una carpeta temporal),
de modo que sobreviven al cerrar el programa o al reconstruir el .exe.

  Windows : %LOCALAPPDATA%\\BrigadasMedicas
  Linux   : ~/.local/share/BrigadasMedicas
  Pruebas : variable de entorno BRIGADAS_DATA_DIR
"""
import os
import sys
from pathlib import Path

APP_NAME = "Expedientes MdM"
APP_SHORT = "Expedientes MdM"
APP_FOLDER = "BrigadasMedicas"
DB_NAME = "brigadas.db"
SCHEMA_VERSION = 1

DISCLAIMER = ("Formato clínico digital de uso interno de la brigada. "
              "No constituye un formulario oficial de la Secretaría de Salud.")


def resource_path(relative: str) -> Path:
    """Ruta a un recurso empaquetado (funciona en desarrollo y dentro del .exe)."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / relative
    return Path(__file__).resolve().parent / relative


def _read_version() -> str:
    """Versión única del programa: el archivo VERSION (también va dentro del .exe)."""
    try:
        return resource_path("VERSION").read_text(encoding="utf-8").strip() or "desconocida"
    except OSError:
        return "desconocida"


APP_VERSION = _read_version()


def data_dir() -> Path:
    env = os.environ.get("BRIGADAS_DATA_DIR")
    if env:
        path = Path(env)
    elif os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or str(Path.home())
        path = Path(base) / APP_FOLDER
    else:
        path = Path.home() / ".local" / "share" / APP_FOLDER
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path() -> Path:
    return data_dir() / DB_NAME


def backups_dir() -> Path:
    p = data_dir() / "respaldos"
    p.mkdir(parents=True, exist_ok=True)
    return p


def exports_dir() -> Path:
    p = data_dir() / "exportaciones"
    p.mkdir(parents=True, exist_ok=True)
    return p


def log_path() -> Path:
    return data_dir() / "errores.log"
