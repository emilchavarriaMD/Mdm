"""Selector de medicamentos para el plan: se busca (con la lupa) o se elige de la lista A–Z (o se escribe otro), se agrega,
y se repite tantas veces como haga falta. Cada medicamento agregado queda en su propia fila, editable y con botón para
quitarlo."""
import tkinter as tk
from tkinter import ttk

from services import cie11_catalog as cat
from services import medicamentos
from ui import theme, widgets


class _Lupa(tk.Canvas):
    """Lupa dibujada (no depende de emojis ni de la fuente del sistema)."""

    def __init__(self, master):
        try:
            fondo = ttk.Style().lookup("TFrame", "background") or master.cget("background")
        except tk.TclError:
            fondo = "#f0f0f0"
        super().__init__(master, width=22, height=22, highlightthickness=0, bd=0, background=fondo)
        color = "#444444"
        self.create_oval(3, 3, 14, 14, outline=color, width=2)
        self.create_line(13, 13, 19, 19, fill=color, width=3, capstyle="round")


class MedPicker(ttk.Frame):
    MAX_RESULTADOS = 8

    def __init__(self, master, iniciales=(), on_change=None):
        super().__init__(master)
        self._on_change = on_change
        self._filas = []                      # [(frame, EntryField)]
        self._resultados = []
        ttk.Label(self, text="Medicamentos (opcional): búsquelos con la lupa o elíjalos de la lista, y pulse «Agregar» o "
                  "toque el resultado; repita con los demás. Se escriben al final del plan sin cambiar el texto de arriba. "
                  "Puede corregir la dosis, la frecuencia o los días en cada fila.",
                  style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        # búsqueda con lupa
        bus = ttk.Frame(self)
        bus.pack(fill="x", pady=(4, 0))
        _Lupa(bus).pack(side="left", padx=(0, 4))
        self.buscador = widgets.EntryField(bus, width=30)
        self.buscador.pack(side="left", fill="x", expand=True)
        self.buscador.bind("<KeyRelease>", self._buscar)
        self.buscador.bind("<Return>", lambda e: self._agregar_resultado(0))
        self.buscador.bind("<Down>", self._ir_a_resultados)
        self.buscador.bind("<Escape>", lambda e: self._limpiar_busqueda())
        ttk.Label(bus, text="Buscar medicamento (parte del nombre)", style="Muted.TLabel").pack(side="left", padx=(8, 0))
        self.lista_res = tk.Listbox(self, height=1, activestyle="dotbox", exportselection=False, font=theme.FONT_TEXT)
        self.lista_res.bind("<ButtonRelease-1>", self._clic_resultado)
        self.lista_res.bind("<Return>", lambda e: self._agregar_resultado(self._seleccion()))
        self.lista_res.bind("<Escape>", lambda e: (self._limpiar_busqueda(), self.buscador.focus_set()))
        # lista A–Z (se puede escribir otro texto)
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(6, 2))
        ttk.Button(barra, text="Agregar", command=self.agregar).pack(side="right", padx=(6, 0))
        self.combo = widgets.ComboField(barra, [""] + medicamentos.MEDICAMENTOS, readonly=False, width=40)
        self.combo.pack(side="left", fill="x", expand=True)
        self.combo.bind("<KeyRelease>", self._filtrar)
        self.combo.bind("<Return>", lambda e: self.agregar())
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.agregar())
        ttk.Label(self, text="Lista en orden alfabético (también puede escribir un medicamento que no esté).",
                  style="Muted.TLabel").pack(anchor="w")
        self.lista = ttk.Frame(self)
        self.lista.pack(fill="x", pady=(4, 0))
        for t in iniciales:
            self._nueva_fila(t)

    # -- búsqueda con lupa ---------------------------------------------------------------
    def buscar(self, texto):
        """Medicamentos que contienen todas las palabras escritas (sin importar acentos ni mayúsculas)."""
        palabras = cat.plain(texto).split()
        if not palabras:
            return []
        return [m for m in medicamentos.MEDICAMENTOS if all(w in cat.plain(m) for w in palabras)]

    def _buscar(self, event=None):
        if event is not None and event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        self._resultados = self.buscar(self.buscador.get_value())[:self.MAX_RESULTADOS * 4]
        self.lista_res.delete(0, "end")
        if not self.buscador.get_value().strip():
            self.lista_res.pack_forget()
            return
        if not self._resultados:
            self.lista_res.insert("end", "(ningún medicamento coincide; puede escribirlo abajo)")
            self.lista_res.configure(height=1)
        else:
            for m in self._resultados:
                self.lista_res.insert("end", m)
            self.lista_res.configure(height=min(len(self._resultados), self.MAX_RESULTADOS))
        self.lista_res.pack(fill="x", after=self.buscador.master)

    def _seleccion(self):
        s = self.lista_res.curselection()
        return s[0] if s else 0

    def _ir_a_resultados(self, _event=None):
        if self._resultados:
            self.lista_res.focus_set()
            self.lista_res.selection_clear(0, "end")
            self.lista_res.selection_set(0)
            self.lista_res.activate(0)
        return "break"

    def _clic_resultado(self, event):
        i = self.lista_res.nearest(event.y)
        if 0 <= i < len(self._resultados):
            self._agregar_resultado(i)

    def _agregar_resultado(self, i):
        if not self._resultados or not (0 <= i < len(self._resultados)):
            return
        self._nueva_fila(self._resultados[i])
        self._limpiar_busqueda()
        self.buscador.focus_set()
        self._cambio()

    def _limpiar_busqueda(self):
        self.buscador.set_value("")
        self._resultados = []
        self.lista_res.delete(0, "end")
        self.lista_res.pack_forget()

    # -- lista A–Z -----------------------------------------------------------------------
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
        ent = widgets.EntryField(fila, width=40)
        ent.set_value(texto)
        item = (fila, ent)
        ttk.Button(fila, text="Quitar", width=7, command=lambda: self._quitar(item)).pack(side="right", padx=(6, 0))
        ent.pack(side="left", fill="x", expand=True)
        ent.bind("<KeyRelease>", lambda e: self._cambio())
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
