"""Historial de atenciones (APS y SSR) con filtros."""
from tkinter import ttk

import config
from reports import excel, pdf
from services import patients as patient_svc
from services import visits as visit_svc
from services.validators import ValidationError, fmt_date, parse_date
from ui import common, dialogs, widgets
from ui.page import Page


class HistoryPage(Page):
    nav_key = "history"

    def __init__(self, app):
        super().__init__(app)
        self.patient_id = None
        ttk.Label(self, text="Historial de atenciones", style="H1.TLabel").pack(anchor="w")
        self.chip = ttk.Frame(self, style="Strip.TFrame", padding=(12, 6))
        self.chip_lbl = ttk.Label(self.chip, text="", style="StripB.TLabel")
        self.chip_lbl.pack(side="left")
        ttk.Button(self.chip, text="Ver todos los pacientes", style="Strip.TButton",
                   command=self._all_patients).pack(side="right")
        box = ttk.LabelFrame(self, text=" Filtros ", padding=(14, 4, 14, 12))
        box.pack(fill="x", pady=(6, 0))
        g = widgets.FormGrid(box, 6)
        self.f = {}

        def add(key, label, w, span=1):
            self.f[key] = w
            g.add(label, w, span=span)

        add("texto", "Paciente (nombre o código)", widgets.EntryField(box), 2)
        add("diagnostico", "Diagnóstico (texto o CIE-11)", widgets.EntryField(box), 2)
        add("brigada", "Brigada", widgets.ComboField(box, []), 2)
        add("desde", "Desde", widgets.DateEntry(box), 2)
        add("hasta", "Hasta", widgets.DateEntry(box), 2)
        add("tipo", "Tipo de ficha", widgets.ComboField(box, ["Todas", "APS", "SSR"]), 1)
        add("estado", "Estado", widgets.ComboField(box, ["Todos", "Borrador", "Finalizada"]), 1)
        self.f["tipo"].set_value("Todas")
        self.f["estado"].set_value("Todos")
        for key in ("texto", "diagnostico"):
            self.f[key].var.trace_add("write", lambda *a: self._schedule())
        for key in ("desde", "hasta"):
            self.f[key].on_change = self._schedule
        for key in ("tipo", "estado", "brigada"):
            self.f[key].bind("<<ComboboxSelected>>", lambda e: self.search())
        row = ttk.Frame(box)
        ttk.Button(row, text="Buscar", style="Accent.TButton", command=self.search).pack(side="left")
        ttk.Button(row, text="Limpiar filtros", command=self.clear).pack(side="left", padx=8)
        self.count = ttk.Label(row, text="", style="Muted.TLabel")
        self.count.pack(side="left", padx=12)
        g.full(row)

        frame, self.tree = widgets.make_tree(self, [
            ("t", "Ficha", 55), ("f", "Fecha", 95), ("p", "Paciente", 210), ("c", "Código", 80),
            ("d", "Diagnóstico principal", 260), ("m", "Personal", 160), ("b", "Brigada", 90),
            ("e", "Estado", 90)], height=12)
        frame.pack(fill="both", expand=True, pady=(10, 0))
        self.tree.bind("<Double-1>", lambda e: self._open())
        self.tree.bind("<Return>", lambda e: self._open())
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(10, 0))
        ttk.Button(bar, text="Abrir ficha", style="Accent.TButton", command=self._open).pack(side="left")
        ttk.Button(bar, text="Exportar PDF", command=self.export_pdf).pack(side="left", padx=8)
        ttk.Button(bar, text="Imprimir", command=self.print_pdf).pack(side="left")
        ttk.Button(bar, text="Exportar listado a Excel", command=self.export_excel).pack(side="right")
        self._rows, self._by_label, self._after = [], {}, None

    def on_show(self, patient_id=None, **kw):
        self.patient_id = patient_id
        self.refresh()
        self.search()

    def refresh(self):
        labels, self._by_label, _ = common.brigade_options(self.db, none_label="(Todas)")
        cur = self.f["brigada"].get_value()
        self.f["brigada"].set_values(labels)
        self.f["brigada"].set_value(cur if cur in self._by_label else "(Todas)")
        if self.patient_id:
            p = patient_svc.get_patient(self.db, self.patient_id)
            if p:
                self.chip_lbl.configure(
                    text=f"Mostrando solo las atenciones de: {patient_svc.display_name(p)} ({p['codigo']})")
                self.chip.pack(fill="x", pady=(6, 0), after=self.winfo_children()[0])
                return
            self.patient_id = None
        self.chip.pack_forget()

    def _all_patients(self):
        self.patient_id = None
        self.refresh()
        self.search()

    def clear(self):
        for k in ("texto", "diagnostico", "desde", "hasta"):
            self.f[k].set_value("")
        self.f["tipo"].set_value("Todas")
        self.f["estado"].set_value("Todos")
        self.f["brigada"].set_value("(Todas)")
        self.search()

    def _schedule(self):
        if self._after:
            self.after_cancel(self._after)
        self._after = self.after(300, self.search)

    def search(self):
        self._after = None
        dates = {}
        for k in ("desde", "hasta"):
            try:
                dates[k] = parse_date(self.f[k].get_value(), "Fecha")
            except ValidationError:
                dates[k] = None
        tipo = {"APS": "aps", "SSR": "ssr"}.get(self.f["tipo"].get_value())
        estado = {"Borrador": "borrador", "Finalizada": "finalizada"}.get(self.f["estado"].get_value())
        self._rows = visit_svc.list_all_visits(
            self.db, patient_id=self.patient_id, texto=self.f["texto"].get_value(),
            fecha_desde=dates["desde"], fecha_hasta=dates["hasta"],
            brigade_id=self._by_label.get(self.f["brigada"].get_value()), kind=tipo, estado=estado,
            diagnostico=self.f["diagnostico"].get_value())
        widgets.fill_tree(self.tree, [(
            f"{v['kind']}:{v['id']}",
            (visit_svc.KIND_SHORT[v["kind"]], fmt_date(v["fecha_atencion"]), v["paciente"],
             v["codigo"], v["dx"] or "", v["personal"] or "", v["brigada"] or "",
             "Borrador" if v["estado"] == "borrador" else "Finalizada"),
            ["draft"] if v["estado"] == "borrador" else []) for v in self._rows])
        pacientes = len({v["patient_id"] for v in self._rows})
        self.count.configure(text=f"{len(self._rows)} atención(es) · {pacientes} paciente(s) único(s)")

    def _sel(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Seleccione primero una atención de la lista.")
            return None, None
        kind, vid = iid.split(":")
        return kind, int(vid)

    def _open(self):
        kind, vid = self._sel()
        if kind:
            self.app.open_visit(kind, vid)

    def _make_pdf(self, kind, vid, path):
        (pdf.aps_pdf if kind == "aps" else pdf.ssr_pdf)(self.db, vid, path)

    def export_pdf(self):
        kind, vid = self._sel()
        if not kind:
            return
        row = next(v for v in self._rows if v["kind"] == kind and v["id"] == vid)
        path = dialogs.ask_save_path(
            self, "Guardar ficha en PDF",
            initialfile=f"{visit_svc.KIND_SHORT[kind]}_{row['codigo']}_{row['fecha_atencion'].replace('-', '')}.pdf")
        if not path:
            return
        try:
            self._make_pdf(kind, vid, path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo generar el PDF:\n{exc}")
            return
        if dialogs.confirm(self, "PDF generado", f"Se guardó:\n{path}", yes="Abrir PDF", no="Cerrar"):
            widgets.open_path(path)

    def print_pdf(self):
        kind, vid = self._sel()
        if not kind:
            return
        path = config.exports_dir() / f"imprimir_{kind}_{vid}.pdf"
        try:
            self._make_pdf(kind, vid, path)
            widgets.open_path(path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo preparar la impresión:\n{exc}")

    def export_excel(self):
        if not self._rows:
            dialogs.info(self, "No hay atenciones para exportar.")
            return
        path = dialogs.ask_save_path(self, "Guardar listado en Excel", initialfile="Listado_atenciones.xlsx",
                                     ext=".xlsx", types=[("Excel", "*.xlsx")])
        if not path:
            return
        rows = [[visit_svc.KIND_SHORT[v["kind"]], fmt_date(v["fecha_atencion"]), v["codigo"],
                 v["paciente"], v["dx"] or "", v["personal"] or "", v["brigada"] or "",
                 "Borrador" if v["estado"] == "borrador" else "Finalizada"] for v in self._rows]
        rep = {"title": "Listado de atenciones",
               "headers": ["Ficha", "Fecha", "Código", "Paciente", "Diagnóstico principal",
                           "Personal", "Brigada", "Estado"],
               "rows": rows, "filters": "Resultado del historial actual",
               "notes": [f"Total de consultas: {len(rows)}",
                         f"Pacientes únicos: {len({v['patient_id'] for v in self._rows})}"]}
        try:
            excel.export_report(path, rep, self.db.get_setting("encabezado_institucion", ""))
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear el archivo de Excel:\n{exc}")
            return
        if dialogs.confirm(self, "Excel generado", f"Se guardó:\n{path}", yes="Abrir", no="Cerrar"):
            widgets.open_path(path)
