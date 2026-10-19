"""Panel para elegir un paciente (búsqueda rápida) cuando no hay uno activo."""
from tkinter import ttk

from services import patients as patient_svc
from services.validators import fmt_date
from ui import widgets


class PatientPicker(ttk.Frame):
    def __init__(self, master, app, on_pick, title="Seleccione un paciente",
                 hint="Escriba nombre, código, historia clínica o teléfono. Doble clic para elegir."):
        super().__init__(master)
        self.app, self.db, self.on_pick = app, app.db, on_pick
        ttk.Label(self, text=title, style="H2.TLabel").pack(anchor="w")
        ttk.Label(self, text=hint, style="Muted.TLabel").pack(anchor="w", pady=(2, 8))
        row = ttk.Frame(self)
        row.pack(fill="x")
        self.entry = widgets.EntryField(row, width=50)
        self.entry.pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Registrar paciente nuevo", style="Accent.TButton",
                   command=lambda: app.show("patient", new=True)).pack(side="left", padx=(10, 0))
        frame, self.tree = widgets.make_tree(self, [
            ("codigo", "Código", 90), ("nombre", "Paciente", 260), ("edad", "Edad", 80),
            ("sexo", "Sexo", 90), ("hc", "Historia clínica", 120),
            ("proc", "Procedencia", 240), ("ult", "Última atención", 120)], height=10)
        frame.pack(fill="both", expand=True, pady=(10, 0))
        self._after = None
        self.entry.var.trace_add("write", lambda *a: self._schedule())
        self.tree.bind("<Double-1>", lambda e: self._pick())
        self.tree.bind("<Return>", lambda e: self._pick())
        self.entry.bind("<Return>", lambda e: self._pick_first())
        self.entry.bind("<Down>", lambda e: self._focus_tree())

    def start(self):
        self.entry.set_value("")
        self.search()
        self.entry.focus_set()

    def _schedule(self):
        if self._after:
            self.after_cancel(self._after)
        self._after = self.after(250, self.search)

    def search(self):
        self._after = None
        rows = patient_svc.search_patients(self.db, texto=self.entry.get_value(), limit=150)
        widgets.fill_tree(self.tree, [(
            r["id"], (r["codigo"], patient_svc.display_name(r), patient_svc.age_text(r), r["sexo"] or "",
                      r["historia_clinica"] or "", patient_svc.procedencia(r),
                      fmt_date(r["ultima"]))) for r in rows])

    def _focus_tree(self):
        kids = self.tree.get_children("")
        if kids:
            self.tree.selection_set(kids[0])
            self.tree.focus(kids[0])
            self.tree.focus_set()

    def _pick_first(self):
        kids = self.tree.get_children("")
        if len(kids) >= 1:
            self.on_pick(int(kids[0]))

    def _pick(self):
        iid = widgets.selected_iid(self.tree)
        if iid:
            self.on_pick(int(iid))
