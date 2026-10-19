"""Pacientes cargados desde los ATA, con el botón «Añadir registro» al lado de cada uno."""
import threading
from tkinter import ttk

from services import activityinfo
from services import ata as ata_svc
from services.validators import fmt_date
from ui import dialogs, widgets
from ui.dialog_activityinfo import ActivityInfoDialog
from ui.page import Page

ACTION = "➕ Añadir registro"


class PacientesPage(Page):
    nav_key = "pacientes"

    def __init__(self, app):
        super().__init__(app)
        self._after = None
        self._rows = {}
        self._busy = False
        self._result = None
        self._checked = set()
        ttk.Label(self, text="Pacientes", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Un renglón por paciente atendido. Pulse «➕ Añadir registro» (junto a cada paciente) para registrarlo en ActivityInfo.", style="Muted.TLabel").pack(
            anchor="w", pady=(0, 6))
        bar = ttk.Frame(self)
        bar.pack(fill="x")
        ttk.Label(bar, text="Buscar:").pack(side="left")
        self.q = widgets.EntryField(bar, width=30)
        self.q.pack(side="left", padx=(6, 12))
        self.q.var.trace_add("write", lambda *a: self._schedule())
        ttk.Label(bar, text="Estado:").pack(side="left")
        self.estado = widgets.ComboField(bar, ["Todos", "Pendiente", "Registrado"], readonly=True, width=14)
        self.estado.set_value("Todos")
        self.estado.pack(side="left", padx=(6, 12))
        self.estado.bind("<<ComboboxSelected>>", lambda e: self.load())
        self.count = ttk.Label(bar, text="", style="Muted.TLabel")
        self.count.pack(side="left", padx=6)
        bar2 = ttk.Frame(self)
        bar2.pack(fill="x", pady=(8, 0))
        ttk.Button(bar2, text="Seleccionar paciente", command=self.toggle_current).pack(side="left")
        ttk.Button(bar2, text="Seleccionar todo", command=self.toggle_all).pack(side="left", padx=8)
        self.btn_del = ttk.Button(bar2, text="Borrar", command=self.delete_checked)
        self.btn_del.pack(side="left")
        ttk.Label(bar2, text="(también puede marcar la casilla ☐ de cada paciente)",
                  style="Muted.TLabel").pack(side="left", padx=10)

        frame, self.tree = widgets.make_tree(self, [
            ("sel", "", 46, "center"), ("fecha", "Fecha", 108), ("nombre", "Paciente", 270), ("accion", "Acción", 160, "center"),
            ("estado", "ActivityInfo", 95, "center"), ("sexo", "Sexo", 50, "center"),
            ("edad", "Edad", 70), ("dx", "Diagnósticos", 340)], height=16)
        frame.pack(fill="both", expand=True, pady=(8, 0))
        self.tree.bind("<Button-1>", self._click)
        self.tree.bind("<Return>", lambda e: self.add_record())
        bot = ttk.Frame(self)
        bot.pack(fill="x", pady=(10, 0))
        ttk.Button(bot, text="Añadir registro al seleccionado", style="Accent.TButton",
                   command=self.add_record).pack(side="left")
        ttk.Button(bot, text="Marcar como registrado", command=lambda: self.mark(True)).pack(
            side="left", padx=8)
        ttk.Button(bot, text="Marcar como pendiente", command=lambda: self.mark(False)).pack(side="left")
        ttk.Button(bot, text="Cargar otro ATA", command=lambda: self.app.show("ata")).pack(side="right")

    def on_show(self, **kw):
        self.load()
        self.q.focus_set()

    def refresh(self):
        self.load()

    def _schedule(self):
        if self._after:
            self.after_cancel(self._after)
        self._after = self.after(250, self.load)

    def load(self):
        self._after = None
        rows = ata_svc.list_records(self.db, self.q.get_value(), self.estado.get_value())
        self._rows = {r["id"]: r for r in rows}
        self._checked &= set(self._rows)
        widgets.fill_tree(self.tree, [(
            r["id"], ("☑" if r["id"] in self._checked else "☐", fmt_date(r["fecha"]), r["nombre"],
                      ACTION if r["ai_estado"] != "Registrado" else "Registrado ✔",
                      r["ai_estado"], r["sexo"], ata_svc.age_text(r),
                      " · ".join(x for x in (r["dx1"], r["dx2"], r["dx3"]) if x))) for r in rows])
        pend = sum(1 for r in rows if r["ai_estado"] != "Registrado")
        self.count.configure(text=f"{len(rows)} paciente(s) · {pend} pendiente(s)")
        self._update_buttons()

    # -- selección y borrado ---------------------------------------------------
    def _update_buttons(self):
        n = len(self._checked)
        self.btn_del.configure(text=f"Borrar ({n})" if n else "Borrar")

    def _set_check(self, rid, on):
        (self._checked.add if on else self._checked.discard)(rid)
        if self.tree.exists(str(rid)):
            self.tree.set(str(rid), "sel", "☑" if on else "☐")
        self._update_buttons()

    def toggle_current(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Pulse primero un paciente de la lista.")
            return
        self._set_check(int(iid), int(iid) not in self._checked)

    def toggle_all(self):
        ids = [int(i) for i in self.tree.get_children("")]
        on = not (ids and all(i in self._checked for i in ids))
        for i in ids:
            self._set_check(i, on)

    def delete_checked(self):
        ids = sorted(self._checked)
        if not ids:
            dialogs.info(self, "No hay pacientes marcados. Use «Seleccionar paciente» o «Seleccionar todo».")
            return
        nombres = [self._rows[i]["nombre"] for i in ids if i in self._rows]
        resumen = "\n".join(f"• {n}" for n in nombres[:8]) + (f"\n… y {len(nombres) - 8} más" if len(nombres) > 8 else "")
        if not dialogs.confirm(self, "Borrar pacientes", f"¿Quitar {len(ids)} paciente(s) del programa?\n\n{resumen}\n\n"
                               "Se quitan de esta lista y de su hoja ATA. Esto no toca ActivityInfo.",
                               yes="Borrar", no="Cancelar"):
            return
        ata_svc.delete_records(self.db, ids)
        self._checked.clear()
        self.app.refresh_all()

    def _click(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        col = self.tree.identify_column(event.x)
        iid = self.tree.identify_row(event.y)
        if iid and col == "#1":
            self._set_check(int(iid), int(iid) not in self._checked)
            return "break"
        if iid and col == f"#{list(self.tree['columns']).index('accion') + 1}":
            self.tree.selection_set(iid)
            self.after(10, self.add_record)

    def _selected(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Seleccione primero un paciente de la lista.")
            return None
        return int(iid)

    def add_record(self):
        rid = self._selected()
        if rid is None:
            return
        rec = ata_svc.get_record(self.db, rid)
        if rec["ai_estado"] == "Registrado" and not dialogs.confirm(
                self, "Ya registrado", f"{rec['nombre']} ya está marcado como registrado en "
                "ActivityInfo. ¿Llenar el formulario otra vez?", yes="Llenar de nuevo", no="Cancelar"):
            return
        data = ActivityInfoDialog(self, activityinfo.build_defaults(self.db, rec), db=self.db).run()
        if not data:
            return
        activityinfo.remember_dx(self.db, data)
        self._busy = True
        self.count.configure(text="Abriendo Chrome… si pide iniciar sesión, hágalo en esa ventana.")
        threading.Thread(target=self._worker, args=(rid, rec["nombre"], data), daemon=True).start()
        self.after(400, self._poll)

    def _worker(self, rid, nombre, data):
        try:
            self._result = (rid, nombre, data, activityinfo.fill_form(data), None)
        except Exception as exc:  # noqa: BLE001
            self._result = (rid, nombre, data, None, exc)

    def _poll(self):
        if self._result is None:
            self.after(400, self._poll)
            return
        rid, nombre, data, report, exc = self._result
        self._result = None
        self.load()
        if exc is not None:
            dialogs.error(self, f"No se pudo llenar el formulario:\n{exc}")
            return
        falta = (report.get("ficha") or []) + (report.get("aps") or [])
        msg = f"Se llenó el formulario de {nombre} en Chrome. REVÍSELO y cree la ficha usted en ActivityInfo " \
              "(el programa no guarda nada)."
        info = report.get("info") or []
        if info:
            msg += "\n\nDiagnósticos elegidos en ActivityInfo (verifíquelos):\n" + "\n".join(f"• {i}" for i in info)
        if falta:
            msg += "\n\nNo se pudieron llenar (hágalo a mano):\n" + "\n".join(f"• {f}" for f in falta)
        dialogs.info(self, msg, title="Formulario llenado")
        if dialogs.confirm(self, "¿Se registró?", f"Cuando haya creado la ficha de {nombre} en ActivityInfo, "
                           "¿la marco como registrada?", yes="Sí, marcar", no="Todavía no"):
            ata_svc.set_registered(self.db, rid, True)
            self.load()

    def mark(self, registered):
        rid = self._selected()
        if rid is not None:
            ata_svc.set_registered(self.db, rid, registered)
            self.load()
