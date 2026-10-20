"""Expedientes MdM – punto de entrada.

Ejecutar en desarrollo:   python main.py
Genera el .exe con:       build.bat
"""
import sys
import traceback


def _fatal(title, message):
    """Muestra un error claro incluso si la interfaz principal no pudo iniciar."""
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:  # noqa: BLE001
        print(f"{title}: {message}", file=sys.stderr)


def _dpi_aware():
    """Texto nítido en pantallas de alta resolución (Windows)."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:  # noqa: BLE001
            pass


def main():
    if sys.version_info < (3, 10):
        _fatal("Python demasiado antiguo", "Este programa necesita Python 3.10 o superior (instale una versión nueva desde python.org).")
        return 1
    try:
        import tkinter  # noqa: F401
    except ImportError:
        _fatal("Falta Tkinter", "Esta instalación de Python no incluye Tkinter. Reinstale Python desde python.org con la opción «tcl/tk and IDLE».")
        return 1
    _dpi_aware()
    try:
        import config
        from database import Database
        db = Database(config.db_path())
    except Exception as exc:  # noqa: BLE001
        _fatal("No se pudo abrir la base de datos",
               f"{exc}\n\nVerifique que la carpeta de datos exista y tenga permisos de escritura.")
        return 1
    try:
        from ui.app import App
        App(db).run()
    except Exception as exc:  # noqa: BLE001
        try:
            import config
            with open(config.log_path(), "a", encoding="utf-8") as fh:
                fh.write(traceback.format_exc())
            where = f"\n\nDetalle técnico guardado en:\n{config.log_path()}"
        except Exception:  # noqa: BLE001
            where = ""
        _fatal("Error al iniciar el programa", f"{exc}{where}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
