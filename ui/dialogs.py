"""Diálogos propios en español (botones claros, siempre centrados sobre la ventana).

Las páginas usan estas funciones (y no tkinter.messagebox directamente) para que el
comportamiento sea uniforme y se pueda probar sin ventanas emergentes.
"""
import tkinter as tk
from tkinter import filedialog, ttk

from services.validators import fmt_date
from ui import theme, widgets


def _center(win, parent):
    win.update_idletasks()
    try:
        top = parent.winfo_toplevel()
        px, py = top.winfo_rootx(), top.winfo_rooty()
        pw, ph = top.winfo_width(), top.winfo_height()
    except tk.TclError:
        px = py = 0
        pw, ph = win.winfo_screenwidth(), win.winfo_screenheight()
    w, h = win.winfo_reqwidth(), win.winfo_reqheight()
    x = max(0, px + (pw - w) // 2)
    y = max(0, py + (ph - h) // 3)
    win.geometry(f"+{x}+{y}")


class _Modal(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent.winfo_toplevel())
        self.withdraw()
        self.title(title)
        self.configure(bg=theme.BG)
        self.transient(parent.winfo_toplevel())
        self.resizable(False, False)
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Escape>", lambda e: self.cancel())

    def cancel(self):
        self.result = None
        self.destroy()

    def run(self):
        _center(self, self.master)
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.wait_window(self)
        return self.result


def choose(parent, title, message, buttons, default=None, cancel=None, details=None):
    """Muestra un mensaje con botones. buttons: [(clave, texto, estilo)].
    Devuelve la clave pulsada (o `cancel` si se cierra la ventana)."""
    dlg = _Modal(parent, title)
    body = ttk.Frame(dlg, padding=(22, 18, 22, 8))
    body.pack(fill="both", expand=True)
    ttk.Label(body, text=message, wraplength=520, justify="left", font=theme.FONT).pack(anchor="w")
    if details:
        txt = tk.Text(body, width=70, height=min(12, max(3, len(details) + 1)), wrap="word",
                      font=theme.FONT, relief="solid", bd=1, padx=8, pady=6, bg=theme.FIELD, fg=theme.TEXT)
        txt.insert("1.0", "\n".join(f"•  {d}" for d in details))
        txt.configure(state="disabled")
        txt.pack(fill="x", pady=(10, 0))
    bar = ttk.Frame(dlg, padding=(22, 10, 22, 18))
    bar.pack(fill="x")
    dlg.result = cancel

    def pick(key):
        dlg.result = key
        dlg.destroy()

    first = None
    for key, text, style in reversed(buttons):
        st = {"accent": "Accent.TButton", "danger": "Danger.TButton"}.get(style, "TButton")
        b = ttk.Button(bar, text=text, style=st, command=lambda k=key: pick(k))
        b.pack(side="right", padx=(8, 0))
        if key == default:
            first = b
    if first is not None:
        first.focus_set()
        dlg.bind("<Return>", lambda e: pick(default))

    def _cancel():
        dlg.result = cancel
        dlg.destroy()

    dlg.cancel = _cancel
    dlg.protocol("WM_DELETE_WINDOW", _cancel)
    dlg.bind("<Escape>", lambda e: _cancel())
    return dlg.run()


def info(parent, message, title="Información"):
    choose(parent, title, message, [("ok", "Entendido", "accent")], default="ok", cancel="ok")


def error(parent, message, title="Error", details=None):
    choose(parent, title, message, [("ok", "Entendido", "accent")], default="ok", cancel="ok",
           details=details)


def show_errors(parent, errors, title="Revise los datos"):
    """Los datos escritos se conservan; solo se informa qué corregir."""
    choose(parent, title, "No se pudo guardar. Corrija lo siguiente (sus datos no se han perdido):",
           [("ok", "Volver al formulario", "accent")], default="ok", cancel="ok",
           details=list(errors))


def confirm(parent, title, message, yes="Sí", no="No", danger=False, details=None):
    return choose(parent, title, message,
                  [("no", no, "normal"), ("yes", yes, "danger" if danger else "accent")],
                  default="no" if danger else "yes", cancel="no", details=details) == "yes"


def confirm_warnings(parent, warnings, proceed="Guardar de todos modos", title="Advertencias"):
    return choose(parent, title,
                  "Revise estas advertencias. Puede continuar si los datos son correctos:",
                  [("back", "Revisar", "normal"), ("go", proceed, "accent")],
                  default="back", cancel="back", details=list(warnings)) == "go"


def unsaved_changes(parent, save_text="Guardar"):
    """-> 'save' | 'discard' | 'cancel'"""
    return choose(parent, "Cambios sin guardar",
                  "Hay cambios sin guardar en esta ficha. ¿Qué desea hacer?",
                  [("cancel", "Seguir editando", "normal"), ("discard", "Descartar cambios", "danger"),
                   ("save", save_text, "accent")], default="save", cancel="cancel")


# -- archivos ------------------------------------------------------------------

def ask_save_path(parent, title, initialfile="", ext=".pdf", types=None):
    return filedialog.asksaveasfilename(
        parent=parent.winfo_toplevel(), title=title, initialfile=initialfile,
        defaultextension=ext, filetypes=types or [("PDF", "*.pdf"), ("Todos", "*.*")]) or None


def ask_open_path(parent, title, types=None):
    return filedialog.askopenfilename(
        parent=parent.winfo_toplevel(), title=title,
        filetypes=types or [("Copias de seguridad", "*.db"), ("Todos", "*.*")]) or None


def ask_directory(parent, title):
    return filedialog.askdirectory(parent=parent.winfo_toplevel(), title=title) or None


# -- contraseña ------------------------------------------------------------------

def ask_password(parent, title, prompt, confirm_twice=False):
    """Devuelve el texto escrito o None si se cancela."""
    dlg = _Modal(parent, title)
    body = ttk.Frame(dlg, padding=(22, 18, 22, 6))
    body.pack(fill="both", expand=True)
    ttk.Label(body, text=prompt, wraplength=360, justify="left").pack(anchor="w")
    e1 = ttk.Entry(body, show="•", width=34)
    e1.pack(fill="x", pady=(10, 0))
    e2 = None
    if confirm_twice:
        ttk.Label(body, text="Repita la contraseña", style="Field.TLabel").pack(anchor="w", pady=(10, 0))
        e2 = ttk.Entry(body, show="•", width=34)
        e2.pack(fill="x", pady=(2, 0))
    msg = ttk.Label(body, text="", style="Error.TLabel")
    msg.pack(anchor="w", pady=(6, 0))

    def ok(_e=None):
        if confirm_twice and e1.get() != e2.get():
            msg.configure(text="Las contraseñas no coinciden.")
            return
        if confirm_twice and len(e1.get()) < 4:
            msg.configure(text="Use al menos 4 caracteres.")
            return
        dlg.result = e1.get()
        dlg.destroy()

    bar = ttk.Frame(dlg, padding=(22, 6, 22, 18))
    bar.pack(fill="x")
    ttk.Button(bar, text="Aceptar", style="Accent.TButton", command=ok).pack(side="right")
    ttk.Button(bar, text="Cancelar", command=dlg.cancel).pack(side="right", padx=8)
    dlg.bind("<Return>", ok)
    e1.focus_set()
    return dlg.run()


# -- sugerencias clínicas (solo para revisión del personal médico) ----------------------

def suggestions(parent, title, intro, items, action_text, preselect=False):
    """Lista de sugerencias con casillas. Devuelve las marcadas, o None si se cancela."""
    dlg = _Modal(parent, title)
    body = ttk.Frame(dlg, padding=(22, 18, 22, 6))
    body.pack(fill="both", expand=True)
    ttk.Label(body, text=intro, wraplength=560, justify="left").pack(anchor="w", pady=(0, 8))
    vars_ = []
    for it in items:
        v = tk.BooleanVar(value=preselect)
        vars_.append(v)
        ttk.Checkbutton(body, text=it, variable=v, command=None).pack(anchor="w", pady=2)
        # etiquetas largas: ajustar al ancho
    for child in body.winfo_children():
        if isinstance(child, ttk.Checkbutton):
            child.configure(style="TCheckbutton")
    bar = ttk.Frame(dlg, padding=(22, 10, 22, 18))
    bar.pack(fill="x")

    def go():
        dlg.result = [it for it, v in zip(items, vars_) if v.get()]
        dlg.destroy()

    ttk.Button(bar, text=action_text, style="Accent.TButton", command=go).pack(side="right")
    ttk.Button(bar, text="Cerrar", command=dlg.cancel).pack(side="right", padx=8)
    return dlg.run()


def read_only_list(parent, title, intro, items):
    dlg = _Modal(parent, title)
    body = ttk.Frame(dlg, padding=(22, 18, 22, 6))
    body.pack(fill="both", expand=True)
    ttk.Label(body, text=intro, wraplength=560, justify="left").pack(anchor="w", pady=(0, 8))
    for it in items:
        ttk.Label(body, text=f"•  {it}", wraplength=560, justify="left").pack(anchor="w", pady=2)
    bar = ttk.Frame(dlg, padding=(22, 10, 22, 18))
    bar.pack(fill="x")
    ttk.Button(bar, text="Cerrar", style="Accent.TButton", command=dlg.cancel).pack(side="right")
    dlg.run()


# -- historial de modificaciones ---------------------------------------------------------

def audit_log(parent, title, rows):
    dlg = tk.Toplevel(parent.winfo_toplevel())
    dlg.withdraw()
    dlg.title(title)
    dlg.configure(bg=theme.BG)
    dlg.transient(parent.winfo_toplevel())
    dlg.geometry("900x420")
    ttk.Label(dlg, text=title, style="H2.TLabel").pack(anchor="w", padx=18, pady=(14, 6))
    frame, tree = widgets.make_tree(dlg, [("ts", "Fecha y hora", 140), ("usuario", "Usuario", 110),
                                          ("accion", "Acción", 150), ("detalle", "Detalle", 480)],
                                    height=12)
    frame.pack(fill="both", expand=True, padx=18)
    widgets.fill_tree(tree, [(r["id"], (_ts(r["ts"]), r.get("usuario") or "", r["accion"],
                                        (r.get("detalle") or "")[:400])) for r in rows])
    ttk.Button(dlg, text="Cerrar", style="Accent.TButton", command=dlg.destroy).pack(
        anchor="e", padx=18, pady=12)
    if not rows:
        ttk.Label(dlg, text="Todavía no hay modificaciones registradas.",
                  style="Muted.TLabel").pack(before=frame)
    _center(dlg, parent)
    dlg.deiconify()
    dlg.grab_set()
    dlg.wait_window(dlg)


def _ts(ts):
    return f"{fmt_date(ts)} {str(ts)[11:16]}" if ts else ""
