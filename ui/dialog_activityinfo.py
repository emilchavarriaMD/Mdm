"""Ventana de revisión antes de llenar ActivityInfo: la persona confirma o corrige cada dato."""
import random
import tkinter as tk
from tkinter import ttk

from services import activityinfo as ai
from services import cie11_catalog as cat
from services import cie11_ssr as ssr_cat
from services import hea_banco
from services import examen_fisico
from ui import dialogs, widgets
from ui.dialogs import _Modal


class ChecksField(ttk.Frame):
    """Varias opciones marcables a la vez (por ejemplo, las consultas a realizar)."""

    def __init__(self, parent, options, columns=2, command=None):
        super().__init__(parent)
        self.vars = {}
        self.command = command
        for i, opt in enumerate(options):
            v = tk.BooleanVar(value=False)
            self.vars[opt] = v
            ttk.Checkbutton(self, text=opt, variable=v, command=lambda: self.command and self.command()).grid(row=i // columns, column=i % columns,
                                                             sticky="w", padx=(0, 18), pady=1)

    def set_value(self, values):
        for opt, v in self.vars.items():
            v.set(opt in (values or []))

    def get_value(self):
        return [opt for opt, v in self.vars.items() if v.get()]


class ActivityInfoDialog(_Modal):
    def __init__(self, parent, defaults: dict, title="Añadir registro en ActivityInfo", db=None):
        super().__init__(parent, title)
        self.db = db
        self.defaults = defaults
        self.w = {}
        self.transient("")                 # sin «transient», Windows muestra los botones de maximizar/minimizar
        self.resizable(True, True)
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = min(900, sw - 40), min(700, sh - 90)
        self.geometry(f"{w}x{h}+{max(0, (sw - w) // 2)}+{max(0, (sh - h) // 3)}")
        self.minsize(640, 420)
        bar = ttk.Frame(self, padding=(18, 8, 18, 12))
        bar.pack(side="bottom", fill="x")          # botones siempre visibles
        sf = widgets.ScrollFrame(self)
        sf.pack(fill="both", expand=True)
        body = ttk.Frame(sf.body, padding=(18, 14, 18, 8))
        body.pack(fill="both", expand=True)

        def _wheel(e):
            sf.canvas.yview_scroll(-1 if (e.delta > 0 or getattr(e, "num", 0) == 4) else 1, "units")
            return "break"
        self.bind("<MouseWheel>", _wheel)
        self.bind("<Button-4>", _wheel)
        self.bind("<Button-5>", _wheel)
        ttk.Label(body, text="Revise los datos antes de llenar el formulario", style="H2.TLabel").pack(
            anchor="w")
        ttk.Label(body, text="Solo se llena el formulario: el programa NO guarda la ficha. Usted la crea "
                  "en ActivityInfo cuando termine de revisar.\nLo que deje vacío no se toca. Los datos que "
                  "el ATA no trae (estado civil, escolaridad…) los elige usted.",
                  style="Muted.TLabel", justify="left", wraplength=760).pack(anchor="w", pady=(2, 8))
        gf = ttk.Frame(body)
        gf.pack(fill="x")
        g = widgets.FormGrid(gf, 3)

        def add(key, label, w, span=1):
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            g.add(label, w, span=span)

        E = lambda: widgets.EntryField(gf, width=26)  # noqa: E731
        C = lambda vals, ro=True: widgets.ComboField(gf, [""] + list(vals), readonly=ro, width=26)  # noqa: E731
        add("lugar", "Lugar de atención (si es «…-Otro», escriba abajo cuál)", E())
        add("punto_especifico", "Especifique punto de atención (solo si el lugar es «Otro»)", E())
        add("donante", "Proyecto: Donante Nombre", E())
        add("proyecto", "Proyecto: Título del proyecto", E())
        add("perfin", "Proyecto: PERFIN", E())
        add("nombres", "Nombres", E())
        add("apellidos", "Apellidos", E())
        add("genero", "Género", C(ai.GENEROS))
        add("fecha", "Fecha de consulta (AAAA-MM-DD)", E())
        add("lgtbiq", "¿Se identifica como persona LGTBIQ+?", C(ai.LGTBIQ))
        add("pueblo", "¿Con qué pueblo se identifica la persona atendida?", C(ai.PUEBLOS))
        add("edad", "Años (manual) — no se usa fecha de nacimiento", E())
        add("estado_civil", "Estado civil", C(ai.ESTADOS_CIVILES))
        add("escolaridad", "Grado de escolaridad", C(ai.ESCOLARIDADES))
        add("ocupacion", "Sector de ocupación", C(ai.OCUPACIONES))
        add("discapacidad", "¿Tiene alguna discapacidad?", C(ai.DISCAPACIDAD))
        add("perfil", "Perfil de población", C(ai.PERFILES))
        add("derivado", "¿Ha sido derivado/a?", C(ai.DERIVADO))
        add("nacionalidad", "País de nacionalidad", E())
        add("idioma", "Idioma", E())
        add("consultas", "Consulta a realizar (puede marcar más de una)",
            ChecksField(gf, ai.CONSULTAS, command=lambda: self._mostrar_ssr()), span=3)
        add("profesional", "Profesional que atiende (APS)", E())
        add("tipo_consulta", "Tipo de consulta (APS)", C(ai.TIPOS_CONSULTA))
        # Orden de la página de ActivityInfo (subformulario APS): HEA, signos vitales y peso, examen físico, diagnósticos
        f_hea = ttk.Frame(body)
        f_hea.pack(fill="x")
        f_vit = ttk.Frame(body)
        f_vit.pack(fill="x")
        f_exa = ttk.Frame(body)
        f_exa.pack(fill="x")
        f_dx = ttk.Frame(body)
        f_dx.pack(fill="x")
        f_plan = ttk.Frame(body)
        f_plan.pack(fill="x")
        f_der = ttk.Frame(body)
        f_der.pack(fill="x")
        self.f_ssr = ttk.Frame(body)           # al final de todo; solo se ve si se marca Salud Sexual y Reproductiva
        ttk.Label(f_vit, text="Signos vitales y peso (frecuencia respiratoria: en niños, elíjala; vacío = no se llena)", style="H2.TLabel").pack(anchor="w", pady=(12, 2))
        gf2 = ttk.Frame(f_vit)
        gf2.pack(fill="x")
        g2 = widgets.FormGrid(gf2, 3)

        def add2(key, label, w, span=1):
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            g2.add(label, w, span=span)

        V = lambda vals: widgets.ComboField(gf2, [""] + list(vals), readonly=False, width=26)  # noqa: E731
        add2("sistolica", "Sistólica (mayor) mmHg", V(ai.LISTA_SISTOLICA))
        add2("diastolica", "Diastólica (menor) mmHg", V(ai.LISTA_DIASTOLICA))
        add2("fc", "Pulso (latidos/min)", V(ai.LISTA_FC))
        add2("fr", "Frec. respiratoria (por min)", V(ai.LISTA_FR))
        add2("temperatura", "Temperatura (ºC)", V(ai.LISTA_TEMP))
        add2("peso", "Peso (kg) — escríbalo", widgets.EntryField(gf2, width=26))
        self._vit_auto = {k: self.w[k].get_value() for k in ("sistolica", "diastolica", "fc", "fr")}
        _p0 = defaults.get("hea_persona") or {}
        self._vit_grupo = ai.grupo_vitales(_p0.get("sexo"), _p0.get("edad"), _p0.get("unidad", "años"))

        dxs = defaults.get("dx") or []
        ttk.Label(f_dx, text="Diagnósticos — lista de ActivityInfo (descripción y código)",
                  style="H2.TLabel").pack(anchor="w", pady=(10, 2))
        self.dx_rows = []
        self.dx_tags = []
        labels = [cat.label(d) for d in cat.descriptions()]
        self._labels = labels
        if dxs:
            for i, d in enumerate(dxs):
                row = ttk.Frame(f_dx)
                row.pack(fill="x", pady=2)
                ttk.Label(row, text=f"{i + 1}. {d['abrev']}", width=22).pack(side="left")
                cb = widgets.ComboField(row, labels, readonly=False, width=78)
                desc, code = cat.from_label(d.get("descripcion", ""))
                if not desc:
                    desc, code = hea_banco.sugerir_lista(d.get("abrev", ""))
                cb.set_value(cat.label(desc) if desc else "")
                cb.pack(side="left", fill="x", expand=True)
                cb.bind("<<ComboboxSelected>>", lambda e: self._regen_hea(True))
                cb.bind("<FocusOut>", lambda e: self._regen_hea(True))
                cb.bind("<KeyRelease>", lambda e, c=cb: self._filtrar(c, e))
                tag = ttk.Label(f_dx, text="", style="Muted.TLabel")
                tag.pack(anchor="w", padx=(170, 0))
                self.dx_tags.append(tag)
                self.dx_rows.append((d["abrev"], cb))
            ttk.Label(f_dx, text="Elija en la lista de ActivityInfo (puede escribir para buscar). Al elegir la "
                      "descripción, ActivityInfo pone el código solo. Si uno no está en la lista, déjelo vacío: no se llena en "
                      "ActivityInfo, pero la HEA sí lo incluye (vea «HEA usa» debajo de cada uno).",
                      style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
            self.recordar = tk.BooleanVar(value=True)
            ttk.Checkbutton(f_dx, text="Recordar estas equivalencias para los próximos pacientes",
                            variable=self.recordar).pack(anchor="w")
        else:
            self.recordar = tk.BooleanVar(value=False)
            ttk.Label(f_dx, text="El ATA no trae diagnósticos para este paciente.",
                      style="Muted.TLabel").pack(anchor="w")
        hh = ttk.Frame(f_hea)
        hh.pack(fill="x", pady=(10, 2))
        ttk.Label(hh, text="HEA — se escribe en «Historia de la enfermedad actual» de APS", style="H2.TLabel").pack(
            side="left")
        ttk.Button(hh, text="Otra versión", command=lambda: self._regen_hea(False)).pack(side="right")
        ttk.Label(f_hea, text="Una sola historia con los diagnósticos elegidos (crónicos como antecedente, el agudo como cuadro "
                  "actual, los demás como síntomas). Revísela y corríjala con lo que el paciente refirió; si la edita a "
                  "mano, ya no se reemplaza sola.", style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        self.hea = tk.Text(f_hea, height=6, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1)
        self.hea.insert("1.0", defaults.get("hea", ""))
        self.hea.pack(fill="x")
        self.hea_aviso = ttk.Label(f_hea, text="", style="Muted.TLabel", wraplength=780, justify="left")
        self.hea_aviso.pack(anchor="w")
        ttk.Label(f_exa, text="Examen físico — se escribe en «Examen Físico» de APS", style="H2.TLabel").pack(
            anchor="w", pady=(12, 2))
        ttk.Label(f_exa, text="Examen céfalo-caudal normal; cada sección cambia según los diagnósticos elegidos "
                  "(genitourinario solo si algún diagnóstico lo requiere). Puede corregir el texto; vacío = no se llena.", style="Muted.TLabel", wraplength=780,
                  justify="left").pack(anchor="w")
        ttk.Button(f_exa, text="Otra versión del examen", command=lambda: self._regen_examen(True)).pack(anchor="e")
        self.examen = tk.Text(f_exa, height=11, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1)
        self.examen.insert("1.0", defaults.get("examen_fisico", ""))
        self._exa_auto = defaults.get("examen_fisico", "")
        self.examen.pack(fill="x")
        ttk.Label(f_plan, text="Plan — se escribe en «Plan» de APS", style="H2.TLabel").pack(anchor="w", pady=(12, 2))
        ttk.Label(f_plan, text="Por ahora solo «Plan»; luego habrá un repertorio. Puede escribir o corregir el texto; "
                  "vacío = no se llena.", style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        self.plan = tk.Text(f_plan, height=5, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1)
        self.plan.insert("1.0", defaults.get("plan", ""))
        self.plan.pack(fill="x")
        ttk.Label(f_der, text="Derivación (hacia) y servicio brindado", style="H2.TLabel").pack(anchor="w", pady=(12, 2))
        ttk.Label(f_der, text="Si elige Sí en «¿Va a ser derivado?» se muestran los demás campos, como en ActivityInfo "
                  "(recapitulativo interno de MdM). El servicio brindado siempre es Salud.", style="Muted.TLabel",
                  wraplength=780, justify="left").pack(anchor="w")
        gf3 = ttk.Frame(f_der)
        gf3.pack(fill="x")
        g3 = widgets.FormGrid(gf3, 3)
        # como en la página: lo demás solo aparece cuando «¿Va a ser derivado?» es Sí
        self.der_extra = ttk.Frame(f_der)
        gf4 = ttk.Frame(self.der_extra)
        gf4.pack(fill="x")
        g4 = widgets.FormGrid(gf4, 3)

        def add3(key, label, vals, parent, grid):
            w = widgets.ComboField(parent, [""] + list(vals), readonly=True, width=26)
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            grid.add(label, w)

        add3("va_derivado", "¿Va a ser derivado?", ai.VA_DERIVADO, gf3, g3)
        add3("n_servicios", "¿A cuántos servicios se deriva?", ai.N_SERVICIOS, gf4, g4)
        add3("transfronteriza", "¿Referencia Transfronteriza?", ai.VA_DERIVADO, gf4, g4)
        add3("servicio_brindado", "Servicio brindado", ai.SERVICIOS_BRINDADOS, gf4, g4)
        add3("servicio_salud", "Salud (si el servicio es Salud)", ai.SERVICIOS_SALUD, gf4, g4)
        self.w["va_derivado"].bind("<<ComboboxSelected>>", lambda e: self._mostrar_derivacion())
        self._mostrar_derivacion()
        self._construir_ssr(defaults)
        self._hea_auto = defaults.get("hea", "")      # último texto generado: si la persona lo cambia, se respeta
        self._dx_vistos = self._clave_hea()
        if self._exa_auto.strip() != examen_fisico.compose([], ssr=False).strip():
            self._exa_auto = "\0"        # texto puesto a mano desde fuera: no se pisa
        if self._ssr_exa_auto.strip() != examen_fisico.compose([], ssr=True).strip():
            self._ssr_exa_auto = "\0"
        self._regen_examen()
        # si se corrige el género o la edad en esta ventana, la HEA se actualiza (salvo que ya la haya editado)
        self.w["genero"].bind("<<ComboboxSelected>>", lambda e: (self._ajustar_vitales(), self._regen_hea(True),
                                                                 self._ssr_condicionales()))
        self.w["edad"].bind("<FocusOut>", lambda e: (self._ajustar_vitales(), self._regen_hea(True)))
        self._marcar_fuentes()
        ttk.Button(bar, text="Cancelar", command=self.cancel).pack(side="right")
        ttk.Button(bar, text="Abrir Chrome y llenar", style="Accent.TButton", command=self._ok).pack(
            side="right", padx=8)

    def _filtrar(self, cb, event, labels=None):
        """Al escribir en un diagnóstico, la lista desplegable muestra solo las opciones que contienen ese texto."""
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        labels = labels or self._labels
        q = cat.plain(cb.get_value())
        cb.set_values([x for x in labels if q in cat.plain(x)] or labels if q else labels)

    def _marcar_fuentes(self):
        """Debajo de cada diagnóstico: qué HEA del banco se está usando (o que no hay una preparada)."""
        for tag, fuente in zip(self.dx_tags, self._dx_actuales()):
            n = hea_banco.bank_id(fuente) if fuente else None
            if not fuente:
                tag.configure(text="HEA: (sin diagnóstico)")
            elif n is None:
                tag.configure(text="HEA: no hay una preparada para este diagnóstico; complétela a mano")
            else:
                tag.configure(text="HEA usa: " + hea_banco.BANK[n]["n"])

    def _dx_actuales(self):
        # descripción elegida en la lista de ActivityInfo; si se dejó vacía, el texto del ATA (la HEA lo incluye igual)
        return [hea_banco.fuente_hea(a, cat.from_label(cb.get_value())[0]) for a, cb in self.dx_rows]

    def _dx_hea(self):
        """Diagnósticos de los que sale la HEA: los de APS y, si se marcó SSR, los de la lista SSR (una sola HEA)."""
        dxs = list(self._dx_actuales())
        if hasattr(self, "ssr_rows") and "Salud Sexual y Reproductiva" in self.w["consultas"].get_value():
            for cb in self.ssr_rows:
                d = ssr_cat.from_label(cb.get_value())[0] if hasattr(ssr_cat, "from_label") else cb.get_value()
                if d and d not in dxs:
                    dxs.append(d)
        return dxs

    def _persona(self):
        """Sexo y edad para la HEA: lo del ATA, corregido con lo que se elija en esta ventana."""
        p = dict(self.defaults.get("hea_persona") or {})
        g = (self.w["genero"].get_value() or "").lower()
        if g.startswith("mujer"):
            p["sexo"] = "M"
        elif g.startswith("hombre"):
            p["sexo"] = "H"
        edad = (self.w["edad"].get_value() or "").strip()
        if edad.isdigit() and edad != "0" and edad != p.get("edad"):   # «0» = menor de 1 año: se queda en meses/días
            p["edad"], p["unidad"] = edad, "años"
        return p

    def _construir_ssr(self, defaults):
        """Sección de Salud Sexual y Reproductiva (al final de la ventana; se ve al marcar esa consulta). Sigue el orden
        del subformulario de ActivityInfo y muestra los campos que dependen de lo elegido, igual que la página."""
        f = self.f_ssr
        self._ssr_vistos = {}

        def titulo(txt, pad=(12, 2)):
            ttk.Label(f, text=txt, style="H2.TLabel").pack(anchor="w", pady=pad)

        def nota(txt):
            ttk.Label(f, text=txt, style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")

        def combo(key, label, vals, parent, grid, ro=True):
            w = widgets.ComboField(parent, [""] + list(vals), readonly=ro, width=26)
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            grid.add(label, w)
            return w

        def entry(key, label, parent, grid):
            w = widgets.EntryField(parent, width=26)
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            grid.add(label, w)
            return w

        def caja(txt, alto, valor):
            t = tk.Text(f, height=alto, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1)
            t.insert("1.0", valor or "")
            t.pack(fill="x")
            return t

        titulo("Salud Sexual y Reproductiva — se llena en su subformulario (después del de Atención primaria)", (16, 2))
        nota("El programa pulsa «Está hecho» solo en el de Atención primaria para poder abrir este; en este NO pulsa "
             "nada: usted lo revisa y lo termina. El profesional es el mismo de arriba. Lo que deje vacío no se toca; los "
             "campos que dependen de otro aparecen al elegirlo, como en ActivityInfo.")
        gf5 = ttk.Frame(f)
        gf5.pack(fill="x")
        g5 = widgets.FormGrid(gf5, 3)
        combo("ssr_mismo_punto", "¿Mismo punto de atención de la ficha?", ai.SI_NO, gf5, g5)
        combo("ssr_mismo_proy", "¿Mismo proyecto de la ficha?", ai.SI_NO, gf5, g5)
        combo("ssr_tipo", "Tipo de consulta (vacío = el mismo de APS)", ai.TIPOS_SSR, gf5, g5)
        combo("ssr_ficha", "¿Ficha corta o larga?", ai.SSR_FICHAS, gf5, g5)
        self.w["ssr_ficha"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        combo("ssr_recibio_aps", "¿Recibió APS el mismo día?", ai.SI_NO, gf5, g5)
        combo("ssr_violencia", "¿Ha sufrido violencia?", ai.SSR_VIOLENCIA, gf5, g5)
        self.w["ssr_violencia"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self.ssr_viol_g = ttk.Frame(f)
        combo("ssr_viol_genero", "Violencia de género", ai.SSR_VIOLENCIA_GENERO, self.ssr_viol_g,
              widgets.FormGrid(self.ssr_viol_g, 3))
        self.ssr_viol_o = ttk.Frame(f)
        combo("ssr_viol_otras", "Otras situaciones de violencia", ai.SSR_VIOLENCIA_OTRAS, self.ssr_viol_o,
              widgets.FormGrid(self.ssr_viol_o, 3))
        self._ssr_gf5 = gf5

        titulo("Historia de la enfermedad actual (SSR)")
        nota("Empieza igual que la HEA de Atención primaria (se copia sola mientras no la edite aquí). Corríjala si hace falta; "
             "vacío = no se llena.")
        self.ssr_hea = caja("HEA", 6, defaults.get("hea", ""))
        self._ssr_hea_auto = defaults.get("hea", "")

        titulo("Antecedentes")
        self.ssr_app = ttk.Frame(f)       # ancla (sin contenido) para colocar los campos de ficha larga
        self.ssr_app.pack()
        self.ssr_larga = ttk.Frame(f)           # solo con ficha «Larga»; según el género salen unos u otros, como en la página
        self._ssr_larga_mujer = ttk.Frame(self.ssr_larga)
        gm_ = widgets.FormGrid(self._ssr_larga_mujer, 3)
        entry("ssr_menarquia", "Menarquía (edad en años, 9 a 20)", self._ssr_larga_mujer, gm_)
        entry("ssr_ritmo", "Ritmo menstrual", self._ssr_larga_mujer, gm_)
        combo("ssr_trast_mens", "Trastorno menstrual", ai.SI_NO, self._ssr_larga_mujer, gm_)
        combo("ssr_menopausia", "Menopausia", ai.SI_NO, self._ssr_larga_mujer, gm_)
        wcit = widgets.CalendarEntry(self._ssr_larga_mujer)
        self.w["ssr_citologia"] = wcit
        gm_.add("Última citología (escoja el día)", wcit)
        combo("ssr_prueba_vph", "¿Prueba de VPH el último año?", ai.SSR_SI_NO_NS, self._ssr_larga_mujer, gm_)
        combo("ssr_autoex_mamas", "¿Autoexamen de mamas el último mes?", ai.SSR_SI_NO_NS, self._ssr_larga_mujer, gm_)
        self._ssr_larga_hombre = ttk.Frame(self.ssr_larga)
        gh_ = widgets.FormGrid(self._ssr_larga_hombre, 3)
        entry("ssr_espermarquia", "Espermarquia (edad en años)", self._ssr_larga_hombre, gh_)
        combo("ssr_autoex_test", "¿Autoexamen de testículos el último mes?", ai.SSR_SI_NO_NS, self._ssr_larga_hombre, gh_)
        combo("ssr_tamizaje_prost", "¿Tamizaje de próstata el último año?", ai.SSR_SI_NO_NS, self._ssr_larga_hombre, gh_)
        ga = ttk.Frame(f)
        ga.pack(fill="x")
        col_its = ttk.Frame(ga)
        col_its.pack(side="left", anchor="n", padx=(0, 14))
        col_itu = ttk.Frame(ga)
        col_itu.pack(side="left", anchor="n")
        top_its = ttk.Frame(col_its)
        top_its.pack(fill="x")
        combo("ssr_its", "Antecedentes de ITS", ai.SSR_SI_NO_NS, top_its, widgets.FormGrid(top_its, 1))
        self.w["ssr_its"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self.ssr_its_x = ttk.Frame(col_its)          # lo de ITS va debajo de ITS
        entry("ssr_its_cual", "¿Cuál?", self.ssr_its_x, widgets.FormGrid(self.ssr_its_x, 1))
        top_itu = ttk.Frame(col_itu)
        top_itu.pack(fill="x")
        combo("ssr_itu", "Antecedentes de ITU", ai.SSR_SI_NO_NS, top_itu, widgets.FormGrid(top_itu, 1))
        self.w["ssr_itu"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self.ssr_itu_x = ttk.Frame(col_itu)          # lo de ITU va debajo de ITU
        gu = widgets.FormGrid(self.ssr_itu_x, 1)
        combo("ssr_itu_complicada", "¿ITU complicada?", ai.SI_NO, self.ssr_itu_x, gu)
        entry("ssr_itu_episodios", "Número de episodios de ITU al año", self.ssr_itu_x, gu)
        self._ssr_ga = ga
        titulo("Antecedentes obstétricos")
        gob = ttk.Frame(f)
        gob.pack(fill="x")
        gobg = widgets.FormGrid(gob, 3)
        combo("ssr_embarazo_actual", "Embarazo actual", ai.SI_NO, gob, gobg)
        combo("ssr_embarazo_anterior", "Embarazo anterior", ai.SSR_EMBARAZO_ANTERIOR, gob, gobg)
        for k in ("ssr_embarazo_actual", "ssr_embarazo_anterior"):
            self.w[k].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self._ssr_gob = gob
        self.ssr_emb_x = ttk.Frame(f)           # solo con embarazo actual «Sí»
        ge = ttk.Frame(self.ssr_emb_x)
        ge.pack(fill="x")
        gege = widgets.FormGrid(ge, 3)
        combo("ssr_conoce_fum", "¿Conoce la FUM?", ai.SI_NO, ge, gege)
        self.w["ssr_conoce_fum"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        combo("ssr_cpn", "¿Control prenatal anterior?", ai.SI_NO, ge, gege)
        self.w["ssr_cpn"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self.ssr_fum_x = ttk.Frame(self.ssr_emb_x)        # conoce la FUM = Sí: calendario para escoger el día
        w = widgets.CalendarEntry(self.ssr_fum_x)
        self.w["ssr_fum"] = w
        w.set_value(defaults.get("ssr_fum", ""))
        widgets.FormGrid(self.ssr_fum_x, 3).add("Última menstruación (FUM): escoja el día", w)
        self.ssr_egm_x = ttk.Frame(self.ssr_emb_x)        # conoce la FUM = No: edad gestacional a mano
        entry("ssr_eg_manual", "Edad gestacional (manual, semanas)", self.ssr_egm_x, widgets.FormGrid(self.ssr_egm_x, 3))
        self.ssr_cpn_x = ttk.Frame(self.ssr_emb_x)
        entry("ssr_cpn_lugar", "Lugar de control prenatal", self.ssr_cpn_x, widgets.FormGrid(self.ssr_cpn_x, 3))
        self.ssr_ant_obst = ttk.Frame(f)        # con embarazo anterior distinto de «No hubo embarazo»
        gq = widgets.FormGrid(self.ssr_ant_obst, 4)
        for k, lab in (("gestaciones", "Gestaciones"), ("partos", "Partos"), ("cesareas", "Cesáreas"), ("abortos", "Abortos"),
                       ("obitos", "Óbitos"), ("hijos_vivos", "Hijos vivos"), ("hijos_muertos", "Hijos muertos")):
            entry("ssr_" + k, lab, self.ssr_ant_obst, gq)
        combo("ssr_lactancia", "Lactancia materna", ai.SI_NO, self.ssr_ant_obst, gq)
        ttk.Label(f, text="Vacunación (marque las que apliquen)").pack(anchor="w", pady=(8, 0))
        self.w["ssr_vacunacion"] = ChecksField(f, ai.SSR_VACUNAS, columns=2)
        self.w["ssr_vacunacion"].pack(anchor="w")
        gb = ttk.Frame(f)
        gb.pack(fill="x", pady=(4, 0))
        grb = widgets.FormGrid(gb, 3)
        combo("ssr_vph", "VPH", ai.SI_NO, gb, grb)
        combo("ssr_papanicolau", "Papanicolau", ai.SI_NO, gb, grb)
        combo("ssr_examen_mama", "Examen de mama", ai.SI_NO, gb, grb)
        entry("ssr_observaciones", "Observaciones", gb, grb)

        titulo("Exámen físico (SSR)")
        nota("Examen céfalo-caudal normal, con genitourinario. Puede corregirlo; vacío = no se llena.")
        self.ssr_examen = caja("Examen", 11, defaults.get("ssr_examen_fisico", defaults.get("examen_fisico", "")))
        self._ssr_exa_auto = defaults.get("ssr_examen_fisico", defaults.get("examen_fisico", ""))

        titulo("Diagnósticos — lista de ActivityInfo SSR (descripción y código)")
        self._ssr_labels = [ssr_cat.label(d) for d in ssr_cat.descriptions()]
        self.ssr_rows = []
        sug = defaults.get("ssr_dx") or []
        if not sug:
            sug = [{"abrev": "", "descripcion": ""} for _ in range(ai.SSR_MAX_DX)]
        for i, x in enumerate(sug):
            row = ttk.Frame(f)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=f"{i + 1}. {x['abrev']}" if x["abrev"] else f"{i + 1}.", width=22).pack(side="left")
            cb = widgets.ComboField(row, self._ssr_labels, readonly=False, width=78)
            if x.get("descripcion"):
                cb.set_value(ssr_cat.label(x["descripcion"]))
            cb.pack(side="left", fill="x", expand=True)
            cb.bind("<KeyRelease>", lambda e, c=cb: self._filtrar(c, e, self._ssr_labels))
            cb.bind("<<ComboboxSelected>>", lambda e: self._regen_hea(True))
            cb.bind("<FocusOut>", lambda e: self._regen_hea(True))
            self.ssr_rows.append(cb)
        nota("Elija en la lista de ActivityInfo de SSR (puede escribir para buscar). SSR admite máximo 2 diagnósticos: deje "
             "vacíos los que no apliquen (los que no tienen equivalente en SSR quedan vacíos).")
        go = ttk.Frame(f)
        go.pack(fill="x", pady=(6, 0))
        gro = widgets.FormGrid(go, 3)
        entry("ssr_obs_dx", "Observaciones del diagnóstico", go, gro)

        titulo("Uso de métodos anticonceptivos")
        gm = ttk.Frame(f)
        gm.pack(fill="x")
        grm = widgets.FormGrid(gm, 3)
        combo("ssr_consejeria", "¿Recibió consejería anticoncepción?", ["Si", "No"], gm, grm)
        self.w["ssr_consejeria"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self._ssr_gm = gm
        self.ssr_met = ttk.Frame(f)      # solo si hubo consejería
        gm2 = ttk.Frame(self.ssr_met)
        gm2.pack(fill="x")
        self._ssr_gm2 = gm2
        grm2 = widgets.FormGrid(gm2, 3)
        combo("ssr_ya_planifica", "¿Ya planifica? (usa un método hoy)", ai.SI_NO, gm2, grm2)
        self.w["ssr_ya_planifica"].bind("<<ComboboxSelected>>", lambda e: self._ssr_condicionales())
        self.ssr_actuales = ttk.LabelFrame(self.ssr_met, text=" 1) Método que USA ACTUALMENTE (antes de esta consulta) ",
                                           padding=8)
        ttk.Label(self.ssr_actuales, text="Elija hasta 2 métodos que la persona ya está usando.",
                  style="Muted.TLabel").pack(anchor="w")
        ga2 = ttk.Frame(self.ssr_actuales)
        ga2.pack(fill="x")
        gra = widgets.FormGrid(ga2, 2)
        combo("ssr_act_1", "Método actual", ai.SSR_METODOS_ACTUALES, ga2, gra)
        combo("ssr_act_2", "Otro método actual (opcional)", ai.SSR_METODOS_ACTUALES, ga2, gra)
        marco_e = ttk.LabelFrame(self.ssr_met, text=" 2) Método ELEGIDO HOY (después de la consejería) ", padding=8)
        marco_e.pack(fill="x", pady=(8, 0))
        ttk.Label(marco_e, text="Elija hasta 2 métodos que la persona decidió usar a partir de esta consulta "
                  "(se recomienda protección dual). «Ninguno» si no eligió.", style="Muted.TLabel", wraplength=740,
                  justify="left").pack(anchor="w")
        ge2 = ttk.Frame(marco_e)
        ge2.pack(fill="x")
        gre2 = widgets.FormGrid(ge2, 2)
        combo("ssr_eleg_1", "Método elegido", ai.SSR_METODOS_ELEGIDOS, ge2, gre2)
        combo("ssr_eleg_2", "Otro método elegido (opcional)", ai.SSR_METODOS_ELEGIDOS, ge2, gre2)
        ga3 = ttk.Frame(self.ssr_met)
        ga3.pack(fill="x", pady=(8, 0))
        combo("ssr_acceso", "Acceso: ¿la persona tiene acceso al método elegido?", ai.SI_NO, ga3, widgets.FormGrid(ga3, 1))
        ttk.Label(self.ssr_met, text="Las listas van de los métodos más usados a los menos usados.",
                  style="Muted.TLabel").pack(anchor="w")

        titulo("Plan (SSR)")
        nota("Por ahora solo «Plan». Vacío = no se llena.")
        self.ssr_plan = caja("Plan", 4, defaults.get("plan", ""))

        titulo("Derivación (SSR)")
        gd = ttk.Frame(f)
        gd.pack(fill="x")
        grd = widgets.FormGrid(gd, 3)
        combo("ssr_va_derivado", "¿Va a ser derivado?", ai.VA_DERIVADO, gd, grd)
        self.w["ssr_va_derivado"].bind("<<ComboboxSelected>>", lambda e: self._mostrar_ssr_der())
        self.ssr_der_extra = ttk.Frame(f)
        gd2 = ttk.Frame(self.ssr_der_extra)
        gd2.pack(fill="x")
        grd2 = widgets.FormGrid(gd2, 3)
        combo("ssr_transfronteriza", "Referencia Transfronteriza", ai.VA_DERIVADO, gd2, grd2)
        combo("ssr_servicio_brindado", "Servicio brindado", ai.SERVICIOS_BRINDADOS, gd2, grd2)
        combo("ssr_servicio_salud", "Salud (si el servicio es Salud)", ai.SSR_SERVICIOS_SALUD, gd2, grd2)
        self.ssr_f_victima = ttk.Frame(f)
        grv = widgets.FormGrid(self.ssr_f_victima, 3)
        combo("ssr_victima_sexual", "¿Víctima de violencia sexual?", ai.SI_NO, self.ssr_f_victima, grv)
        self._ssr_condicionales()
        self._mostrar_ssr_der()
        self._mostrar_ssr()

    def _ssr_condicionales(self):
        """Muestra u oculta lo que en ActivityInfo solo aparece según lo elegido (violencia, ITS, ITU, consejería)."""
        for fr in (self.ssr_viol_g, self.ssr_viol_o, self.ssr_its_x, self.ssr_itu_x, self.ssr_met, self.ssr_emb_x,
                   self.ssr_fum_x, self.ssr_egm_x, self.ssr_cpn_x, self.ssr_ant_obst):
            fr.pack_forget()
        self.ssr_larga.pack_forget()
        self._ssr_larga_mujer.pack_forget()
        self._ssr_larga_hombre.pack_forget()
        if self.w["ssr_ficha"].get_value() == "Larga" and self.w["genero"].get_value():
            self.ssr_larga.pack(fill="x", after=self.ssr_app)
            if self.w["genero"].get_value() in ("Mujer CIS", "Hombre TRANS"):
                self._ssr_larga_mujer.pack(fill="x")
            else:
                self._ssr_larga_hombre.pack(fill="x")
        v = self.w["ssr_violencia"].get_value()
        if v == "Violencia Basada en Género":
            self.ssr_viol_g.pack(fill="x", after=self._ssr_gf5)
        elif v == "Otra Situación de Violencia":
            self.ssr_viol_o.pack(fill="x", after=self._ssr_gf5)
        if self.w["ssr_its"].get_value() == "Sí":
            self.ssr_its_x.pack(fill="x")
        if self.w["ssr_itu"].get_value() == "Sí":
            self.ssr_itu_x.pack(fill="x")
        if self.w["ssr_embarazo_actual"].get_value() == "Sí":
            self.ssr_emb_x.pack(fill="x", after=self._ssr_gob)
            conoce = self.w["ssr_conoce_fum"].get_value()
            if conoce == "Sí":
                self.ssr_fum_x.pack(fill="x")
            elif conoce == "No":
                self.ssr_egm_x.pack(fill="x")
            if self.w["ssr_cpn"].get_value() == "Sí":
                self.ssr_cpn_x.pack(fill="x")
        ant = self.w["ssr_embarazo_anterior"].get_value()
        if ant and ant != "No hubo embarazo":
            self.ssr_ant_obst.pack(fill="x", after=self.ssr_emb_x if self.ssr_emb_x.winfo_manager() else self._ssr_gob)
        cons = self.w["ssr_consejeria"].get_value() == "Si"
        if cons:
            self.ssr_met.pack(fill="x", after=self._ssr_gm)
        self.ssr_actuales.pack_forget()
        if cons and self.w["ssr_ya_planifica"].get_value() == "Sí":
            self.ssr_actuales.pack(fill="x", after=self._ssr_gm2, pady=(6, 0))

    def _mostrar_ssr_der(self):
        self.ssr_der_extra.pack_forget()
        self.ssr_f_victima.pack_forget()
        if self.w["ssr_va_derivado"].get_value() == "Sí":
            self.ssr_der_extra.pack(fill="x", after=self.w["ssr_va_derivado"].master)
        self.ssr_f_victima.pack(fill="x", pady=(6, 0))

    def _sync_ssr_hea(self):
        """La HEA de SSR copia la de APS mientras la persona no la haya editado."""
        actual = self.ssr_hea.get("1.0", "end").strip()
        if actual == self._ssr_hea_auto.strip():
            nuevo = self.hea.get("1.0", "end").strip()
            self.ssr_hea.delete("1.0", "end")
            self.ssr_hea.insert("1.0", nuevo)
            self._ssr_hea_auto = nuevo

    def _mostrar_ssr(self):
        if "Salud Sexual y Reproductiva" in self.w["consultas"].get_value():
            self.f_ssr.pack(fill="x")
            self._regen_hea(True)
            self._sync_ssr_hea()
        else:
            self.f_ssr.pack_forget()

    def _mostrar_derivacion(self):
        """«Servicio brindado» y lo demás solo existen en la página cuando «¿Va a ser derivado?» es Sí."""
        if self.w["va_derivado"].get_value() == "Sí":
            self.der_extra.pack(fill="x")
        else:
            self.der_extra.pack_forget()

    def _ajustar_vitales(self):
        """Si cambian el género o la edad a otra franja (p. ej. de lactante a escolar), se proponen de nuevo los signos
        vitales de esa franja, solo en los campos que la persona no había cambiado."""
        p = self._persona()
        grupo = ai.grupo_vitales(p.get("sexo"), p.get("edad"), p.get("unidad", "años"))
        if grupo == self._vit_grupo:
            return
        self._vit_grupo = grupo
        nuevo = ai.vitales_defecto(p.get("sexo"), p.get("edad"), p.get("unidad", "años"))
        for k in ("sistolica", "diastolica", "fc", "fr"):
            if self.w[k].get_value() == self._vit_auto.get(k):
                self.w[k].set_value(nuevo[k])
                self._vit_auto[k] = nuevo[k]

    def _clave_hea(self):
        p = self._persona()
        return (tuple(self._dx_hea()), p.get("sexo"), p.get("edad"), p.get("unidad"))

    def _regen_examen(self, forzar=False):
        """Examen físico por secciones según los diagnósticos; si se editó a mano, no se pisa (salvo «Otra versión»)."""
        def poner(caja, texto, auto_attr):
            if not forzar and caja.get("1.0", "end").strip() != getattr(self, auto_attr, "").strip():
                return
            caja.delete("1.0", "end")
            caja.insert("1.0", texto)
            setattr(self, auto_attr, texto)
        aps = [d for d in self._dx_actuales() if d]
        rng = random.Random()
        poner(self.examen, examen_fisico.compose(aps, ssr=False, rng=rng), "_exa_auto")
        if hasattr(self, "ssr_examen"):
            poner(self.ssr_examen, examen_fisico.compose([d for d in self._dx_hea() if d], ssr=True, rng=rng), "_ssr_exa_auto")

    def _regen_hea(self, solo_si_cambio):
        """Vuelve a armar la HEA con los diagnósticos elegidos. Si la persona editó el texto a mano, no lo pisa
        (salvo con «Otra versión»)."""
        self._marcar_fuentes()
        self._regen_examen()
        dxs = self._dx_hea()
        if solo_si_cambio:
            clave = self._clave_hea()
            if clave == self._dx_vistos:
                return
            self._dx_vistos = clave
            if self.hea.get("1.0", "end").strip() != self._hea_auto.strip():
                return
        p = self._persona()
        texto, avisos = hea_banco.compose(p.get("sexo"), p.get("edad"), [d for d in dxs if d], p.get("unidad", "años"))
        self.hea.delete("1.0", "end")
        self.hea.insert("1.0", texto)
        self._hea_auto = texto
        self.hea_aviso.configure(text="\n".join("⚠ " + a for a in avisos))
        if hasattr(self, "ssr_hea"):
            self._sync_ssr_hea()

    def run(self):                      # ya tiene tamaño y posición propios (900 x 700, centrada)
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.wait_window(self)
        return self.result

    def _ok(self):
        data = {k: (w.get_value() if isinstance(w, ChecksField) else w.get_value().strip())
                for k, w in self.w.items()}
        if not data["consultas"]:
            dialogs.info(self, "Marque al menos una consulta a realizar.")
            return
        falta = [t for k, t in ai.OBLIGATORIOS if not data.get(k)]
        if "Atención Primaria de Salud" in data["consultas"] and not data.get("tipo_consulta"):
            falta.append("Tipo de consulta (APS)")
        if falta and not dialogs.confirm(
                self, "Faltan datos obligatorios", "Estos campos obligatorios están vacíos y quedarán sin llenar "
                "en ActivityInfo:\n\n" + "\n".join(f"• {t}" for t in falta) + "\n\n¿Abrir Chrome de todos modos?",
                yes="Abrir de todos modos", no="Volver y elegir"):
            return
        dx, malos = [], []
        for a, cb in self.dx_rows:
            texto = cb.get_value().strip()
            desc, code = cat.from_label(texto)
            if texto and not desc:
                malos.append(texto)
            if desc:
                dx.append({"abrev": a, "descripcion": desc, "cie11": code})
        if malos:
            dialogs.info(self, "Estos diagnósticos no están en la lista de ActivityInfo; elíjalos de la lista "
                         "desplegable:\n\n" + "\n".join(f"• {m}" for m in malos))
            return
        data["dx"] = dx
        data["recordar_dx"] = bool(self.recordar.get())
        quiere_ssr = "Salud Sexual y Reproductiva" in data["consultas"]
        if quiere_ssr:
            self._sync_ssr_hea()
        ssr_dx, malos_ssr = [], []
        if quiere_ssr:
            for cb in self.ssr_rows:
                texto = cb.get_value().strip()
                desc, code = ssr_cat.from_label(texto)
                if texto and not desc:
                    malos_ssr.append(texto)
                if desc and desc not in [x["descripcion"] for x in ssr_dx]:
                    ssr_dx.append({"abrev": "", "descripcion": desc, "cie11": code})
            if len(ssr_dx) > ai.SSR_MAX_DX:
                dialogs.info(self, f"Salud Sexual y Reproductiva admite máximo {ai.SSR_MAX_DX} diagnósticos. Deje vacíos los "
                             "que sobren.")
                return
            if malos_ssr:
                dialogs.info(self, "Estos diagnósticos no están en la lista de Salud Sexual y Reproductiva; elíjalos de la "
                             "lista desplegable:\n\n" + "\n".join(f"• {m}" for m in malos_ssr))
                return
        if quiere_ssr and self.w["ssr_embarazo_actual"].get_value() == "Sí" and self.w["ssr_conoce_fum"].get_value() == "Sí":
            fum = self.w["ssr_fum"].get_value()
            f = widgets.CalendarEntry.parse(fum)
            if fum and (f is None or f > __import__("datetime").date.today()):
                dialogs.info(self, "La fecha de la última menstruación (FUM) no es válida. Escójala con el calendario 📅 "
                             "(formato AAAA-MM-DD, y no puede ser futura).")
                return
        data["hea"] = self.hea.get("1.0", "end").strip()
        data["examen_fisico"] = self.examen.get("1.0", "end").strip()
        data["plan"] = self.plan.get("1.0", "end").strip()
        if data.get("va_derivado") != "Sí":       # sin Sí no existen esos campos en la página
            for k in ("n_servicios", "transfronteriza", "servicio_brindado", "servicio_salud"):
                data[k] = ""
        data["tiene_fecha_nac"] = "No"  # siempre se usa la edad
        for k in [k for k in data if k.startswith("ssr_")]:
            data.pop(k)
        if quiere_ssr:
            tipo = self.w["ssr_tipo"].get_value() or (data.get("tipo_consulta") if data.get("tipo_consulta") in ai.TIPOS_SSR else "")
            W = lambda k: self.w[k].get_value()  # noqa: E731
            uniq = lambda *ks: [v for i, v in enumerate([W(k) for k in ks]) if v and v not in [W(k) for k in ks][:i]]  # noqa: E731
            data["ssr"] = {"mismo_punto": W("ssr_mismo_punto"), "mismo_proy": W("ssr_mismo_proy"),
                           "tipo": tipo, "ficha": W("ssr_ficha"),
                           "recibio_aps": W("ssr_recibio_aps") if "Atención Primaria de Salud" in data["consultas"] else "",
                           "dx": ssr_dx, "n_dx": len(ssr_dx) or "",
                           "violencia": W("ssr_violencia"),
                           "viol_genero": W("ssr_viol_genero") if W("ssr_violencia") == "Violencia Basada en Género" else "",
                           "viol_otras": W("ssr_viol_otras") if W("ssr_violencia") == "Otra Situación de Violencia" else "",
                           "hea": self.ssr_hea.get("1.0", "end").strip(),
                           **({k: W("ssr_" + k).strip() if isinstance(W("ssr_" + k), str) else W("ssr_" + k)
                               for k in ("menarquia", "ritmo", "trast_mens", "menopausia", "citologia", "prueba_vph",
                                         "autoex_mamas")}
                              if W("ssr_ficha") == "Larga" and W("genero") in ("Mujer CIS", "Hombre TRANS") else {}),
                           **({k: W("ssr_" + k).strip() for k in ("espermarquia", "autoex_test", "tamizaje_prost")}
                              if W("ssr_ficha") == "Larga" and W("genero") and W("genero") not in ("Mujer CIS", "Hombre TRANS") else {}),
                           "its": W("ssr_its"), "its_cual": W("ssr_its_cual").strip() if W("ssr_its") == "Sí" else "",
                           "itu": W("ssr_itu"),
                           "itu_complicada": W("ssr_itu_complicada") if W("ssr_itu") == "Sí" else "",
                           "itu_episodios": W("ssr_itu_episodios").strip() if W("ssr_itu") == "Sí" else "",
                           "vph": W("ssr_vph"), "papanicolau": W("ssr_papanicolau"), "examen_mama": W("ssr_examen_mama"),
                           "vacunacion": W("ssr_vacunacion"), "observaciones": W("ssr_observaciones").strip(),
                           "examen_fisico": self.ssr_examen.get("1.0", "end").strip(),
                           "obs_dx": W("ssr_obs_dx").strip(), "consejeria": W("ssr_consejeria"),
                           "ya_planifica": W("ssr_ya_planifica") if W("ssr_consejeria") == "Si" else "",
                           "acceso": W("ssr_acceso") if W("ssr_consejeria") == "Si" else "",
                           "embarazo_actual": W("ssr_embarazo_actual"), "embarazo_anterior": W("ssr_embarazo_anterior"),
                           **({"conoce_fum": W("ssr_conoce_fum"), "cpn": W("ssr_cpn"),
                               "fum": W("ssr_fum").strip() if W("ssr_conoce_fum") == "Sí" else "",
                               "eg_manual": W("ssr_eg_manual").strip() if W("ssr_conoce_fum") == "No" else "",
                               "cpn_lugar": W("ssr_cpn_lugar").strip() if W("ssr_cpn") == "Sí" else ""}
                              if W("ssr_embarazo_actual") == "Sí" else {}),
                           **({k: W("ssr_" + k).strip() for k in ("gestaciones", "partos", "cesareas", "abortos", "obitos",
                                                                    "hijos_vivos", "hijos_muertos")}
                              if W("ssr_embarazo_anterior") not in ("", "No hubo embarazo") else {}),
                           "lactancia": W("ssr_lactancia") if W("ssr_embarazo_anterior") not in ("", "No hubo embarazo") else "",
                           "metodos_actuales": uniq("ssr_act_1", "ssr_act_2") if W("ssr_ya_planifica") == "Sí" and W("ssr_consejeria") == "Si" else [],
                           "metodos_elegidos": uniq("ssr_eleg_1", "ssr_eleg_2") if W("ssr_consejeria") == "Si" else [],
                           "plan": self.ssr_plan.get("1.0", "end").strip(),
                           "va_derivado": W("ssr_va_derivado"), "victima_sexual": W("ssr_victima_sexual")}
            if data["ssr"]["va_derivado"] == "Sí":
                data["ssr"].update({"transfronteriza": self.w["ssr_transfronteriza"].get_value(),
                                    "servicio_brindado": self.w["ssr_servicio_brindado"].get_value(),
                                    "servicio_salud": self.w["ssr_servicio_salud"].get_value()})
        self.result = data
        self.destroy()
