"""Funciones auxiliares compartidas por varias pantallas."""
from datetime import datetime


def now_hhmm():
    return datetime.now().strftime("%H:%M")
