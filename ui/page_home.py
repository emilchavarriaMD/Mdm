"""Inicio: panel con estadísticas, accesos rápidos y borradores pendientes."""
from tkinter import ttk

from services import brigades as brigade_svc
from services import stats
from services import visits as visit_svc
from services.validators import fmt_date
from ui import widgets
from ui.page import Page

NO_BRIGADE = "(Todas / ninguna)"


class HomePage(Page):
    nav_key = "home"

    def __init__(self, app):
        super().__init__(app)
        ttk.Label(self, text="Inicio", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Resumen del trabajo de hoy y accesos rápidos.",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self)
        top.pack(fill="x")
        ttk.Label(top, text="Brigada seleccionada:", style="Field.TLabel").pack(side="left")
        self.brigade_combo = widgets.ComboField(top, width=48)
        self.brigade_combo.pack(side="left", padx=8)
        self.brigade_combo.bind("<<ComboboxSelected>>", lambda e: self._brigade_changed())
        ttk.Button(top, text="Administrar brigadas", command=lambda: app.show("brigades")).pack(
            side="left")

        cards = ttk.Frame(self)
        cards.pack(fill="x", pady=14)
        self.card = {}
        specs = [("pacientes", "Pacientes registrados", "total en el sistema"),
                 ("aps_hoy", "Atenciones APS de hoy", ""),
                 ("ssr_hoy", "Atenciones SSR de hoy", ""),
                 ("atendidos", "Atendidos en la brigada", "")]
        for i, (key, title, sub) in enumerate(specs):
            cards.columnconfigure(i, weight=1, uniform="c")
            f = ttk.Frame(cards, style="Card.TFrame", padding=(16, 12))
            f.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0))
            ttk.Label(f, text=title, style="StatCap.TLabel").pack(anchor="w")
            num = ttk.Label(f, text="0", style="StatNum.TLabel")
            num.pack(anchor="w")
            subl = ttk.Label(f, text=sub, style="StatSub.TLabel")
            subl.pack(anchor="w")
            self.card[key] = (num, subl)

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(0, 10))
        ttk.Button(actions, text="Registrar paciente nuevo", style="Accent.TButton",
                   command=lambda: app.show("patient", new=True)).pack(side="left")
        ttk.Button(actions, text="Buscar paciente", command=lambda: app.show("search")).pack(
            side="left", padx=8)
        ttk.Button(actions, text="Historial de atenciones",
                   command=lambda: app.show("history")).pack(side="left")

        lists = ttk.Frame(self)
        lists.pack(fill="both", expand=True)
        lists.columnconfigure(0, weight=1, uniform="l")
        lists.columnconfigure(1, weight=1, uniform="l")
        lists.rowconfigure(1, weight=1)
        self.draft_title = ttk.Label(lists, text="Borradores pendientes (fichas incompletas)",
                                     style="H2.TLabel")
        self.draft_title.grid(row=0, column=0, sticky="w")
        ttk.Label(lists, text="Últimas atenciones registradas", style="H2.TLabel").grid(
            row=0, column=1, sticky="w", padx=(10, 0))
        cols = [("t", "Ficha", 55), ("f", "Fecha", 95), ("p", "Paciente", 150),
                ("d", "Diagnóstico principal", 150)]
        f1, self.drafts = widgets.make_tree(lists, cols, height=9)
        f1.grid(row=1, column=0, sticky="nsew", pady=(6, 0))
        f2, self.recent = widgets.make_tree(lists, cols + [("e", "Estado", 80)], height=9)
        f2.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(6, 0))
        ttk.Label(lists, text="Doble clic sobre una fila para abrir la ficha.",
                  style="Hint.TLabel").grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))
        self.drafts.bind("<Double-1>", lambda e: self._open(self.drafts))
        self.recent.bind("<Double-1>", lambda e: self._open(self.recent))
        self._brigade_map = {}

    def on_show(self, **kw):
        self.refresh()

    def refresh(self):
        brigades = brigade_svc.list_brigades(self.db)
        self._brigade_map = {NO_BRIGADE: None}
        for b in brigades:
            self._brigade_map[brigade_svc.label(b)] = b["id"]
        self.brigade_combo.set_values(list(self._brigade_map))
        cur = self.app.current_brigade_id()
        label = next((k for k, v in self._brigade_map.items() if v == cur), NO_BRIGADE)
        self.brigade_combo.set_value(label)
        self._load()

    def _brigade_changed(self):
        bid = self._brigade_map.get(self.brigade_combo.get_value())
        self.app.set_current_brigade(bid)
        self._load()

    def _load(self):
        bid = self.app.current_brigade_id()
        s = stats.dashboard_stats(self.db, bid)
        self.card["pacientes"][0].configure(text=str(s["pacientes"]))
        self.card["aps_hoy"][0].configure(text=str(s["aps_hoy"]))
        self.card["ssr_hoy"][0].configure(text=str(s["ssr_hoy"]))
        if bid:
            self.card["atendidos"][0].configure(text=str(s["brigada_atendidos"]))
            self.card["atendidos"][1].configure(
                text=f"{s['brigada_consultas']} consultas · {s['brigada_registrados']} registrados")
        else:
            self.card["atendidos"][0].configure(text="–")
            self.card["atendidos"][1].configure(text="Seleccione una brigada")
        self.draft_title.configure(text=f"Borradores pendientes ({s['borradores']})")

        def row(v, with_state=False):
            vals = (visit_svc.KIND_SHORT[v["kind"]], fmt_date(v["fecha_atencion"]), v["paciente"],
                    v["dx"] or "(sin diagnóstico)")
            if with_state:
                vals += ("Borrador" if v["estado"] == "borrador" else "Finalizada",)
            return (f"{v['kind']}:{v['id']}", vals, ["draft"] if v["estado"] == "borrador" else [])

        widgets.fill_tree(self.drafts, [row(v) for v in visit_svc.list_all_visits(
            self.db, estado="borrador", limit=40)])
        widgets.fill_tree(self.recent, [row(v, True) for v in visit_svc.list_all_visits(
            self.db, limit=40)])

    def _open(self, tree):
        iid = widgets.selected_iid(tree)
        if iid:
            kind, vid = iid.split(":")
            self.app.open_visit(kind, int(vid))
