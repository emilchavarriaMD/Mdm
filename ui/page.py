"""Clase base de las pantallas (páginas) del programa."""
from tkinter import ttk


class Page(ttk.Frame):
    nav_key = ""

    def __init__(self, app):
        super().__init__(app.content)
        self.app = app
        self.db = app.db

    # Se llama cada vez que la página se muestra.
    def on_show(self, **kw):
        pass

    # Devuelve False si el usuario decide quedarse (p. ej. cambios sin guardar).
    def can_leave(self):
        return True

    # Se llama tras restaurar una copia de seguridad o cambiar catálogos.
    def refresh(self):
        pass

    # Ctrl+S
    def on_save_shortcut(self):
        pass
