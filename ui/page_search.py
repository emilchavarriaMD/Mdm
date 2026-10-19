"""Buscar pacientes: por nombre, código, historia clínica, teléfono, fecha, brigada, diagnóstico."""
from tkinter import ttk

import config
from reports import excel
from services import patients as patient_svc
from services.validators import ValidationError, fmt_date, parse_date
from ui import common, dialogs, widgets
from ui.page import Page


class SearchPage(Page):
    nav_key = "search"

    def __init__(self, app):
        super().__init__(app)
        ttk.Label(self, text="Buscar pacientes", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Escriba para buscar; los resultados se actualizan solos. "
                  "Doble clic para abrir la Ficha Integral.", style="Muted.TLabel").pack(
            anchor="w", pady=(0, 6))
        box = ttk.LabelFrame(self, text=" Filtros ", padding=(14, 4, 14, 12))
        box.pack(fill="x")
        g = widgets.FormGrid(box, 6)
        self.f = {}

        def add(key, label, w, span=1):
            self.f[key] = w
            g.add(label, w, span=span)

        add("texto", "Nombre, código, historia clínica o teléfono", widgets.EntryField(box), 3)
        add("diagnostico", "Diagnóstico (texto o CIE-11)", widgets.EntryField(box), 3)
        add("desde", "Atenciones desde", widgets.DateEntry(box), 2)
        add("hasta", "Atenciones hasta", widgets.DateEntry(box), 2)
        add("tipo", "Tipo de ficha", widgets.ComboField(box, patient_svc.TIPOS_FICHA), 2)
        add("brigada", "Brigada", widgets.ComboField(box, []), 3)
        self.f["tipo"].set_value("Todos")
        for key in ("texto", "diagnostico"):
            self.f[key].var.trace_add("write", lambda *a: self._schedule())
        for key in ("desde", "hasta"):
            self.f[key].on_change = self._schedule
        for key in ("tipo", "brigada"):
            self.f[key].bind("<<ComboboxSelected>>", lambda e: self.search())
        self.f["texto"].bind("<Return>", lambda e: self.search())
        row = ttk.Frame(box)
        ttk.Button(row, text="Buscar", style="Accent.TButton", command=lambda: self.search(True)).pack(
            side="left")
        ttk.Button(row, text="Limpiar filtros", command=self.clear).pack(side="left", padx=8)
        self.count = ttk.Label(row, text="", style="Muted.TLabel")
        self.count.pack(side="left", padx=12)
        g.full(row)

        frame, self.tree = widgets.make_tree(self, [
            ("codigo", "Código", 85), ("nombre", "Paciente", 220), ("edad", "Edad", 80),
            ("sexo", "Sexo", 100), ("hc", "H. clínica", 100), ("tel", "Teléfono", 100),
            ("proc", "Procedencia", 220), ("brig", "Brigada", 110),
            ("aps", "APS", 50, "center"), ("ssr", "SSR", 50, "center"),
            ("ult", "Última atención", 110)], height=12)
        frame.pack(fill="both", expand=True, pady=(10, 0))
        self.tree.bind("<Double-1>", lambda e: self._open())
        self.tree.bind("<Return>", lambda e: self._open())
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(10, 0))
        ttk.Button(bar, text="Abrir Ficha Integral", style="Accent.TButton",
                   command=self._open).pack(side="left")
        ttk.Button(bar, text="Nueva APS", command=lambda: self._visit("aps")).pack(side="left", padx=8)
        ttk.Button(bar, text="Nueva SSR", command=lambda: self._visit("ssr")).pack(side="left")
        ttk.Button(bar, text="Historial", command=self._history).pack(side="left", padx=8)
        ttk.Button(bar, text="Exportar listado a Excel", command=self.export).pack(side="right")
        self._after = None
        self._rows = []
        self._by_label = {}

    def on_show(self, **kw):
        self.refresh()
        self.search()
        self.f["texto"].focus_set()

    def refresh(self):
        labels, self._by_label, _ = common.brigade_options(self.db, none_label="(Todas)")
        cur = self.f["brigada"].get_value()
        self.f["brigada"].set_values(labels)
        self.f["brigada"].set_value(cur if cur in self._by_label else "(Todas)")

    def clear(self):
        for k in ("texto", "diagnostico", "desde", "hasta"):
            self.f[k].set_value("")
        self.f["tipo"].set_value("Todos")
        self.f["brigada"].set_value("(Todas)")
        self.search()

    def _schedule(self):
        if self._after:
            self.after_cancel(self._after)
        self._after = self.after(300, self.search)

    def search(self, strict=False):
        self._after = None
        dates = {}
        for k in ("desde", "hasta"):
            try:
                dates[k] = parse_date(self.f[k].get_value(), f"Fecha '{k}'")
            except ValidationError as exc:
                if strict:
                    dialogs.show_errors(self, [str(exc)])
                    return
                dates[k] = None
        self._rows = patient_svc.search_patients(
            self.db, texto=self.f["texto"].get_value(), fecha_desde=dates["desde"],
            fecha_hasta=dates["hasta"], brigade_id=self._by_label.get(self.f["brigada"].get_value()),
            diagnostico=self.f["diagnostico"].get_value(), tipo_ficha=self.f["tipo"].get_value())
        widgets.fill_tree(self.tree, [(
            r["id"], (r["codigo"], patient_svc.display_name(r), patient_svc.age_text(r),
                      r["sexo"] or "", r["historia_clinica"] or "", r["telefono"] or "",
                      patient_svc.procedencia(r), r["brigada_codigo"] or "", r["aps_n"], r["ssr_n"],
                      fmt_date(r["ultima"]))) for r in self._rows])
        self.count.configure(text=f"{len(self._rows)} paciente(s) encontrado(s)")

    def _selected(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Seleccione primero un paciente de la lista.")
            return None
        return int(iid)

    def _open(self):
        pid = widgets.selected_iid(self.tree)
        if pid:
            self.app.open_patient(int(pid))
        else:
            dialogs.info(self, "Seleccione primero un paciente de la lista.")

    def _visit(self, kind):
        pid = self._selected()
        if pid:
            self.app.new_visit(kind, pid)

    def _history(self):
        pid = self._selected()
        if pid:
            self.app.set_active(pid)
            self.app.show("history", patient_id=pid)

    def export(self):
        if not self._rows:
            dialogs.info(self, "No hay resultados para exportar.")
            return
        path = dialogs.ask_save_path(self, "Guardar listado en Excel", initialfile="Listado_pacientes.xlsx",
                                     ext=".xlsx", types=[("Excel", "*.xlsx")])
        if not path:
            return
        rows = [[r["codigo"], patient_svc.display_name(r), patient_svc.age_text(r), r["sexo"] or "",
                 r["departamento"] or "", r["municipio"] or "", r["localidad"] or "",
                 r["brigada_codigo"] or "", r["aps_n"], r["ssr_n"], fmt_date(r["ultima"])]
                for r in self._rows]
        rep = {"title": "Listado de pacientes",
               "headers": ["Código", "Paciente", "Edad", "Sexo", "Departamento", "Municipio",
                           "Localidad", "Brigada", "Atenciones APS", "Atenciones SSR",
                           "Última atención"],
               "rows": rows, "filters": "Resultado de la búsqueda actual",
               "notes": [f"Pacientes únicos: {len(rows)}"]}
        try:
            excel.export_report(path, rep, self.db.get_setting("encabezado_institucion", ""))
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear el archivo de Excel:\n{exc}")
            return
        if dialogs.confirm(self, "Excel generado", f"Se guardó:\n{path}", yes="Abrir", no="Cerrar"):
            widgets.open_path(path)
