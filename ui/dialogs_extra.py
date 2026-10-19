"""Papelera de pacientes y bitácora del llenado."""
import tkinter as tk
from tkinter import ttk

from services import ata as ata_svc
from services import fill_log
from services.validators import fmt_date
from ui import dialogs, widgets


def papelera(parent, db):
    """Lista los pacientes borrados y deja recuperar los marcados. Devuelve cuántos se recuperaron."""
    rows = ata_svc.list_papelera(db)
    dlg = dialogs._Modal(parent, "Papelera")
    dlg.resizable(True, True)
    body = ttk.Frame(dlg, padding=(18, 16, 18, 6))
    body.pack(fill="both", expand=True)
    ttk.Label(body, text="Pacientes borrados. Seleccione (puede usar Ctrl o Mayús) los que quiera recuperar.",
              wraplength=640, justify="left").pack(anchor="w", pady=(0, 8))
    frame, tree = widgets.make_tree(body, [("fecha", "Fecha", 100), ("nombre", "Paciente", 260),
                                           ("dx", "Diagnósticos", 300), ("borrado", "Borrado", 140)],
                                    height=12, selectmode="extended")
    frame.pack(fill="both", expand=True)
    widgets.fill_tree(tree, [(r["id"], (fmt_date(r["fecha"]), r["nombre"],
                                        " · ".join(x for x in (r["dx1"], r["dx2"], r["dx3"]) if x), r["borrado_en"]))
                             for r in rows])
    if not rows:
        ttk.Label(body, text="La papelera está vacía.", style="Muted.TLabel").pack(anchor="w", pady=8)
    n = {"v": 0}

    def recuperar():
        ids = [int(i) for i in tree.selection()]
        if not ids:
            dialogs.info(dlg, "Seleccione primero a quién recuperar.")
            return
        n["v"] = ata_svc.restore_records(db, ids)
        dlg.destroy()

    bar = ttk.Frame(dlg, padding=(18, 8, 18, 16))
    bar.pack(fill="x")
    ttk.Button(bar, text="Cerrar", command=dlg.cancel).pack(side="right")
    if rows:
        ttk.Button(bar, text="Recuperar seleccionados", style="Accent.TButton", command=recuperar).pack(side="right", padx=8)
    dlg.run()
    return n["v"]


def bitacora(parent):
    dlg = dialogs._Modal(parent, "Bitácora del llenado")
    dlg.resizable(True, True)
    body = ttk.Frame(dlg, padding=(18, 16, 18, 6))
    body.pack(fill="both", expand=True)
    ttk.Label(body, text="Cada vez que se llena ActivityInfo queda aquí el resultado (lo más reciente arriba). "
              "Si algo falla, esta información ayuda a encontrar el motivo.", wraplength=640, justify="left").pack(
        anchor="w", pady=(0, 8))
    txt = tk.Text(body, width=92, height=22, wrap="word")
    sb = ttk.Scrollbar(body, command=txt.yview)
    txt.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    txt.pack(side="left", fill="both", expand=True)
    entradas = fill_log.leer()
    txt.insert("1.0", "\n\n".join(fill_log.texto(e) for e in entradas) if entradas else "Todavía no hay llenados registrados.")
    txt.configure(state="disabled")
    bar = ttk.Frame(dlg, padding=(18, 8, 18, 16))
    bar.pack(fill="x")
    ttk.Button(bar, text="Cerrar", style="Accent.TButton", command=dlg.cancel).pack(side="right")
    ttk.Button(bar, text="Abrir el archivo", command=lambda: widgets.open_path(str(fill_log.log_path()))).pack(side="right", padx=8)
    dlg.run()
