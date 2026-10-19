"""Fichas de atención APS y SSR (un evento clínico independiente por fecha)."""
import json
import re
from datetime import date
from tkinter import ttk

import config
from reports import pdf
from services import clinical
from services import patients as patient_svc
from services import visits as visit_svc
from services.validators import (ValidationError, check_vitals, fmt_date, fmt_number,
                                 parse_date, VITALS)
from ui import common, dialogs, widgets
from ui.page import Page
from ui.picker import PatientPicker

NEW_LABEL = "+ Nueva atención"
PRUEBAS_COMUNES = ["Prueba de embarazo", "Examen general de orina", "Cinta reactiva de orina",
                   "Prueba rápida de VIH", "Prueba rápida de sífilis", "Glucometría",
                   "Examen con espéculo", "Otra"]
NUM_KEYS = {"pas", "pad", "fc", "fr", "temperatura", "peso", "metodo_cantidad"}


# ---------------------------------------------------------------------------
# Filas dinámicas
# ---------------------------------------------------------------------------

class MedRow:
    """Un medicamento del plan terapéutico (prescrito vs. entregado por separado)."""

    def __init__(self, parent, remove_cb, ctx):
        self.frame = ttk.LabelFrame(parent, text=" Medicamento ", padding=(10, 2, 10, 10))
        f = self.frame
        g = widgets.FormGrid(f, 4)
        self.f = {}

        def add(key, label, w, **kw):
            self.f[key] = w
            g.add(label, w, **kw)

        add("generico", "Nombre genérico", widgets.ComboField(f, ctx["meds"], readonly=False),
            span=2)
        add("presentacion", "Presentación y concentración", widgets.EntryField(f))
        add("dosis", "Dosis", widgets.EntryField(f))
        add("via", "Vía de administración", widgets.ComboField(f, ctx["vias"], readonly=False))
        add("frecuencia", "Frecuencia", widgets.EntryField(f))
        add("horario", "Horario específico (si corresponde)", widgets.EntryField(f))
        add("duracion", "Duración del tratamiento", widgets.EntryField(f))
        add("cant_prescrita", "Cantidad TOTAL PRESCRITA", widgets.EntryField(f))
        add("cant_entregada", "Cantidad ENTREGADA al paciente", widgets.EntryField(f))
        add("unidad", "Unidad", widgets.ComboField(f, ctx["units"], readonly=False))
        add("indicaciones", "Indicaciones especiales", widgets.EntryField(f), span=2)
        bottom = ttk.Frame(f)
        ttk.Button(bottom, text="Quitar medicamento", style="Danger.TButton",
                   command=remove_cb).pack(side="right")
        g.full(bottom)

    def get(self):
        return {k: w.get_value() for k, w in self.f.items()}

    def set(self, d):
        for k, w in self.f.items():
            v = d.get(k)
            w.set_value(fmt_number(v) if k in ("cant_prescrita", "cant_entregada")
                        and v not in (None, "") else ("" if v is None else v))

    def focus(self):
        self.f["generico"].focus_set()


class DxRow:
    """Un diagnóstico: descripción, código CIE-11 (solo si se verificó) y observaciones."""

    def __init__(self, parent, remove_cb=None, title=" Diagnóstico secundario "):
        self.frame = ttk.LabelFrame(parent, text=title, padding=(10, 2, 10, 10)) \
            if title else ttk.Frame(parent)
        f = self.frame
        g = widgets.FormGrid(f, 4)
        self.f = {}

        def add(key, label, w, **kw):
            self.f[key] = w
            g.add(label, w, **kw)

        add("descripcion", "Descripción del diagnóstico", widgets.EntryField(f), span=2)
        add("cie11", "Código CIE-11", widgets.EntryField(f, width=12))
        add("cie11_verificado", "", widgets.CheckField(f, text="Código verificado"))
        add("observaciones", "Observaciones", widgets.EntryField(f), span=3)
        if remove_cb:
            ttk.Button(f, text="Quitar", style="Danger.TButton", command=remove_cb).grid(
                row=g.r * 3 + 1, column=3, sticky="e", pady=(2, 0))

    def get(self):
        return {k: w.get_value() for k, w in self.f.items()}

    def set(self, d):
        for k, w in self.f.items():
            v = d.get(k)
            w.set_value(v if v is not None else "")

    def focus(self):
        self.f["descripcion"].focus_set()


class TestRow:
    def __init__(self, parent, remove_cb):
        self.frame = ttk.LabelFrame(parent, text=" Prueba ", padding=(10, 2, 10, 10))
        f = self.frame
        g = widgets.FormGrid(f, 4)
        self.f = {}

        def add(key, label, w, **kw):
            self.f[key] = w
            g.add(label, w, **kw)

        add("prueba", "Prueba", widgets.ComboField(f, PRUEBAS_COMUNES, readonly=False), span=2)
        add("estado", "Estado", widgets.ComboField(f, visit_svc.PRUEBA_ESTADOS))
        add("resultado", "Resultado (solo si se realizó)", widgets.EntryField(f), span=2)
        add("motivo", "Motivo si no se realizó", widgets.EntryField(f), span=2)
        ttk.Button(f, text="Quitar", style="Danger.TButton", command=remove_cb).grid(
            row=g.r * 3 + 1, column=3, sticky="e", pady=(2, 0))
        self.f["estado"].set_value("Realizada")

    def get(self):
        return {k: w.get_value() for k, w in self.f.items()}

    def set(self, d):
        for k, w in self.f.items():
            w.set_value(d.get(k) or ("Realizada" if k == "estado" else ""))

    def focus(self):
        self.f["prueba"].focus_set()


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------

