"""Buscador con lupa para las listas desplegables largas (diagnósticos de ActivityInfo): al escribir en el cuadro aparece,
justo debajo, la lista de las opciones que coinciden; se elige con un clic o con Enter. La lista desplegable de siempre
sigue funcionando (en orden alfabético) y también se puede dejar escrito un texto propio."""
import tkinter as tk
from tkinter import ttk

from services.cie11_catalog import plain
from ui import theme


class Lupa(tk.Canvas):
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


def buscar(texto, etiquetas, limite=60):
    """Opciones que contienen todas las palabras escritas (sin acentos ni mayúsculas; también vale el código).
    Primero las que empiezan con lo escrito y después las demás, cada grupo en el orden de la lista (A–Z)."""
    palabras = plain(texto).split()
    if not palabras:
        return []
    q = " ".join(palabras)
    empiezan, contienen = [], []
    for e in etiquetas:
        p = plain(e)
        if all(w in p for w in palabras):
            (empiezan if p.startswith(q) else contienen).append(e)
    return (empiezan + contienen)[:limite]


class BuscadorLista:
    """Agrega una lupa a la izquierda de `cb` (dentro de `fila`) y una lista de resultados debajo de `fila`.
    `al_elegir()` se llama después de poner la opción elegida en `cb`."""
    FILAS = 7

    def __init__(self, cb, fila, etiquetas, al_elegir=None):
        self.cb, self.fila, self.etiquetas, self.al_elegir = cb, fila, etiquetas, al_elegir
        self.resultados = []
        self._ocultar_job = None
        self.lupa = Lupa(fila)
        self.lupa.pack(side="left", padx=(0, 4), before=cb)
        self.lista = tk.Listbox(fila.master, height=1, activestyle="dotbox", exportselection=False, font=theme.FONT_TEXT)
        cb.bind("<KeyRelease>", self._al_escribir, add="+")
        cb.bind("<Return>", lambda e: self._elegir(self._seleccion()) if self.resultados else None, add="+")
        cb.bind("<Down>", self._ir_a_lista, add="+")
        cb.bind("<Escape>", lambda e: self.ocultar(), add="+")
        cb.bind("<<ComboboxSelected>>", lambda e: self.ocultar(), add="+")
        cb.bind("<FocusOut>", lambda e: self._ocultar_tarde(), add="+")
        self.lista.bind("<ButtonRelease-1>", self._clic)
        self.lista.bind("<Return>", lambda e: self._elegir(self._seleccion()))
        self.lista.bind("<Escape>", lambda e: (self.ocultar(), self.cb.focus_set()))
        self.lista.bind("<FocusIn>", lambda e: self._cancelar_ocultar())

    # -- mostrar / ocultar -----------------------------------------------------------------
    def mostrar(self, texto):
        self._cancelar_ocultar()
        self.resultados = buscar(texto, self.etiquetas)
        if not (texto or "").strip():
            self.ocultar()
            return
        self.lista.delete(0, "end")
        if not self.resultados:
            self.lista.insert("end", "(ninguna opción coincide)")
            self.lista.configure(height=1)
        else:
            for e in self.resultados:
                self.lista.insert("end", e)
            self.lista.configure(height=min(len(self.resultados), self.FILAS))
        self.lista.pack(fill="x", padx=(26, 0), after=self.fila)

    def ocultar(self):
        self._cancelar_ocultar()
        self.resultados = []
        self.lista.pack_forget()

    def _ocultar_tarde(self):
        self._cancelar_ocultar()
        self._ocultar_job = self.cb.after(250, lambda: None if self._foco_en_lista() else self.ocultar())

    def _foco_en_lista(self):
        """¿La lista de resultados tiene el foco? No se usa focus_get(): con la lista desplegable del combo abierta, tkinter
        no sabe convertir esa ventana («popdown») y lanza KeyError."""
        try:
            return str(self.lista.tk.call("focus")) == str(self.lista)
        except tk.TclError:
            return False

    def _cancelar_ocultar(self):
        if self._ocultar_job:
            try:
                self.cb.after_cancel(self._ocultar_job)
            except (tk.TclError, ValueError):
                pass
            self._ocultar_job = None

    # -- eventos -----------------------------------------------------------------------------
    def _al_escribir(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Left", "Right", "Shift_L", "Shift_R", "Control_L"):
            return
        texto = self.cb.get()
        if texto.strip() in self.etiquetas:        # ya es una opción completa: no hay nada que buscar
            self.ocultar()
            return
        self.mostrar(texto)

    def _seleccion(self):
        s = self.lista.curselection()
        return s[0] if s else 0

    def _ir_a_lista(self, _event=None):
        if self.resultados:
            self._cancelar_ocultar()
            self.lista.focus_set()
            self.lista.selection_clear(0, "end")
            self.lista.selection_set(0)
            self.lista.activate(0)
            return "break"
        return None

    def _clic(self, event):
        i = self.lista.nearest(event.y)
        if 0 <= i < len(self.resultados):
            self._elegir(i)

    def _elegir(self, i):
        if not (0 <= i < len(self.resultados)):
            return
        self.cb.set_value(self.resultados[i])
        self.ocultar()
        self.cb.focus_set()
        self.cb.icursor("end")
        if self.al_elegir:
            self.al_elegir()
