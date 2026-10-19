"""Reportes y exportaciones (pacientes únicos vs. número de consultas)."""
from datetime import datetime
from tkinter import ttk

from reports import excel
from services import stats
from services.validators import ValidationError, parse_date
from ui import common, dialogs, widgets
from ui.page import Page


class ReportsPage(Page):
    nav_key = "reports"

    def __init__(self, app):
        super().__init__(app)
        self.report = None
        ttk.Label(self, text="Reportes y exportaciones", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Elija el reporte y el período. Los reportes distinguen pacientes únicos "
                  "de consultas totales.", style="Muted.TLabel").pack(anchor="w", pady=(0, 6))
        box = ttk.LabelFrame(self, text=" Opciones ", padding=(14, 4, 14, 12))
        box.pack(fill="x")
        g = widgets.FormGrid(box, 6)
        self.f = {}

        def add(key, label, w, span=1):
            self.f[key] = w
            g.add(label, w, span=span)

        add("reporte", "Reporte", widgets.ComboField(box, list(stats.REPORTS)), 3)
        add("brigada", "Brigada", widgets.ComboField(box, []), 3)
        add("desde", "Desde", widgets.DateEntry(box), 2)
        add("hasta", "Hasta", widgets.DateEntry(box), 2)
        self.final_only = widgets.CheckField(box, text="Solo fichas finalizadas")
        g.add("", self.final_only, span=2)
        self.f["reporte"].set_value(next(iter(stats.REPORTS)))
        row = ttk.Frame(box)
        ttk.Button(row, text="Generar reporte", style="Accent.TButton", command=self.generate).pack(
            side="left")
        ttk.Button(row, text="Exportar a Excel", command=self.export).pack(side="left", padx=8)
        g.full(row)
        self.f["reporte"].bind("<<ComboboxSelected>>", lambda e: self.generate())
        self.f["brigada"].bind("<<ComboboxSelected>>", lambda e: self.generate())

        self.title = ttk.Label(self, text="", style="H2.TLabel")
        self.title.pack(anchor="w", pady=(10, 0))
        self.info = ttk.Label(self, text="", style="Muted.TLabel", wraplength=1000, justify="left")
        self.info.pack(anchor="w")
        frame, self.tree = widgets.make_tree(self, [("c0", "", 100)], height=12)
        frame.pack(fill="both", expand=True, pady=(6, 0))
        self.notes = ttk.Label(self, text="", style="Hint.TLabel", wraplength=1000, justify="left")
        self.notes.pack(anchor="w", pady=(6, 0))
        self._by_label = {}

    def on_show(self, **kw):
        self.refresh()
        self.generate()

    def refresh(self):
        labels, self._by_label, _ = common.brigade_options(self.db, none_label="(Todas las brigadas)")
        cur = self.f["brigada"].get_value()
        self.f["brigada"].set_values(labels)
        if cur not in self._by_label:
            cur_id = self.app.current_brigade_id()
            cur = next((k for k, v in self._by_label.items() if v == cur_id), "(Todas las brigadas)")
        self.f["brigada"].set_value(cur)

    def generate(self):
        try:
            desde = parse_date(self.f["desde"].get_value(), "Desde")
            hasta = parse_date(self.f["hasta"].get_value(), "Hasta")
        except ValidationError as exc:
            dialogs.show_errors(self, [str(exc)])
            return
        label = self.f["brigada"].get_value()
        self.report = stats.run_report(
            self.db, self.f["reporte"].get_value(), desde=desde, hasta=hasta,
            brigade_id=self._by_label.get(label), solo_final=self.final_only.get_value(),
            brigada_txt="" if label.startswith("(") else label)
        rep = self.report
        cols = [f"c{i}" for i in range(len(rep["headers"]))]
        self.tree.configure(columns=cols)
        for i, (c, h) in enumerate(zip(cols, rep["headers"])):
            longest = max([len(str(h))] + [len(str(r[i])) for r in rep["rows"] if len(r) > i])
            self.tree.heading(c, text=h, command=lambda c=c: widgets.sort_tree(self.tree, c, False))
            self.tree.column(c, width=min(max(len(str(h)) * 10 + 28, longest * 8 + 16, 80), 380),
                             minwidth=60)
        widgets.fill_tree(self.tree, [(i, [str(v) for v in row]) for i, row in enumerate(rep["rows"])])
        self.title.configure(text=rep["title"])
        self.info.configure(text=rep.get("filters", ""))
        self.notes.configure(text="\n".join(rep.get("notes", [])))
        if not rep["rows"]:
            self.notes.configure(text="No hay datos para este reporte con los filtros elegidos.")

    def export(self):
        if not self.report or not self.report["rows"]:
            dialogs.info(self, "Genere primero un reporte con datos.")
            return
        name = self.report["title"].replace(" ", "_").replace("/", "-")
        path = dialogs.ask_save_path(
            self, "Guardar reporte en Excel", ext=".xlsx", types=[("Excel", "*.xlsx")],
            initialfile=f"{name}_{datetime.now():%Y%m%d}.xlsx")
        if not path:
            return
        try:
            excel.export_report(path, self.report, self.db.get_setting("encabezado_institucion", ""))
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear el archivo de Excel:\n{exc}")
            return
        if dialogs.confirm(self, "Excel generado", f"Se guardó:\n{path}", yes="Abrir", no="Cerrar"):
            widgets.open_path(path)
