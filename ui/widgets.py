"""Componentes reutilizables de la interfaz Tkinter.

Todos los campos de formulario exponen la misma interfaz:
    get_value() -> texto / bool        set_value(valor)
para que las páginas puedan recoger y rellenar formularios de forma uniforme.
"""
import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from ui import theme

# ---------------------------------------------------------------------------
# Utilidades generales
# ---------------------------------------------------------------------------


def open_path(path):
    """Abre un archivo o carpeta con la aplicación predeterminada del sistema."""
    path = str(path)
    if sys.platform.startswith("win"):
        os.startfile(path)  # noqa: S606  (solo Windows)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def _wheel_units(event):
    if getattr(event, "num", None) == 4:
        return -1
    if getattr(event, "num", None) == 5:
        return 1
    delta = getattr(event, "delta", 0)
    if delta == 0:
        return 0
    return -1 if delta > 0 else 1


def install_global_bindings(root):
    """Rueda del ratón sobre el formulario (sin cambiar listas desplegables por accidente)
    y Tab para saltar de campo dentro de los cuadros de texto."""
    # Evita que girar la rueda sobre una lista desplegable cambie el valor clínico.
    for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
        try:
            root.unbind_class("TCombobox", seq)
        except tk.TclError:
            pass

    def on_wheel(event):
        units = _wheel_units(event)
        if not units:
            return
        try:
            w = root.winfo_containing(event.x_root, event.y_root)
        except (KeyError, tk.TclError):
            return
        first = True
        while w is not None:
            if isinstance(w, (ttk.Treeview, tk.Listbox)):
                return  # se desplazan solos
            if isinstance(w, tk.Text):
                try:
                    lo, hi = w.yview()
                except tk.TclError:
                    return
                if first and (lo > 0.0 or hi < 1.0):
                    return  # el texto tiene más contenido: se desplaza él mismo
            if isinstance(w, ScrollFrame):
                w.canvas.yview_scroll(units * 3, "units")
                return "break"
            first = False
            w = getattr(w, "master", None)

    root.bind_all("<MouseWheel>", on_wheel)
    root.bind_all("<Button-4>", on_wheel)
    root.bind_all("<Button-5>", on_wheel)


