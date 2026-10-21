"""Selector de medicamentos para el plan: se elige uno de la lista (o se escribe otro), se agrega, y se repite
tantas veces como haga falta. Cada medicamento agregado queda en su propia fila, editable y con botón para quitarlo."""
import tkinter as tk
from tkinter import ttk

from services import cie11_catalog as cat
from services import medicamentos
from ui import theme, widgets


class MedPicker(ttk.Frame):
    def __init__(self, master, iniciales=(), on_change=None):
        super().__init__(master)
        self._on_change = on_change
        self._filas = []                      # [(frame, EntryField)]
        ttk.Label(self, text="Medicamentos (opcional): elija uno, pulse «Agregar» y repita con los demás. Se escriben al final "
                  "del plan sin cambiar el texto de arriba. Puede corregir la dosis, la frecuencia o los días en cada fila.",
                  style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(4, 2))
        self.combo = widgets.ComboField(barra, [""] + medicamentos.MEDICAMENTOS, readonly=False, width=90)
        self.combo.pack(side="left", fill="x", expand=True)
        self.combo.bind("<KeyRelease>", self._filtrar)
        self.combo.bind("<Return>", lambda e: self.agregar())
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.agregar())
        ttk.Button(barra, text="Agregar", command=self.agregar).pack(side="left", padx=(6, 0))
        self.lista = ttk.Frame(self)
        self.lista.pack(fill="x")
        for t in iniciales:
            self._nueva_fila(t)

    def _filtrar(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        q = cat.plain(self.combo.get_value())
        todos = medicamentos.MEDICAMENTOS
        self.combo.set_values([x for x in todos if q in cat.plain(x)] or todos if q else [""] + todos)

    def agregar(self):
        """Pasa el medicamento elegido (o escrito) a la lista y deja el selector libre para el siguiente."""
        texto = self.combo.get_value().strip()
        if not texto:
            return
        self._nueva_fila(texto)
        self.combo.set_value("")
        self.combo.set_values([""] + medicamentos.MEDICAMENTOS)
        self.combo.focus_set()
        self._cambio()

    def _nueva_fila(self, texto):
        fila = ttk.Frame(self.lista)
        fila.pack(fill="x", pady=1)
        ttk.Label(fila, text="•").pack(side="left", padx=(2, 4))
        ent = widgets.EntryField(fila, width=90)
        ent.set_value(texto)
        ent.pack(side="left", fill="x", expand=True)
        ent.bind("<KeyRelease>", lambda e: self._cambio())
        item = (fila, ent)
        ttk.Button(fila, text="Quitar", width=7, command=lambda: self._quitar(item)).pack(side="left", padx=(6, 0))
        self._filas.append(item)

    def _quitar(self, item):
        item[0].destroy()
        self._filas.remove(item)
        self._cambio()

    def _cambio(self):
        if self._on_change:
            self._on_change()

    def valores(self):
        return [e.get_value().strip() for _f, e in self._filas if e.get_value().strip()]

    def poner(self, lineas):
        for f, _e in list(self._filas):
            f.destroy()
        self._filas.clear()
        for t in lineas:
            self._nueva_fila(t)
