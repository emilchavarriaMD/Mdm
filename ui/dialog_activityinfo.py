"""Ventana de revisión antes de llenar ActivityInfo: la persona confirma o corrige cada dato."""
import tkinter as tk
from tkinter import ttk

from services import activityinfo as ai
from services import cie11_catalog as cat
from services import cie11_ssr as ssr_cat
from services import hea_banco
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
        self._vit_auto = {k: self.w[k].get_value() for k in ("diastolica", "fr")}

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
        ttk.Label(f_exa, text="Por ahora solo «Cefalo-caudal»; luego habrá una biblioteca de exámenes. Puede escribir o "
                  "corregir el texto; vacío = no se llena.", style="Muted.TLabel", wraplength=780,
                  justify="left").pack(anchor="w")
        self.examen = tk.Text(f_exa, height=5, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1)
        self.examen.insert("1.0", defaults.get("examen_fisico", ""))
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
        # si se corrige el género o la edad en esta ventana, la HEA se actualiza (salvo que ya la haya editado)
        self.w["genero"].bind("<<ComboboxSelected>>", lambda e: (self._ajustar_vitales(), self._regen_hea(True)))
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
        """Sección de Salud Sexual y Reproductiva: se despliega abajo del todo al marcar esa consulta. La HEA, el examen
        físico, el plan y el profesional son los mismos de Atención primaria; los diagnósticos tienen su propia lista."""
        f = self.f_ssr
        ttk.Label(f, text="Salud Sexual y Reproductiva — se llena en su subformulario (después del de Atención primaria)",
                  style="H2.TLabel").pack(anchor="w", pady=(16, 2))
        ttk.Label(f, text="Usa la misma HEA, el mismo examen físico, el mismo plan y el mismo profesional de Atención primaria "
                  "(los de arriba). El programa pulsa «Está hecho» solo en el de Atención primaria para poder abrir este; en "
                  "este NO pulsa nada: usted lo revisa y lo termina. Lo que deje vacío no se toca.", style="Muted.TLabel",
                  wraplength=780, justify="left").pack(anchor="w")
        gf5 = ttk.Frame(f)
        gf5.pack(fill="x")
        g5 = widgets.FormGrid(gf5, 3)

        def add5(key, label, vals, parent=None, grid=None):
            w = widgets.ComboField(parent or gf5, [""] + list(vals), readonly=True, width=26)
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            (grid or g5).add(label, w)

        add5("ssr_mismo_punto", "¿Mismo punto de atención de la ficha?", ai.SI_NO)
        add5("ssr_mismo_proy", "¿Mismo proyecto de la ficha?", ai.SI_NO)
        add5("ssr_tipo", "Tipo de consulta (vacío = el mismo de APS)", ai.TIPOS_SSR)
        add5("ssr_ficha", "¿Ficha corta o larga?", ai.SSR_FICHAS)
        add5("ssr_recibio_aps", "¿Recibió APS el mismo día?", ai.SI_NO)
        add5("ssr_violencia", "¿Ha sufrido violencia?", ai.SSR_VIOLENCIA)
        # Antecedentes (van después de la HEA en la página)
        ttk.Label(f, text="Antecedentes", style="H2.TLabel").pack(anchor="w", pady=(10, 2))
        ga = ttk.Frame(f)
        ga.pack(fill="x")
        gr = widgets.FormGrid(ga, 3)
        add5("ssr_its", "Antecedentes de ITS", ai.SSR_SI_NO_NS, ga, gr)
        add5("ssr_itu", "Antecedentes de ITU", ai.SSR_SI_NO_NS, ga, gr)
        add5("ssr_vph", "VPH", ai.SI_NO, ga, gr)
        add5("ssr_papanicolau", "Papanicolau", ai.SI_NO, ga, gr)
        add5("ssr_examen_mama", "Examen de mama", ai.SI_NO, ga, gr)
        w = widgets.EntryField(ga, width=26)
        self.w["ssr_observaciones"] = w
        w.set_value(defaults.get("ssr_observaciones", ""))
        gr.add("Observaciones", w)
        ttk.Label(f, text="Vacunación (marque las que apliquen)").pack(anchor="w", pady=(4, 0))
        self.w["ssr_vacunacion"] = ChecksField(f, ai.SSR_VACUNAS, columns=2)
        self.w["ssr_vacunacion"].pack(anchor="w")
        # Diagnósticos: mismo formato que los de Atención primaria (uno por cada diagnóstico del ATA)
        ttk.Label(f, text="Diagnósticos — lista de ActivityInfo SSR (descripción y código)",
                  style="H2.TLabel").pack(anchor="w", pady=(10, 2))
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
            self.ssr_rows.append(cb)
        ttk.Label(f, text="Elija en la lista de ActivityInfo de SSR (puede escribir para buscar). SSR admite máximo 2 "
                  f"diagnósticos: deje vacíos los que no apliquen (los que no tienen equivalente en SSR quedan vacíos).",
                  style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        go = ttk.Frame(f)
        go.pack(fill="x", pady=(6, 0))
        gro = widgets.FormGrid(go, 3)
        w = widgets.EntryField(go, width=26)
        self.w["ssr_obs_dx"] = w
        w.set_value(defaults.get("ssr_obs_dx", ""))
        gro.add("Observaciones del diagnóstico", w)
        add5("ssr_consejeria", "¿Consejería anticoncepción?", ["Si", "No"], go, gro)
        # Derivación (después del plan): lo demás solo existe si «¿Va a ser derivado?» es Sí
        ttk.Label(f, text="Derivación (SSR)", style="H2.TLabel").pack(anchor="w", pady=(10, 2))
        gd = ttk.Frame(f)
        gd.pack(fill="x")
        grd = widgets.FormGrid(gd, 3)
        add5("ssr_va_derivado", "¿Va a ser derivado?", ai.VA_DERIVADO, gd, grd)
        self.ssr_der_extra = ttk.Frame(f)
        gd2 = ttk.Frame(self.ssr_der_extra)
        gd2.pack(fill="x")
        grd2 = widgets.FormGrid(gd2, 3)
        add5("ssr_transfronteriza", "Referencia Transfronteriza", ai.VA_DERIVADO, gd2, grd2)
        add5("ssr_servicio_brindado", "Servicio brindado", ai.SERVICIOS_BRINDADOS, gd2, grd2)
        add5("ssr_servicio_salud", "Salud (si el servicio es Salud)", ai.SSR_SERVICIOS_SALUD, gd2, grd2)
        self.w["ssr_va_derivado"].bind("<<ComboboxSelected>>", lambda e: self._mostrar_ssr_der())
        gv = ttk.Frame(f)
        self.ssr_f_victima = gv
        grv = widgets.FormGrid(gv, 3)
        add5("ssr_victima_sexual", "¿Víctima de violencia sexual?", ai.SI_NO, gv, grv)
        self._mostrar_ssr_der()
        self._mostrar_ssr()

    def _mostrar_ssr_der(self):
        self.ssr_der_extra.pack_forget()
        self.ssr_f_victima.pack_forget()
        if self.w["ssr_va_derivado"].get_value() == "Sí":
            self.ssr_der_extra.pack(fill="x")
        self.ssr_f_victima.pack(fill="x", pady=(6, 0))

    def _mostrar_ssr(self):
        if "Salud Sexual y Reproductiva" in self.w["consultas"].get_value():
            self.f_ssr.pack(fill="x")
        else:
            self.f_ssr.pack_forget()

    def _mostrar_derivacion(self):
        """«Servicio brindado» y lo demás solo existen en la página cuando «¿Va a ser derivado?» es Sí."""
        if self.w["va_derivado"].get_value() == "Sí":
            self.der_extra.pack(fill="x")
        else:
            self.der_extra.pack_forget()

    def _ajustar_vitales(self):
        """Si cambian el género o la edad, la diastólica y la frecuencia respiratoria propuestas se ajustan
        (solo si la persona no las había cambiado)."""
        p = self._persona()
        nuevo = ai.vitales_defecto(p.get("sexo"), p.get("edad"), p.get("unidad", "años"))
        for k in ("diastolica", "fr"):
            if self.w[k].get_value() == self._vit_auto.get(k):
                self.w[k].set_value(nuevo[k])
                self._vit_auto[k] = nuevo[k]

    def _clave_hea(self):
        p = self._persona()
        return (tuple(self._dx_actuales()), p.get("sexo"), p.get("edad"), p.get("unidad"))

    def _regen_hea(self, solo_si_cambio):
        """Vuelve a armar la HEA con los diagnósticos elegidos. Si la persona editó el texto a mano, no lo pisa
        (salvo con «Otra versión»)."""
        dxs = self._dx_actuales()
        self._marcar_fuentes()
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
            data["ssr"] = {"mismo_punto": self.w["ssr_mismo_punto"].get_value(), "mismo_proy": self.w["ssr_mismo_proy"].get_value(),
                           "tipo": tipo, "ficha": self.w["ssr_ficha"].get_value(),
                           "recibio_aps": self.w["ssr_recibio_aps"].get_value() if "Atención Primaria de Salud" in data["consultas"] else "",
                           "dx": ssr_dx, "n_dx": len(ssr_dx) or "",
                           "violencia": self.w["ssr_violencia"].get_value(), "its": self.w["ssr_its"].get_value(),
                           "itu": self.w["ssr_itu"].get_value(), "vph": self.w["ssr_vph"].get_value(),
                           "papanicolau": self.w["ssr_papanicolau"].get_value(),
                           "examen_mama": self.w["ssr_examen_mama"].get_value(),
                           "vacunacion": self.w["ssr_vacunacion"].get_value(),
                           "observaciones": self.w["ssr_observaciones"].get_value().strip(),
                           "obs_dx": self.w["ssr_obs_dx"].get_value().strip(),
                           "consejeria": self.w["ssr_consejeria"].get_value(),
                           "va_derivado": self.w["ssr_va_derivado"].get_value(),
                           "victima_sexual": self.w["ssr_victima_sexual"].get_value()}
            if data["ssr"]["va_derivado"] == "Sí":
                data["ssr"].update({"transfronteriza": self.w["ssr_transfronteriza"].get_value(),
                                    "servicio_brindado": self.w["ssr_servicio_brindado"].get_value(),
                                    "servicio_salud": self.w["ssr_servicio_salud"].get_value()})
        self.result = data
        self.destroy()