class ScrollFrame(ttk.Frame):
    """Contenedor con barra de desplazamiento vertical. Colocar el contenido en `.body`."""

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=theme.BG)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.body = ttk.Frame(self.canvas)
        self._win = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", self._on_body)
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfigure(self._win, width=e.width))

    def _on_body(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def scroll_top(self):
        self.canvas.yview_moveto(0)


# ---------------------------------------------------------------------------
# Campos
# ---------------------------------------------------------------------------

def _tab_next(event):
    event.widget.tk_focusNext().focus()
    return "break"


def _tab_prev(event):
    event.widget.tk_focusPrev().focus()
    return "break"


class TextBox(ttk.Frame):
    """Cuadro de texto multilínea que crece con el contenido. Tab pasa al siguiente campo."""

    def __init__(self, master, height=3, max_height=14, **kw):
        super().__init__(master, **kw)
        self.min_h, self.max_h, self._h = height, max_height, height
        self.text = tk.Text(self, height=height, wrap="word", font=theme.FONT_TEXT, undo=True,
                            relief="solid", bd=1, padx=6, pady=4, highlightthickness=1,
                            highlightcolor=theme.PRIMARY, highlightbackground=theme.BORDER,
                            bg="white", fg=theme.TEXT, insertbackground=theme.TEXT)
        self.text.pack(fill="both", expand=True)
        self.text.bind("<Tab>", _tab_next)
        self.text.bind("<Shift-Tab>", _tab_prev)
        self.text.bind("<ISO_Left_Tab>", _tab_prev)
        self.text.bind("<KeyRelease>", lambda e: self._autosize())
        self.text.bind("<Configure>", lambda e: self.after_idle(self._autosize))

    def _autosize(self):
        try:
            n = self.text.count("1.0", "end-1c", "displaylines")
            n = n[0] if isinstance(n, tuple) else (n or 1)
        except (tk.TclError, TypeError):
            n = int(self.text.index("end-1c").split(".")[0])
        n = max(self.min_h, min(int(n or 1), self.max_h))
        if n != self._h:
            self._h = n
            self.text.configure(height=n)

    def get_value(self):
        return self.text.get("1.0", "end-1c")

    def set_value(self, value):
        state = str(self.text.cget("state"))
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        if value:
            self.text.insert("1.0", str(value))
        self.text.edit_reset()
        self.text.configure(state=state)
        self.after_idle(self._autosize)

    def append_value(self, value):
        current = self.get_value().rstrip()
        self.set_value((current + "\n" if current else "") + value)

    def focus_field(self):
        self.text.focus_set()


class EntryField(ttk.Entry):
    def __init__(self, master, width=24, **kw):
        self.var = tk.StringVar()
        super().__init__(master, textvariable=self.var, width=width, **kw)

    def get_value(self):
        return self.var.get()

    def set_value(self, value):
        self.var.set("" if value is None else str(value))

    def focus_field(self):
        self.focus_set()


class ComboField(ttk.Combobox):
    """Lista desplegable. readonly=False permite escribir un valor nuevo."""

    def __init__(self, master, values=(), readonly=True, width=24, **kw):
        self.var = tk.StringVar()
        super().__init__(master, textvariable=self.var, values=list(values), width=width,
                         state="readonly" if readonly else "normal", **kw)

    def get_value(self):
        return self.var.get()

    def set_value(self, value):
        self.var.set("" if value is None else str(value))

    def set_values(self, values):
        self.configure(values=list(values))

    def focus_field(self):
        self.focus_set()


class CheckField(ttk.Checkbutton):
    def __init__(self, master, text="", **kw):
        self.var = tk.BooleanVar(value=False)
        super().__init__(master, text=text, variable=self.var, **kw)

    def get_value(self):
        return bool(self.var.get())

    def set_value(self, value):
        self.var.set(bool(value) and value not in ("0", "No"))


class DateEntry(ttk.Frame):
    """Fecha DD/MM/AAAA con formato automático (escriba solo los números)."""

    def __init__(self, master, show_today=False, width=12, on_change=None, **kw):
        super().__init__(master, **kw)
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, width=width)
        self.entry.pack(side="left")
        self.on_change = on_change
        if show_today:
            b = ttk.Button(self, text="Hoy", style="Small.TButton", command=self.set_today,
                           takefocus=0)
            b.pack(side="left", padx=(6, 0))
        ttk.Label(self, text="dd/mm/aaaa", style="Hint.TLabel").pack(side="left", padx=(8, 0))
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<FocusOut>", lambda e: self._notify())

    def _notify(self):
        if self.on_change:
            self.on_change()

    def _on_key(self, event):
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Home", "End", "Tab",
                            "ISO_Left_Tab", "Shift_L", "Shift_R", "Control_L", "Control_R"):
            self._notify()
            return
        text = self.var.get()
        if event.char == "/":
            parts = text.rstrip("/").split("/")[:3]
            fixed = [p.zfill(2) if i < 2 else p for i, p in enumerate(parts)]
            new = "/".join(fixed) + ("/" if len(fixed) < 3 else "")
        else:
            d = re.sub(r"\D", "", text)[:8]
            new = d[:2] + ("/" + d[2:4] if len(d) > 2 else "") + ("/" + d[4:] if len(d) > 4 else "")
        if new != text:
            self.var.set(new)
            self.entry.icursor("end")
        self._notify()

    def set_today(self):
        from datetime import date
        self.var.set(date.today().strftime("%d/%m/%Y"))
        self._notify()

    def get_value(self):
        return self.var.get().strip()

    def set_value(self, value):
        value = "" if value is None else str(value)
        if re.match(r"^\d{4}-\d{2}-\d{2}", value):
            value = f"{value[8:10]}/{value[5:7]}/{value[0:4]}"
        self.var.set(value)

    def focus_field(self):
        self.entry.focus_set()


# ---------------------------------------------------------------------------
# Distribución de formularios
# ---------------------------------------------------------------------------

class FormGrid:
    """Coloca campos con su etiqueta encima, en una cuadrícula de N columnas."""

    def __init__(self, parent, columns=3):
        self.parent, self.columns, self.r, self.c = parent, columns, 0, 0
        for i in range(columns):
            parent.columnconfigure(i, weight=1, uniform="fg")

    def add(self, label, widget, span=1, required=False, sticky="ew", hint=None):
        if self.c + span > self.columns:
            self.newline()
        text = label + (" *" if required else "")
        ttk.Label(self.parent, text=text, style="Field.TLabel").grid(
            row=self.r * 3, column=self.c, columnspan=span, sticky="w", padx=(0, 12), pady=(10, 0))
        widget.grid(row=self.r * 3 + 1, column=self.c, columnspan=span, sticky=sticky,
                    padx=(0, 12), pady=(2, 0))
        if hint:
            ttk.Label(self.parent, text=hint, style="Hint.TLabel").grid(
                row=self.r * 3 + 2, column=self.c, columnspan=span, sticky="w")
        self.c += span
        if self.c >= self.columns:
            self.newline()
        return widget

    def newline(self):
        if self.c:
            self.r += 1
            self.c = 0

    def full(self, widget, pady=(8, 0)):
        """Widget que ocupa todo el ancho (avisos, botones, subtítulos)."""
        self.newline()
        widget.grid(row=self.r * 3, column=0, columnspan=self.columns, sticky="ew", pady=pady)
        self.r += 1


def section(parent, title, pady=(0, 12)):
    """Recuadro con título; devuelve el marco interior."""
    box = ttk.LabelFrame(parent, text=f" {title} ", padding=(14, 6, 14, 14))
    box.pack(fill="x", pady=pady)
    return box


