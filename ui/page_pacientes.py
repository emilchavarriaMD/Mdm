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

        frame, self.tree = widgets.make_tree(self, [
            ("fecha", "Fecha", 108), ("nombre", "Paciente", 270), ("accion", "Acción", 160, "center"),
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
        widgets.fill_tree(self.tree, [(
            r["id"], (fmt_date(r["fecha"]), r["nombre"],
                      ACTION if r["ai_estado"] != "Registrado" else "Registrado ✔",
                      r["ai_estado"], r["sexo"], ata_svc.age_text(r),
                      " · ".join(x for x in (r["dx1"], r["dx2"], r["dx3"]) if x))) for r in rows])
        pend = sum(1 for r in rows if r["ai_estado"] != "Registrado")
        self.count.configure(text=f"{len(rows)} paciente(s) · {pend} pendiente(s)")

    def _click(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        col = self.tree.identify_column(event.x)
        iid = self.tree.identify_row(event.y)
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
        data = ActivityInfoDialog(self, activityinfo.build_defaults(self.db, rec)).run()
        if not data:
            return
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
        dx = data.get("dx") or []
        if dx:
            msg += "\n\nDiagnósticos por elegir a mano (CIE-11):\n" + "\n".join(
                f"• {d['abrev']}" + (f" → {d['descripcion']} {d['cie11']}".rstrip() if d['descripcion'] or d['cie11'] else "")
                for d in dx)
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
