"""Registro de brigadas médicas y vista de sus pacientes, diagnósticos y atenciones."""
import json
from datetime import date
from tkinter import ttk

from reports import excel
from services import brigades as brigade_svc
from services.validators import fmt_date
from ui import common, dialogs, widgets
from ui.page import Page


class BrigadesPage(Page):
    nav_key = "brigades"

    def __init__(self, app):
        super().__init__(app)
        self.bid = None
        self._clean = None
        self._patients = []
        ttk.Label(self, text="Brigadas médicas", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Cree la brigada del día, márquela como 'actual' y los pacientes y "
                  "atenciones nuevos se le asociarán automáticamente.", style="Muted.TLabel").pack(
            anchor="w", pady=(0, 6))
        self.scroll = widgets.ScrollFrame(self)
        self.scroll.pack(fill="both", expand=True)
        body = self.scroll.body
        top = ttk.Frame(body)
        top.pack(fill="x")
        top.columnconfigure(0, weight=3, uniform="b")
        top.columnconfigure(1, weight=4, uniform="b")

        left = ttk.Frame(top)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        ttk.Label(left, text="Brigadas registradas", style="H2.TLabel").pack(anchor="w")
        frame, self.tree = widgets.make_tree(left, [("c", "Código", 95), ("n", "Nombre", 130),
                                                    ("f", "Fecha", 100), ("a", "Actual", 60, "center")],
                                             height=9)
        frame.pack(fill="both", expand=True, pady=(6, 6))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        ttk.Button(left, text="+ Nueva brigada", command=self.new).pack(anchor="w")

        right = ttk.LabelFrame(top, text=" Datos de la brigada ", padding=(14, 4, 14, 12))
        right.grid(row=0, column=1, sticky="nsew")
        g = widgets.FormGrid(right, 2)
        self.f = {}

        def add(key, label, w, **kw):
            self.f[key] = w
            g.add(label, w, **kw)

        add("codigo", "Código de la brigada", widgets.EntryField(right), required=True)
        add("nombre", "Nombre de la brigada", widgets.EntryField(right), required=True)
        add("fecha", "Fecha", widgets.DateEntry(right, show_today=True), required=True)
        add("departamento", "Departamento", widgets.ComboField(right, [], readonly=True))
        add("municipio", "Municipio", widgets.ComboField(right, [], readonly=False))
        add("localidad", "Localidad o comunidad", widgets.ComboField(right, [], readonly=False))
        add("lugar", "Establecimiento o lugar de atención", widgets.EntryField(right), span=2)
        add("personal", "Personal participante (uno por línea)", widgets.TextBox(right, height=3), span=2)
        add("observaciones", "Observaciones", widgets.TextBox(right, height=2), span=2)
        btns = ttk.Frame(right)
        ttk.Button(btns, text="Guardar brigada", style="Accent.TButton", command=self.save).pack(
            side="left")
        self.btn_current = ttk.Button(btns, text="Usar como brigada actual", command=self.make_current)
        self.btn_current.pack(side="left", padx=8)
        self.btn_delete = ttk.Button(btns, text="Eliminar", style="Danger.TButton", command=self.delete)
        self.btn_delete.pack(side="left")
        self.status = ttk.Label(btns, text="", style="Saved.TLabel")
        self.status.pack(side="left", padx=10)
        g.full(btns, pady=(12, 0))

        bottom = widgets.section(body, "Pacientes de la brigada seleccionada", pady=(14, 0))
        self.summary = ttk.Label(bottom, text="Seleccione una brigada guardada.", style="Muted.TLabel")
        self.summary.pack(anchor="w")
        frame2, self.ptree = widgets.make_tree(bottom, [
            ("c", "Código", 80), ("n", "Paciente", 210), ("e", "Edad", 70), ("s", "Sexo", 80),
            ("a", "APS", 45, "center"), ("r", "SSR", 45, "center"),
            ("d", "Diagnósticos registrados", 420)], height=8)
        frame2.pack(fill="both", expand=True, pady=(6, 6))
        self.ptree.bind("<Double-1>", lambda e: self._open_patient())
        row = ttk.Frame(bottom)
        row.pack(fill="x")
        ttk.Button(row, text="Abrir Ficha Integral", command=self._open_patient).pack(side="left")
        ttk.Button(row, text="Exportar a Excel", command=self.export).pack(side="right")

    # ------------------------------------------------------------------
    def on_show(self, **kw):
        self.refresh()
        if self.bid is None:
            cur = self.app.current_brigade_id()
            if cur:
                self._select(cur)
            else:
                self.new(force=True)

    def refresh(self):
        self.f["departamento"].set_values([""] + self.db.catalog("departamento"))
        self.f["municipio"].set_values(common.known_values(self.db, "brigades", "municipio"))
        self.f["localidad"].set_values(common.known_values(self.db, "brigades", "localidad"))
        cur = self.app.current_brigade_id()
        widgets.fill_tree(self.tree, [(
            b["id"], (b["codigo"], b["nombre"], fmt_date(b["fecha"]), "●" if b["id"] == cur else ""))
            for b in brigade_svc.list_brigades(self.db)])
        if self.bid and self.tree.exists(str(self.bid)):
            self.tree.selection_set(str(self.bid))

    def collect(self):
        return {k: w.get_value() for k, w in self.f.items()}

    def _mark_clean(self):
        self._clean = json.dumps(self.collect(), sort_keys=True)

    def is_dirty(self):
        return self._clean is not None and json.dumps(self.collect(), sort_keys=True) != self._clean

    def can_leave(self):
        if not self.is_dirty():
            return True
        choice = dialogs.unsaved_changes(self, "Guardar brigada")
        if choice == "cancel":
            return False
        if choice == "save":
            return self.save()
        self._mark_clean()
        return True

    def on_save_shortcut(self):
        self.save()

    def new(self, force=False):
        if not force and not self.can_leave():
            return
        self.bid = None
        for w in self.f.values():
            w.set_value("")
        self.f["fecha"].set_value(date.today().isoformat())
        self.tree.selection_remove(self.tree.selection())
        self.btn_current.state(["disabled"])
        self.btn_delete.state(["disabled"])
        self.summary.configure(text="Guarde la brigada para ver sus pacientes.")
        widgets.fill_tree(self.ptree, [])
        self._mark_clean()
        self.status.configure(text="")
        self.f["codigo"].focus_set()

    def _on_select(self, _e=None):
        iid = widgets.selected_iid(self.tree)
        if iid and int(iid) != self.bid:
            if not self.can_leave():
                if self.bid and self.tree.exists(str(self.bid)):
                    self.tree.selection_set(str(self.bid))
                return
            self._select(int(iid))

    def _select(self, bid):
        b = brigade_svc.get_brigade(self.db, bid)
        if not b:
            return
        self.bid = bid
        for k, w in self.f.items():
            w.set_value(b.get(k) or "")
        if self.tree.exists(str(bid)):
            self.tree.selection_set(str(bid))
        self.btn_current.state(["!disabled"])
        self.btn_delete.state(["!disabled"])
        self._mark_clean()
        self.status.configure(text="")
        self._load_patients()

    def _load_patients(self):
        s = brigade_svc.brigade_summary(self.db, self.bid)
        self.summary.configure(
            text=f"Pacientes atendidos: {s['atendidos']}   ·   Registrados en la brigada: "
                 f"{s['registrados']}   ·   Atenciones APS: {s['aps']}   ·   Atenciones SSR: {s['ssr']}")
        self._patients = brigade_svc.brigade_patients(self.db, self.bid)
        widgets.fill_tree(self.ptree, [(
            p["id"], (p["codigo"], f"{p['nombres']} {p['apellidos']}", p["edad"], p["sexo"] or "",
                      p["aps_n"], p["ssr_n"], p["diagnosticos"])) for p in self._patients])

    def save(self):
        data, errors = brigade_svc.prepare_brigade(self.collect())
        if errors:
            dialogs.show_errors(self, errors)
            return False
        try:
            bid = brigade_svc.save_brigade(self.db, data, self.bid)
        except ValueError as exc:
            dialogs.show_errors(self, [str(exc)])
            return False
        self.bid = bid
        if not self.app.current_brigade_id():
            self.app.set_current_brigade(bid)
        self.refresh()
        self._select(bid)
        self.app.refresh_all()
        self.status.configure(text=f"Brigada guardada a las {common.now_hhmm()}")
        return True

    def make_current(self):
        if self.bid is None or self.is_dirty() and not self.save():
            return
        self.app.set_current_brigade(self.bid)
        self.refresh()
        self.status.configure(text="Esta es ahora la brigada actual.")

    def delete(self):
        if self.bid is None:
            return
        if not dialogs.confirm(self, "Eliminar brigada",
                               "¿Eliminar esta brigada? Solo es posible si no tiene pacientes ni "
                               "atenciones asociadas.", yes="Eliminar", no="Cancelar", danger=True):
            return
        try:
            brigade_svc.delete_brigade(self.db, self.bid)
        except ValueError as exc:
            dialogs.error(self, str(exc))
            return
        if self.app.current_brigade_id() == self.bid:
            self.app.set_current_brigade(None)
        self.bid = None
        self.refresh()
        self.new(force=True)
        self.app.refresh_all()

    def _open_patient(self):
        iid = widgets.selected_iid(self.ptree)
        if iid:
            self.app.open_patient(int(iid))
        else:
            dialogs.info(self, "Seleccione un paciente de la lista.")

    def export(self):
        if self.bid is None or not self._patients:
            dialogs.info(self, "No hay pacientes para exportar en esta brigada.")
            return
        b = brigade_svc.get_brigade(self.db, self.bid)
        path = dialogs.ask_save_path(self, "Guardar listado en Excel",
                                     initialfile=f"Brigada_{b['codigo']}.xlsx", ext=".xlsx",
                                     types=[("Excel", "*.xlsx")])
        if not path:
            return
        rows = [[p["codigo"], f"{p['nombres']} {p['apellidos']}", p["edad"], p["sexo"] or "",
                 p["aps_n"], p["ssr_n"], p["diagnosticos"]] for p in self._patients]
        rep = {"title": f"Brigada {b['codigo']} – pacientes", "filters": brigade_svc.label(b),
               "headers": ["Código", "Paciente", "Edad", "Sexo", "Atenciones APS", "Atenciones SSR",
                           "Diagnósticos"], "rows": rows,
               "notes": [f"Pacientes únicos: {len(rows)}"]}
        try:
            excel.export_report(path, rep, self.db.get_setting("encabezado_institucion", ""))
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear el archivo de Excel:\n{exc}")
            return
        if dialogs.confirm(self, "Excel generado", f"Se guardó:\n{path}", yes="Abrir", no="Cerrar"):
            widgets.open_path(path)