def button_row(parent, items, pady=(8, 0)):
    """items: [(texto, comando, estilo)] en una fila horizontal."""
    row = ttk.Frame(parent)
    for text, cmd, *style in items:
        b = ttk.Button(row, text=text, command=cmd, style=style[0] if style else "TButton")
        b.pack(side="left", padx=(0, 8))
    return row


# ---------------------------------------------------------------------------
# Filas dinámicas (medicamentos, diagnósticos, pruebas…)
# ---------------------------------------------------------------------------

class RowList(ttk.Frame):
    """Lista de filas que se pueden agregar y quitar.

    row_factory(parent, remove_cb) debe devolver un objeto con:
        .frame  .get() -> dict   .set(dict)   .focus()
    """

    def __init__(self, master, row_factory, add_text="+ Agregar fila"):
        super().__init__(master)
        self.factory = row_factory
        self.container = ttk.Frame(self)
        self.container.pack(fill="x")
        self.add_btn = ttk.Button(self, text=add_text, command=lambda: self.add_row(focus=True))
        self.add_btn.pack(anchor="w", pady=(8, 0))
        self.rows = []

    def add_row(self, data=None, focus=False):
        holder = {}
        row = self.factory(self.container, lambda: self.remove_row(holder["row"]))
        holder["row"] = row
        row.frame.pack(fill="x", pady=(0, 8))
        if data:
            row.set(data)
        self.rows.append(row)
        if focus:
            row.focus()
        return row

    def remove_row(self, row):
        if row in self.rows:
            self.rows.remove(row)
            row.frame.destroy()

    def clear(self):
        for r in list(self.rows):
            self.remove_row(r)

    def get_all(self):
        return [r.get() for r in self.rows]

    def set_all(self, items, min_rows=0):
        self.clear()
        for it in items or []:
            self.add_row(it)
        for _ in range(max(0, min_rows - len(self.rows))):
            self.add_row()


# ---------------------------------------------------------------------------
# Tablas (Treeview)
# ---------------------------------------------------------------------------

def _sort_key(text):
    s = str(text).strip()
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", s)
    if m:
        return (0, f"{m.group(3)}{m.group(2)}{m.group(1)}")
    try:
        return (0, f"{float(s):020.4f}")
    except ValueError:
        return (1, s.lower())


def sort_tree(tree, col, reverse):
    items = [(tree.set(k, col), k) for k in tree.get_children("")]
    items.sort(key=lambda t: _sort_key(t[0]), reverse=reverse)
    for i, (_, k) in enumerate(items):
        tree.move(k, "", i)
    _stripe(tree)
    tree.heading(col, command=lambda: sort_tree(tree, col, not reverse))


def _stripe(tree):
    for i, k in enumerate(tree.get_children("")):
        tags = [t for t in tree.item(k, "tags") if t not in ("odd", "even")]
        tree.item(k, tags=tags + ["odd" if i % 2 else "even"])


def make_tree(parent, columns, height=10, selectmode="browse"):
    """columns: [(id, encabezado, ancho, [anchor])]. Devuelve (marco, tree)."""
    frame = ttk.Frame(parent)
    tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings", height=height,
                        selectmode=selectmode)
    for cid, title, width, *rest in columns:
        tree.heading(cid, text=title, command=lambda c=cid: sort_tree(tree, c, False))
        width = max(width, int(len(title) * 9.5) + 26)  # que el encabezado nunca se corte
        tree.column(cid, width=width, minwidth=width // 2, anchor=rest[0] if rest else "w")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    tree.tag_configure("odd", background="#F4F8F9")
    tree.tag_configure("even", background="white")
    tree.tag_configure("draft", foreground=theme.WARN)
    return frame, tree


def fill_tree(tree, items):
    """items: [(iid, valores, [tags])]"""
    tree.delete(*tree.get_children(""))
    for i, item in enumerate(items):
        iid, values = str(item[0]), item[1]
        tags = list(item[2]) if len(item) > 2 else []
        tree.insert("", "end", iid=iid, values=values, tags=tags + ["odd" if i % 2 else "even"])


def selected_iid(tree):
    sel = tree.selection()
    return sel[0] if sel else None


# ---------------------------------------------------------------------------
# Bloqueo / desbloqueo de formularios (fichas finalizadas en modo lectura)
# ---------------------------------------------------------------------------

def set_locked(widget, locked):
    for child in widget.winfo_children():
        if isinstance(child, tk.Text):
            child.configure(state="disabled" if locked else "normal",
                            bg="#EDF0F1" if locked else "white")
        elif isinstance(child, (ttk.Entry, ttk.Combobox, ttk.Checkbutton, ttk.Radiobutton,
                                ttk.Button)):
            if not getattr(child, "_keep_enabled", False):
                child.state(["disabled" if locked else "!disabled"])
        set_locked(child, locked)


def keep_enabled(widget):
    widget._keep_enabled = True
    return widget
