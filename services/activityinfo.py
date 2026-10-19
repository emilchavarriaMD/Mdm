"""Registro de un paciente del ATA en ActivityInfo (se abre Chrome y se siguen los pasos del formulario).

El programa NUNCA guarda ni escribe contraseñas: la persona inicia sesión una sola vez en la
ventana de Chrome que se abre (queda guardada en un perfil propio del programa).
"""
import webbrowser

FORM_URL = "https://www.activityinfo.org/app#form/cgagdtzm4cnphz5kmo/newRecord"


def register(db, record_id, parent=None):
    """Abre el formulario de ActivityInfo para este paciente. (Los pasos automáticos se agregan
    después de revisar los campos del formulario.)"""
    open_form()


def open_form():
    """Abre el formulario de nuevo registro en el navegador predeterminado."""
    webbrowser.open(FORM_URL)