class VisitPage(Page):
    def __init__(self, app, kind):
        super().__init__(app)
        self.kind = kind
        self.nav_key = kind
        self.short = visit_svc.KIND_SHORT[kind]
        self.pid = self.vid = self.patient = None
        self.estado = "nuevo"  # nuevo | borrador | finalizada
        self.locked = False
        self._clean = None
        self.hea_origen = "manual"
        self.w = {}
        self.exam_w = {}
        self.inter_w = {}
        self._visit_map = {}
        self._prev_choice = NEW_LABEL

        head = ttk.Frame(self)
        head.pack(fill="x")
        ttk.Label(head, text=visit_svc.KIND_NAMES[kind], style="H1.TLabel").pack(side="left")
        self.badge = ttk.Label(head, text="", style="Draft.TLabel")
        self.badge.pack(side="left", padx=14)
        self.dirty_lbl = ttk.Label(head, text="", style="Dirty.TLabel")
        self.dirty_lbl.pack(side="left")

        self.picker_box = ttk.Frame(self)
        self.picker = PatientPicker(
            self.picker_box, app, on_pick=lambda pid: app.new_visit(kind, pid),
            title=f"¿A qué paciente se le registra la atención {self.short}?")
        self.picker.pack(fill="both", expand=True, pady=(12, 0))

        self.form_box = ttk.Frame(self)
        self._build_bar()
        self._build_top()
        self.nb = ttk.Notebook(self.form_box)
        self.nb.pack(fill="both", expand=True, pady=(8, 0))
        self._build_tabs()

    # ------------------------------------------------------------------ utilidades UI
    def _reg(self, grid, key, label, widget, **kw):
        self.w[key] = widget
        return grid.add(label, widget, **kw)

    def _tab(self, title):
        sf = widgets.ScrollFrame(self.nb)
        self.nb.add(sf, text=title)
        inner = ttk.Frame(sf.body, padding=(4, 10, 8, 10))
        inner.pack(fill="both", expand=True)
        return inner

    def _build_top(self):
        info = ttk.Frame(self.form_box, style="Strip.TFrame", padding=(12, 6))
        info.pack(fill="x")
        left = ttk.Frame(info, style="Strip.TFrame")
        left.pack(side="left")
        self.pt_lbl = ttk.Label(left, text="", style="StripB.TLabel")
        self.pt_lbl.pack(anchor="w")
        self.pt_info = ttk.Label(left, text="", style="Strip.TLabel")
        self.pt_info.pack(anchor="w")
        right = ttk.Frame(info, style="Strip.TFrame")
        right.pack(side="right")
        self.btn_log = ttk.Button(right, text="Ver cambios", style="Strip.TButton",
                                  command=self.show_log)
        self.btn_log.pack(side="right")
        self.btn_print = ttk.Button(right, text="Imprimir", style="Strip.TButton",
                                    command=self.print_pdf)
        self.btn_print.pack(side="right", padx=6)
        self.btn_pdf = ttk.Button(right, text="Exportar PDF", style="Strip.TButton",
                                  command=self.export_pdf)
        self.btn_pdf.pack(side="right")
        ttk.Button(right, text="Ficha Integral", style="Strip.TButton",
                   command=lambda: self.app.open_patient(self.pid)).pack(side="right", padx=(0, 6))
        sel = ttk.Frame(self.form_box)
        sel.pack(fill="x", pady=(8, 0))
        ttk.Label(sel, text="Atención:", style="Field.TLabel").pack(side="left")
        self.visit_combo = widgets.keep_enabled(widgets.ComboField(sel, [NEW_LABEL], width=62))
        self.visit_combo.pack(side="left", padx=8)
        self.visit_combo.bind("<<ComboboxSelected>>", self._on_pick_visit)
        widgets.keep_enabled(ttk.Button(sel, text="Nueva atención", command=self._new_clicked)).pack(
            side="left")
        for b in (self.btn_pdf, self.btn_print, self.btn_log):
            widgets.keep_enabled(b)
        self.bar_buttons += [self.btn_pdf, self.btn_print, self.btn_log]

    def _build_bar(self):
        bar = ttk.Frame(self.form_box)
        bar.pack(side="bottom", fill="x", pady=(10, 0))
        ttk.Separator(bar).pack(fill="x", pady=(0, 10))
        ttk.Button(bar, text="← Regresar", command=self.app.back).pack(side="left")
        self.btn_cancel = ttk.Button(bar, text="Cancelar cambios", command=self.cancel)
        self.btn_cancel.pack(side="left", padx=8)
        self.btn_delete = ttk.Button(bar, text="Eliminar borrador", style="Danger.TButton",
                                     command=self.delete_draft)
        self.btn_delete.pack(side="left")
        self.status = ttk.Label(bar, text="", style="Saved.TLabel")
        self.status.pack(side="left", padx=12)
        self.btn_final = ttk.Button(bar, text="Finalizar ficha", style="Accent.TButton",
                                    command=lambda: self.save(True))
        self.btn_final.pack(side="right")
        self.btn_draft = ttk.Button(bar, text="Guardar borrador", command=lambda: self.save(False))
        self.btn_draft.pack(side="right", padx=8)
        self.btn_edit = ttk.Button(bar, text="Editar ficha", style="Accent.TButton",
                                   command=self.unlock)
        self.bar_buttons = [self.btn_cancel, self.btn_delete, self.btn_final, self.btn_draft,
                            self.btn_edit]
        for b in self.bar_buttons:
            widgets.keep_enabled(b)

    # ------------------------------------------------------------------ pestañas
    def _build_tabs(self):
        self._build_tab_datos()
        self._build_tab_hea()
        self._build_tab_clinica()
        self._build_tab_dx()
        self._build_tab_plan()

    # -- 1. datos de la atención
    def _build_tab_datos(self):
        t = self._tab("1. Datos")
        s = widgets.section(t, "Datos administrativos")
        g = widgets.FormGrid(s, 3)
        self._reg(g, "fecha_atencion", f"Fecha de atención {self.short}",
                  widgets.DateEntry(s, show_today=True, on_change=self._update_same_day),
                  required=True)
        self._reg(g, "personal", "Personal médico que brinda la atención",
                  widgets.ComboField(s, [], readonly=False),
                  hint="Obligatorio para finalizar. Escriba un nombre nuevo y quedará en la lista.")
        self._reg(g, "brigade", "Brigada médica", widgets.ComboField(s, [], width=36))
        self._reg(g, "lugar", "Lugar de atención", widgets.ComboField(s, [], readonly=False))
        if self.kind == "aps":
            self._reg(g, "historia_clinica", "Número de historia clínica", widgets.EntryField(s))
        else:
            self._reg(g, "categoria", "Categoría de atención",
                      widgets.ComboField(s, [], readonly=False),
                      hint="Obligatoria para finalizar. La lista es configurable.")
            self._reg(g, "motivo", "Motivo de consulta", widgets.EntryField(s), span=2)
        # pregunta "mismo día"
        g.newline()
        box = ttk.Frame(s)
        q = ("¿Se brindó atención APS el mismo día en que se creó la Ficha Integral?"
             if self.kind == "aps" else "¿Se brindó atención SSR el mismo día que la atención APS?")
        ttk.Label(box, text=q + " *", style="Field.TLabel").pack(anchor="w")
        row = ttk.Frame(box)
        row.pack(anchor="w", pady=(2, 0))
        options = ["Sí", "No"] if self.kind == "aps" else visit_svc.SAME_DAY_APS
        self.same_combo = widgets.ComboField(row, options, width=30)
        self.same_combo.pack(side="left")
        self.same_manual = widgets.CheckField(row, text="Corregir manualmente")
        self.same_manual.configure(command=self._update_same_day)
        self.same_manual.pack(side="left", padx=12)
        self.same_info = ttk.Label(box, text="", style="Hint.TLabel", wraplength=720,
                                   justify="left")
        self.same_info.pack(anchor="w", pady=(4, 0))
        g.full(box)
        self._reg(g, "observaciones", "Observaciones clínicas", widgets.TextBox(s, height=2),
                  span=3)

    # -- 2. HEA
    def _build_tab_hea(self):
        t = self._tab("2. Historia (HEA)")
        ttk.Label(
            t, style="Note.TLabel", wraplength=900, justify="left",
            text="Importante: el diagnóstico por sí solo NO demuestra que el paciente tenga los "
                 "síntomas típicos de esa enfermedad. Escriba solo lo que el paciente refiere. "
                 "El borrador se arma únicamente con lo que usted escriba y marca como PENDIENTE "
                 "lo que falta; nunca agrega síntomas.").pack(fill="x", pady=(0, 10))
        s = widgets.section(t, "Datos del interrogatorio")
        g = widgets.FormGrid(s, 2)
        if self.kind == "aps":
            for key, label, _core in clinical.APS_HEA_FIELDS:
                self._reg(g, key, label, widgets.TextBox(s, height=2))
        else:
            for key, label in clinical.SSR_HEA_FIELDS:
                if key in ("fum", "hea_fecha_ultima_dosis"):
                    self._reg(g, key, label, widgets.DateEntry(s))
                else:
                    self._reg(g, key, label, widgets.TextBox(s, height=2))
        s2 = widgets.section(t, "Redacción de la HEA")
        btns = widgets.button_row(s2, [
            ("Ver preguntas sugeridas", self.suggest_questions),
            ("Generar borrador de HEA con lo documentado", self.generate_hea, "Accent.TButton")],
            pady=(0, 8))
        btns.pack(anchor="w")
        self.hea_pending = ttk.Label(s2, text="", style="Warn.TLabel", wraplength=900,
                                     justify="left")
        self.hea_pending.pack(anchor="w", pady=(0, 6))
        ttk.Label(s2, text="Historia de la Enfermedad Actual (texto final)",
                  style="Field.TLabel").pack(anchor="w")
        self.w["hea_texto"] = widgets.TextBox(s2, height=7, max_height=20)
        self.w["hea_texto"].pack(fill="x", pady=(2, 8))
        self.w["hea_revisada"] = widgets.CheckField(
            s2, text="HEA revisada y confirmada por el personal médico")
        self.w["hea_revisada"].pack(anchor="w")
        ttk.Label(s2, text="Un borrador generado por plantilla debe marcarse como revisado "
                  "antes de finalizar la ficha.", style="Hint.TLabel").pack(anchor="w")

    # -- 3. signos vitales + examen físico (+ pruebas en SSR)
    def _build_tab_clinica(self):
        t = self._tab("3. Signos y examen" if self.kind == "aps"
                      else "3. Evaluación")
        s = widgets.section(t, "Signos vitales")
        g = widgets.FormGrid(s, 6)
        g.full(ttk.Label(s, text="PAS/PAD: presión arterial sistólica/diastólica · FC: frecuencia "
                         "cardíaca · FR: frecuencia respiratoria. Deje vacío lo que no se midió.",
                         style="Hint.TLabel", wraplength=900, justify="left"), pady=(0, 0))
        self.vital_w = {}
        for key, (label, unit, *_r) in VITALS.items():
            e = widgets.EntryField(s, width=9)
            e.bind("<KeyRelease>", lambda ev: self._live_vitals())
            self.vital_w[key] = e
            m = re.search(r"\((\w+)\)", label)
            short = m.group(1) if m else label
            self._reg(g, key, f"{short} ({unit})", e)
        g.newline()
        self._reg(g, "vitales_nota", "Nota o justificación de valores extremos (opcional)",
                  widgets.EntryField(s), span=6)
        self.vital_msg = ttk.Label(s, text="", style="Warn.TLabel", wraplength=900, justify="left")
        g.full(self.vital_msg)

        box = widgets.section(t, "Examen físico" + (" en orden cefalocaudal" if self.kind == "aps"
                                                    else ""))
        ttk.Label(box, text="Nada se marca como normal automáticamente: elija 'Sin hallazgos "
                  "patológicos identificados' solo si la región fue evaluada y el hallazgo está "
                  "confirmado.", style="Hint.TLabel", wraplength=900, justify="left").pack(anchor="w")
        grid = ttk.Frame(box)
        grid.pack(fill="x", pady=(6, 0))
        grid.columnconfigure(2, weight=1)
        r = 0
        for region, label in visit_svc.REGIONS[self.kind]:
            self._exam_row(grid, r, region, label, False)
            r += 1
            if region == "abdomen":
                b = ttk.Button(grid, text="Documentar: exploración abdominal limitada "
                               "(sin camilla ni espacio adecuado)",
                               command=self._abdomen_limited)
                b.grid(row=r, column=1, columnspan=2, sticky="w", pady=(0, 4))
                r += 1
                for sub, sublabel in visit_svc.ABDOMEN_SUB:
                    self._exam_row(grid, r, sub, sublabel, True)
                    r += 1
        if self.kind == "ssr":
            pb = widgets.section(t, "Pruebas realizadas y resultados")
            ttk.Label(pb, text="No se asume ninguna prueba: registre solo las realizadas, o indique "
                      "expresamente las que no se hicieron y por qué.", style="Hint.TLabel",
                      wraplength=900, justify="left").pack(anchor="w", pady=(0, 6))
            self.tests = widgets.RowList(pb, lambda p, rm: TestRow(p, rm), "+ Agregar prueba")
            self.tests.pack(fill="x")

    def _exam_row(self, grid, r, region, label, indent):
        lbl = ttk.Label(grid, text=("      " if indent else "") + label, wraplength=250,
                        justify="left")
        lbl.grid(row=r, column=0, sticky="nw", padx=(0, 10), pady=(8, 2))
        combo = widgets.ComboField(grid, visit_svc.EXAM_ESTADOS, width=30)
        combo.set_value(visit_svc.EXAM_PENDIENTE)
        combo.grid(row=r, column=1, sticky="nw", padx=(0, 10), pady=(4, 2))
        tb = widgets.TextBox(grid, height=1 if indent else 2, max_height=10)
        tb.grid(row=r, column=2, sticky="ew", pady=(4, 2))
        self.exam_w[region] = (combo, tb)

    def _abdomen_limited(self):
        combo, tb = self.exam_w["abdomen"]
        current = tb.get_value().strip()
        if current and current != visit_svc.ABDOMEN_LIMITADO and not dialogs.confirm(
                self, "Reemplazar texto",
                "El campo de abdomen ya tiene texto. ¿Reemplazarlo por la nota de exploración "
                "limitada?", yes="Reemplazar", no="Conservar"):
            return
        combo.set_value(visit_svc.EXAM_LIMITADO)
        tb.set_value(visit_svc.ABDOMEN_LIMITADO)

    # -- 4. diagnósticos
    def _build_tab_dx(self):
        t = self._tab("4. Diagnósticos")
        s = widgets.section(t, "Diagnóstico principal")
        ttk.Label(s, text="Registre el código CIE-11 solo cuando lo haya verificado. Si un "
                  "diagnóstico manuscrito no se lee con claridad, deje el texto como está y no "
                  "marque el código como verificado.", style="Hint.TLabel", wraplength=900,
                  justify="left").pack(anchor="w", pady=(0, 4))
        self.dx_main = DxRow(s, None, title=None)
        self.dx_main.frame.pack(fill="x")
        s2 = widgets.section(t, "Diagnósticos secundarios")
        self.dx_list = widgets.RowList(s2, lambda p, rm: DxRow(p, rm), "+ Agregar diagnóstico secundario")
        self.dx_list.pack(fill="x")

    # -- 5. plan terapéutico
    def _build_tab_plan(self):
        t = self._tab("5. Plan terapéutico" if self.kind == "aps" else "5. Plan y consejería")
        s = widgets.section(t, "Medicamentos prescritos y entregados")
        ttk.Label(s, text="El sistema no calcula dosis ni cantidades: las introduce y valida el "
                  "personal médico. Anote por separado lo prescrito y lo realmente entregado.",
                  style="Hint.TLabel", wraplength=900, justify="left").pack(anchor="w", pady=(0, 6))
        self.meds_ctx = {"meds": [], "vias": [], "units": []}
        self.meds = widgets.RowList(s, lambda p, rm: MedRow(p, rm, self.meds_ctx),
                                    "+ Agregar medicamento")
        self.meds.pack(fill="x")

        if self.kind == "ssr":
            self._build_ssr_plan(t)
        else:
            c = widgets.section(t, "Consejería y signos de alarma")
            g = widgets.FormGrid(c, 3)
            g.full(ttk.Label(c, text="Las sugerencias son para revisión médica. Marque la consejería "
                             "como 'Realizada' solo si efectivamente se brindó.", style="Hint.TLabel",
                             wraplength=900, justify="left"), pady=(0, 0))
            self._reg(g, "consejeria_alarma", "Signos de alarma explicados al paciente",
                      widgets.TextBox(c, height=3), span=2)
            self._reg(g, "consejeria_estado", "Estado de la consejería",
                      widgets.ComboField(c, visit_svc.CONSEJERIA_ESTADOS))
            g.full(widgets.button_row(c, [("Sugerir signos de alarma (para revisión)",
                                           self.suggest_alarm)]))
        r = widgets.section(t, "Recomendaciones y seguimiento")
        g = widgets.FormGrid(r, 2)
        self._reg(g, "recomendaciones", "Recomendaciones generales", widgets.TextBox(r, height=2))
        if self.kind == "aps":
            self._reg(g, "medidas_no_farm", "Medidas no farmacológicas", widgets.TextBox(r, height=2))
        self._reg(g, "seguimiento", "Seguimiento", widgets.TextBox(r, height=2))
        self._reg(g, "fecha_control", "Fecha sugerida de control", widgets.DateEntry(r))
        self._reg(g, "referencia", "Referencia a otro establecimiento (si corresponde)",
                  widgets.TextBox(r, height=2), span=2)

    def _build_ssr_plan(self, t):
        m = widgets.section(t, "Método anticonceptivo entregado o administrado")
        g = widgets.FormGrid(m, 3)
        self._reg(g, "metodo_entregado", "Método", widgets.EntryField(m))
        self._reg(g, "metodo_presentacion", "Presentación", widgets.EntryField(m))
        self._reg(g, "metodo_cantidad", "Cantidad", widgets.EntryField(m, width=10))
        self._reg(g, "metodo_unidad", "Unidad", widgets.ComboField(m, [], readonly=False))
        self._reg(g, "fecha_administracion", "Fecha de administración",
                  widgets.DateEntry(m, show_today=True))
        self._reg(g, "fecha_proxima_dosis", "Fecha prevista de la próxima dosis",
                  widgets.DateEntry(m))
        i = widgets.section(t, "Intervenciones y consejería")
        ttk.Label(i, text="Cada intervención queda 'Pendiente' hasta que confirme que se realizó. "
                  "No se registran entregas ni administraciones sin confirmar.", style="Hint.TLabel",
                  wraplength=900, justify="left").pack(anchor="w", pady=(0, 6))
        grid = ttk.Frame(i)
        grid.pack(fill="x")
        grid.columnconfigure(2, weight=1)
        for r, tipo in enumerate(visit_svc.SSR_INTERVENCIONES):
            ttk.Label(grid, text=tipo).grid(row=r, column=0, sticky="w", padx=(0, 12), pady=4)
            combo = widgets.ComboField(grid, visit_svc.INTERVENCION_ESTADOS, width=16)
            combo.set_value("Pendiente")
            combo.grid(row=r, column=1, sticky="w", padx=(0, 10), pady=4)
            note = widgets.EntryField(grid)
            note.grid(row=r, column=2, sticky="ew", pady=4)
            self.inter_w[tipo] = (combo, note)
        a = widgets.section(t, "Signos de alarma")
        g2 = widgets.FormGrid(a, 1)
        self._reg(g2, "signos_alarma", "Signos de alarma explicados al paciente",
                  widgets.TextBox(a, height=3))
        g2.full(widgets.button_row(a, [("Sugerir signos de alarma (para revisión)",
                                        self.suggest_alarm)]))

    # ------------------------------------------------------------------ carga
    def on_show(self, patient_id=None, visit_id=None, **kw):
        pid = patient_id or self.app.active_pid
        if not pid:
            self._show_picker()
            return
        self._fill_lists()
        self._set_patient(pid)
        self._refresh_visit_choices()
        if visit_id:
            self._load_visit(visit_id)
        else:
            self._load_new()
        self._poll()

    def refresh(self):
        self._fill_lists()
        if self.pid:
            self._refresh_visit_choices()

    def _show_picker(self):
        self.pid = self.vid = self.patient = None
        self.form_box.pack_forget()
        self.picker_box.pack(fill="both", expand=True)
        self.badge.configure(text="")
        self.dirty_lbl.configure(text="")
        self._clean = None
        self.picker.start()

    def _fill_lists(self):
        db = self.db
        self.w["personal"].set_values(db.catalog("personal"))
        labels, self.by_label, self.by_id = common.brigade_options(db)
        self.w["brigade"].set_values(labels)
        self.w["lugar"].set_values(common.known_values(db, f"{self.kind}_visits", "lugar"))
        self.meds_ctx["meds"] = common.known_meds(db)
        self.meds_ctx["vias"] = db.catalog("via_administracion")
        self.meds_ctx["units"] = db.catalog("unidad_cantidad")
        if self.kind == "ssr":
            self.w["categoria"].set_values(db.catalog("categoria_ssr"))
            self.w["metodo_unidad"].set_values(db.catalog("unidad_cantidad"))

    def _set_patient(self, pid):
        self.patient = patient_svc.get_patient(self.db, pid)
        self.pid = pid
        self.app.set_active(pid)
        p = self.patient
        self.pt_lbl.configure(
            text=f"{patient_svc.display_name(p)}   ·   {p['codigo']}   ·   "
                 f"{patient_svc.age_text(p) or 'edad no registrada'}   ·   "
                 f"{p['sexo'] or 'sexo no registrado'}")
        self.pt_info.configure(
            text=f"{patient_svc.procedencia(p) or 'procedencia no registrada'}   ·   "
                 f"Ficha Integral creada el {fmt_date(p['fecha_creacion'])}")
        self.picker_box.pack_forget()
        self.form_box.pack(fill="both", expand=True)

    def _refresh_visit_choices(self):
        rows = visit_svc.list_all_visits(self.db, patient_id=self.pid, kind=self.kind)
        self._visit_map = {NEW_LABEL: None}
        for v in rows:
            label = (f"{fmt_date(v['fecha_atencion'])}  ·  "
                     f"{'Borrador' if v['estado'] == 'borrador' else 'Finalizada'}  ·  "
                     f"{v['dx'] or 'sin diagnóstico'}  (#{v['id']})")
            self._visit_map[label] = v["id"]
        self.visit_combo.set_values(list(self._visit_map))

    def _sync_visit_combo(self):
        label = next((k for k, v in self._visit_map.items() if v == self.vid), NEW_LABEL)
        self.visit_combo.set_value(label)
        self._prev_choice = label

    def _on_pick_visit(self, _event=None):
        label = self.visit_combo.get_value()
        vid = self._visit_map.get(label)
        if not self.can_leave():
            self.visit_combo.set_value(self._prev_choice)
            return
        self._mark_clean()
        if vid is None:
            self._load_new()
        else:
            self._load_visit(vid)

    def _new_clicked(self):
        if not self.can_leave():
            return
        self._mark_clean()
        self._load_new()

    def _reset_form(self):
        for k, w in self.w.items():
            if k == "brigade":
                continue
            w.set_value("")
        for combo, tb in self.exam_w.values():
            combo.set_value(visit_svc.EXAM_PENDIENTE)
            tb.set_value("")
        self.dx_main.set({})
        self.dx_list.clear()
        self.meds.clear()
        if self.kind == "ssr":
            self.tests.clear()
            for combo, note in self.inter_w.values():
                combo.set_value("Pendiente")
                note.set_value("")
        self.hea_origen = "manual"
        self.hea_pending.configure(text="")
        self.same_manual.set_value(False)

    def _load_new(self):
        self.vid = None
        self.estado = "nuevo"
        self._reset_form()
        self.w["fecha_atencion"].set_value(date.today().isoformat())
        self.w["personal"].set_value(self.db.get_setting("ultimo_personal", ""))
        bid = self.app.current_brigade_id()
        self.w["brigade"].set_value(self.by_id.get(bid, common.NO_BRIGADE))
        if bid:
            from services import brigades as brigade_svc
            b = brigade_svc.get_brigade(self.db, bid)
            self.w["lugar"].set_value(b.get("lugar") or b.get("localidad") or "")
        if self.kind == "aps":
            self.w["historia_clinica"].set_value(self.patient.get("historia_clinica") or "")
            self.w["consejeria_estado"].set_value("Pendiente")
        self._update_same_day()
        self._live_vitals()
        self._sync_visit_combo()
        self.status.configure(text="")
        self._apply_state()
        self._mark_clean()
        self.nb.select(0)
        self.w["fecha_atencion"].focus_field()

    def _load_visit(self, vid):
        v = visit_svc.get_visit(self.db, self.kind, vid)
        if not v or v["main"]["patient_id"] != self.pid:
            self._load_new()
            return
        m = v["main"]
        self.vid = vid
        self.estado = m["estado"]
        self._reset_form()
        for k, w in self.w.items():
            if k == "brigade":
                continue
            val = m.get(k)
            if k in NUM_KEYS:
                val = fmt_number(val) if val is not None else ""
            w.set_value("" if val is None else val)
        self.w["hea_revisada"].set_value(bool(m.get("hea_revisada")))
        self.w["brigade"].set_value(self.by_id.get(m["brigade_id"], common.NO_BRIGADE))
        self.hea_origen = m.get("hea_origen") or "manual"
        same_key = "mismo_dia_ficha" if self.kind == "aps" else "mismo_dia_aps"
        self.same_combo.set_value(m.get(same_key))
        self.same_manual.set_value(bool(m.get("mismo_dia_manual")))
        for region, e in v["exam"].items():
            if region in self.exam_w:
                self.exam_w[region][0].set_value(e["estado"])
                self.exam_w[region][1].set_value(e["hallazgos"])
        principal = [d for d in v["dx"] if d["tipo"] == "principal"]
        self.dx_main.set(principal[0] if principal else {})
        self.dx_list.set_all([d for d in v["dx"] if d["tipo"] != "principal"])
        self.meds.set_all(v["meds"])
        if self.kind == "ssr":
            self.tests.set_all(v["tests"])
            for tipo, (combo, note) in self.inter_w.items():
                e = v["interventions"].get(tipo, {})
                combo.set_value(e.get("estado", "Pendiente"))
                note.set_value(e.get("nota", ""))
        self._update_same_day()
        self._live_vitals()
        self._sync_visit_combo()
        self._apply_state()
        self._mark_clean()

    # ------------------------------------------------------------------ estado / bloqueo
    def _apply_state(self):
        final = self.estado == "finalizada"
        self.locked = final
        widgets.set_locked(self.nb, final)
        if self.estado == "nuevo":
            self.badge.configure(text="NUEVA – sin guardar", style="Draft.TLabel")
        elif self.estado == "borrador":
            self.badge.configure(text="BORRADOR – ficha incompleta", style="Draft.TLabel")
        else:
            self.badge.configure(text="FINALIZADA – guardada", style="Final.TLabel")
        self._update_same_day()
        self._buttons()

    def _buttons(self):
        for b in (self.btn_final, self.btn_draft, self.btn_edit):
            b.pack_forget()
        saved = self.vid is not None
        if self.locked:
            self.btn_edit.pack(side="right")
        else:
            if self.estado == "finalizada":
                self.btn_final.configure(text="Guardar cambios")
                self.btn_final.pack(side="right")
            else:
                self.btn_final.configure(text="Finalizar ficha")
                self.btn_final.pack(side="right")
                self.btn_draft.pack(side="right", padx=8)
        for b in (self.btn_pdf, self.btn_print, self.btn_log):
            b.state(["!disabled"] if saved else ["disabled"])
        self.btn_delete.state(["!disabled"] if self.estado == "borrador" else ["disabled"])
        self.btn_cancel.state(["disabled"] if self.locked else ["!disabled"])

    def unlock(self):
        if not dialogs.confirm(
                self, "Editar ficha finalizada",
                "Esta ficha ya está finalizada. Si la edita, cada cambio quedará anotado en el "
                "historial de modificaciones. ¿Desea editarla?", yes="Editar", no="Cancelar"):
            return
        self.locked = False
        widgets.set_locked(self.nb, False)
        self._update_same_day()
        self._buttons()

    # ------------------------------------------------------------------ "mismo día"
    def _fecha_iso(self):
        try:
            return parse_date(self.w["fecha_atencion"].get_value())
        except ValidationError:
            return None

    def _update_same_day(self):
        if not self.pid:
            return
        manual = self.same_manual.get_value()
        iso = self._fecha_iso()
        if not manual:
            self.same_combo.set_value(
                visit_svc.suggest_same_day(self.db, self.kind, self.pid, iso, self.patient))
        self.same_combo.state(["!disabled"] if (manual and not self.locked) else ["disabled"])
        value = self.same_combo.get_value()
        creation = fmt_date(self.patient["fecha_creacion"])
        if self.kind == "aps":
            text = (f"La atención se brindó el mismo día en que se creó la Ficha Integral ({creation})."
                    if value == "Sí" else
                    f"La atención ocurrió en otra fecha: la Ficha Integral se creó el {creation}. "
                    "Puede guardarla igualmente.")
        else:
            text = {"Sí": "Hay una atención APS de este paciente en la misma fecha.",
                    "No": "La atención APS de este paciente se registró en otra fecha.",
                    }.get(value, "Este paciente no tiene atención APS registrada.")
        if not manual:
            text += "  (calculado automáticamente)"
        self.same_info.configure(text=text)

    # ------------------------------------------------------------------ signos vitales
    def _live_vitals(self):
        raw = {k: w.get_value() for k, w in self.vital_w.items()}
        _vals, errors, warnings = check_vitals(raw)
        for k, w in self.vital_w.items():
            _v, err, _w = check_vitals({k: raw[k]})
            w.configure(style="Bad.TEntry" if err else "TEntry")
        if errors:
            self.vital_msg.configure(text="\n".join(errors), style="Error.TLabel")
        elif warnings:
            self.vital_msg.configure(text="\n".join(warnings), style="Warn.TLabel")
        else:
            self.vital_msg.configure(text="")

    # ------------------------------------------------------------------ asistentes locales
    def _dx_text(self):
        parts = [self.dx_main.get().get("descripcion", "")]
        if self.kind == "ssr":
            parts += [self.w["categoria"].get_value(), self.w["motivo"].get_value()]
        else:
            parts.append(self.w["hea_motivo"].get_value())
        return " ".join(p for p in parts if p)

    def suggest_questions(self):
        title, qs = clinical.suggest_questions(self.kind, self._dx_text())
        dialogs.read_only_list(
            self, "Preguntas sugeridas",
            f"Orientación para: {title}.\nSon sugerencias para el interrogatorio; NO son datos "
            "del paciente y no se guardan en la ficha.", qs)

    def generate_hea(self):
        current = self.w["hea_texto"].get_value().strip()
        if current and not dialogs.confirm(
                self, "Reemplazar HEA", "Ya hay un texto en la HEA. ¿Reemplazarlo por un nuevo "
                "borrador generado con los datos documentados?", yes="Reemplazar", no="Conservar"):
            return
        dx = self.dx_main.get().get("descripcion", "")
        if self.kind == "aps":
            fields = {k: self.w[k].get_value() for k, _l, _c in clinical.APS_HEA_FIELDS}
            text, pending = clinical.build_hea_aps(self.patient, fields, dx)
        else:
            fields = {}
            for k, _l in clinical.SSR_HEA_FIELDS:
                val = self.w[k].get_value()
                if k in ("fum", "hea_fecha_ultima_dosis"):
                    try:
                        val = parse_date(val) or ""
                    except ValidationError:
                        pass
                fields[k] = val
            text, pending = clinical.build_hea_ssr(
                self.patient, fields, self.w["motivo"].get_value(),
                self.w["categoria"].get_value(), dx)
        self.w["hea_texto"].set_value(text)
        self.w["hea_revisada"].set_value(False)
        self.hea_origen = "plantilla"
        self.hea_pending.configure(
            text=("Datos pendientes de documentar: " + "; ".join(pending)) if pending else "")
        dialogs.info(self, "Se generó un BORRADOR PRELIMINAR con lo que usted documentó. Revíselo y "
                     "corríjalo; luego marque 'HEA revisada y confirmada' para poder finalizar.",
                     title="Borrador de HEA")

    def suggest_alarm(self):
        signs = clinical.suggest_alarm_signs(self.kind, self._dx_text())
        picked = dialogs.suggestions(
            self, "Signos de alarma sugeridos",
            "Marque los que correspondan. Son sugerencias para revisión médica; insertarlos no "
            "significa que la consejería se haya brindado.", signs, "Insertar seleccionados",
            preselect=True)
        if picked:
            key = "consejeria_alarma" if self.kind == "aps" else "signos_alarma"
            self.w[key].append_value("\n".join(f"- {s}" for s in picked))

    # ------------------------------------------------------------------ recolección
    def collect(self):
        main = {}
        for k, w in self.w.items():
            if k != "brigade":
                main[k] = w.get_value()
        main["brigade_id"] = self.by_label.get(self.w["brigade"].get_value())
        same_key = "mismo_dia_ficha" if self.kind == "aps" else "mismo_dia_aps"
        main[same_key] = self.same_combo.get_value()
        main["mismo_dia_manual"] = 1 if self.same_manual.get_value() else 0
        main["hea_origen"] = self.hea_origen
        main["hea_revisada"] = 1 if self.w["hea_revisada"].get_value() else 0
        exam = {r: {"estado": c.get_value(), "hallazgos": t.get_value()}
                for r, (c, t) in self.exam_w.items()}
        dx = []
        principal = self.dx_main.get()
        principal["tipo"] = "principal"
        dx.append(principal)
        for d in self.dx_list.get_all():
            d["tipo"] = "secundario"
            dx.append(d)
        raw = {"main": main, "exam": exam, "dx": dx, "meds": self.meds.get_all()}
        if self.kind == "ssr":
            raw["tests"] = self.tests.get_all()
            raw["interventions"] = {t: {"estado": c.get_value(), "nota": n.get_value()}
                                    for t, (c, n) in self.inter_w.items()}
        return raw

    def _mark_clean(self):
        self._clean = json.dumps(self.collect(), sort_keys=True, default=str)
        self.dirty_lbl.configure(text="")

    def is_dirty(self):
        if self._clean is None or not self.form_box.winfo_ismapped():
            return False
        return json.dumps(self.collect(), sort_keys=True, default=str) != self._clean

    def _poll(self):
        if not self.winfo_exists() or not self.winfo_ismapped():
            return
        if self.form_box.winfo_ismapped():
            self.dirty_lbl.configure(
                text="●  Cambios sin guardar" if (not self.locked and self.is_dirty()) else "")
        self.after(600, self._poll)

    def can_leave(self):
        if self.locked or not self.pid or not self.is_dirty():
            return True
        save_text = "Guardar cambios" if self.estado == "finalizada" else "Guardar borrador"
        choice = dialogs.unsaved_changes(self, save_text)
        if choice == "cancel":
            return False
        if choice == "save":
            return self.save(self.estado == "finalizada")
        self._mark_clean()
        return True

    def on_save_shortcut(self):
        if self.pid and not self.locked and self.form_box.winfo_ismapped():
            self.save(self.estado == "finalizada")

    # ------------------------------------------------------------------ acciones
    def cancel(self):
        if self.locked:
            return
        if self.is_dirty() and not dialogs.confirm(
                self, "Cancelar cambios", "Se perderán los datos escritos que no haya guardado.",
                yes="Descartar cambios", no="Seguir editando", danger=True):
            return
        self._mark_clean()
        if self.vid:
            self._load_visit(self.vid)
        else:
            self._load_new()

    def save(self, finalize):
        raw = self.collect()
        data, errors, warnings = visit_svc.prepare_visit(self.kind, raw, finalizing=finalize)
        if errors:
            dialogs.show_errors(self, errors)
            return False
        if finalize and warnings and not dialogs.confirm_warnings(
                self, warnings, "Finalizar de todos modos", title="Antes de finalizar la ficha"):
            return False
        main = data["main"]
        db = self.db
        was_new = self.vid is None
        vid = visit_svc.save_visit(db, self.kind, self.pid, data, self.vid)
        # catálogos configurables: lo nuevo que se escribió queda disponible
        if main.get("personal"):
            db.add_catalog("personal", main["personal"])
            db.set_setting("ultimo_personal", main["personal"])
        if self.kind == "ssr" and main.get("categoria"):
            db.add_catalog("categoria_ssr", main["categoria"])
        for m in data["meds"]:
            if m.get("via"):
                db.add_catalog("via_administracion", m["via"])
            if m.get("unidad"):
                db.add_catalog("unidad_cantidad", m["unidad"])
        self._fill_lists()
        self._refresh_visit_choices()
        self._load_visit(vid)
        stamp = common.now_hhmm()
        if finalize:
            self.status.configure(text=f"Ficha finalizada y guardada a las {stamp}")
        else:
            n = len(warnings)
            self.status.configure(text=f"Borrador guardado a las {stamp}"
                                  + (f"  ({n} advertencia(s))" if n else ""))
        self.app.refresh_brigade_label()
        self.app._update_strip()
        return True

    def delete_draft(self):
        if self.vid is None or self.estado != "borrador":
            return
        if not dialogs.confirm(self, "Eliminar borrador",
                               "Se eliminará este borrador. Las fichas finalizadas nunca se borran. "
                               "¿Continuar?", yes="Eliminar borrador", no="Cancelar", danger=True):
            return
        visit_svc.delete_draft(self.db, self.kind, self.vid)
        self._refresh_visit_choices()
        self._mark_clean()
        self._load_new()
        self.status.configure(text="Borrador eliminado")
        self.app._update_strip()

    def show_log(self):
        if self.vid:
            dialogs.audit_log(self, f"Historial de modificaciones – {self.short} #{self.vid}",
                              visit_svc.visit_audit(self.db, self.kind, self.vid))

    # ------------------------------------------------------------------ PDF
    def _ensure_saved(self):
        if self.vid is None:
            dialogs.info(self, "Guarde primero la ficha (como borrador o finalizada) para poder "
                         "exportarla o imprimirla.")
            return False
        if not self.locked and self.is_dirty():
            choice = dialogs.choose(
                self, "Cambios sin guardar",
                "El PDF refleja lo que está guardado. ¿Guardar los cambios antes?",
                [("cancel", "Cancelar", "normal"), ("save", "Guardar y continuar", "accent")],
                default="save", cancel="cancel")
            if choice != "save" or not self.save(self.estado == "finalizada"):
                return False
        return True

    def _build_pdf(self, path):
        fn = pdf.aps_pdf if self.kind == "aps" else pdf.ssr_pdf
        fn(self.db, self.vid, path)

    def export_pdf(self):
        if not self._ensure_saved():
            return
        fecha = (self._fecha_iso() or "").replace("-", "")
        path = dialogs.ask_save_path(
            self, f"Guardar ficha {self.short} en PDF",
            initialfile=f"{self.short}_{self.patient['codigo']}_{fecha}.pdf")
        if not path:
            return
        try:
            self._build_pdf(path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo generar el PDF:\n{exc}")
            return
        if dialogs.confirm(self, "PDF generado", f"Se guardó:\n{path}", yes="Abrir PDF", no="Cerrar"):
            widgets.open_path(path)

    def print_pdf(self):
        if not self._ensure_saved():
            return
        path = config.exports_dir() / f"imprimir_{self.short}_{self.patient['codigo']}_{self.vid}.pdf"
        try:
            self._build_pdf(path)
            widgets.open_path(path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo preparar la impresión:\n{exc}")
