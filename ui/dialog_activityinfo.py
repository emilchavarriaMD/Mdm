"""Ventana de revisión antes de llenar ActivityInfo: la persona confirma o corrige cada dato."""
import random
import tkinter as tk
from tkinter import ttk

from services import activityinfo as ai
from services import coherencia
from services import cie11_catalog as cat
from services import cie11_ssr as ssr_cat
from services import hea_banco
from services import examen_fisico, plan_banco
from services import medicamentos
from ui import dialogs, med_picker, theme, widgets
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
        self.snap = None
        self._restaurado = bool(defaults.get("_restaurado"))
        self.w = {}
        self.transient("")                 # sin «transient», Windows muestra los botones de maximizar/minimizar
        self.resizable(True, True)
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = min(1090, sw - 40), min(700, sh - 90)
        self.geometry(f"{w}x{h}+{max(0, (sw - w) // 2)}+{max(0, (sh - h) // 3)}")
        self.minsize(760, 420)
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
        self.secciones = {}
        gf = self._sec(body, "datos", "Datos de la ficha y de la consulta")
        g = widgets.FormGrid(gf, 3)

        def add(key, label, w, span=1):
            self.w[key] = w
            w.set_value(defaults.get(key, ""))
            g.add(label, w, span=span)

        E = lambda: widgets.EntryField(gf, width=26)  # noqa: E731
        C = lambda vals, ro=True: widgets.ComboField(gf, [""] + list(vals), readonly=ro, width=26)  # noqa: E731
        add("lugar", "Lugar de atención (San Pedro Sula o Choloma según el ATA)",
            widgets.ComboField(gf, [""] + list(ai.LUGARES_ATENCION), readonly=False, width=26))
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
        add("telefono", "Número de teléfono (con prefijo internacional)", E())
        add("discapacidad", "¿Tiene alguna discapacidad?", C(ai.DISCAPACIDAD))
        self.w["discapacidad"].bind("<<ComboboxSelected>>", lambda _e: self._mostrar_disc())
        self._disc_tipo = ChecksField(gf, ai.TIPOS_DISCAPACIDAD, columns=4)
        add("discapacidad_tipo", "¿Qué tipo de discapacidad? (solo si es «Sí»; puede marcar más de una)",
            self._disc_tipo, span=3)
        self._disc_lbl = gf.grid_slaves(row=self.w["discapacidad_tipo"].grid_info()["row"] - 1)
        self._mostrar_disc()
        add("perfil", "Perfil de población", C(ai.PERFILES))
        add("derivado", "¿Ha sido derivado/a?", C(ai.DERIVADO))
        self.w["derivado"].bind("<<ComboboxSelected>>", lambda _e: self._mostrar_derivado_desde())
        g.newline()                       # Derivación (desde): su propia fila, solo si la respuesta es «Sí»
        add("derivado_procedencia", "Procedencia de la derivación", C(ai.PROCEDENCIAS))
        add("derivado_obs", "Derivación: observaciones", E())
        add("derivado_codigo", "Derivación: código de referencia", E())
        g.newline()
        self._der_desde = {}
        for k in ("derivado_procedencia", "derivado_obs", "derivado_codigo"):
            w = self.w[k]
            self._der_desde[k] = [w] + list(gf.grid_slaves(row=w.grid_info()["row"] - 1, column=w.grid_info()["column"]))
        self._mostrar_derivado_desde()
        add("nacionalidad", "País de nacionalidad", E())
        add("idioma", "Idioma", E())
        add("consultas", "Consulta a realizar (puede marcar más de una)",
            ChecksField(gf, ai.CONSULTAS, command=lambda: self._mostrar_ssr()), span=3)
        add("profesional", "Profesional que atiende (APS)", E())
        add("tipo_consulta", "Tipo de consulta (APS)", C(ai.TIPOS_CONSULTA))
        # Orden de la página de ActivityInfo (subformulario APS): HEA, signos vitales y peso, examen físico, diagnósticos
        f_hea = self._sec(body, "hea", "Historia de la enfermedad actual (HEA)")
        f_vit = self._sec(body, "vit", "Signos vitales y peso")
        f_exa = self._sec(body, "exa", "Examen físico")
        f_dx = self._sec(body, "dx", "Diagnósticos")
        f_plan = self._sec(body, "plan", "Plan")
        f_der = self._sec(body, "der", "Derivación y servicio brindado")
        self.f_ssr = ttk.Frame(body)           # al final de todo; solo se ve si se marca Salud Sexual y Reproductiva
        self.ssr_sec = widgets.Seccion(self.f_ssr, "Salud sexual y reproductiva")     # con viñeta plegable, como las demás
        self.secciones["ssr"] = self.ssr_sec
        ttk.Label(f_vit, text="Frecuencia respiratoria: en niños, elíjala; vacío = no se llena.", style="Muted.TLabel").pack(anchor="w")
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
        # menores de 18 años: estado civil, escolaridad y ocupación «No aplica / Ninguno / No aplica» (solo mientras no se cambien)
        self._soc_auto = {k: self.w[k].get_value() for k in ("estado_civil", "escolaridad", "ocupacion")}
        self._soc_menor = ai.es_menor_de_edad(_p0.get("edad"), _p0.get("unidad", "años"))

        dxs = defaults.get("dx") or []
        ttk.Label(f_dx, text="Lista de ActivityInfo (descripción y código).",
                  style="Muted.TLabel").pack(anchor="w")
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
        hh.pack(fill="x")
        ttk.Label(hh, text="Se escribe en «Historia de la enfermedad actual» de APS.", style="Muted.TLabel").pack(
            side="left")
        ttk.Button(hh, text="Otra versión", command=lambda: self._regen_hea_aps(True)).pack(side="right")
        ttk.Label(f_hea, text="Una sola historia con los diagnósticos de APS (crónicos como antecedente, el agudo como cuadro "
                  "actual, los demás como síntomas); los que pasan a Salud Sexual y Reproductiva tienen su propia HEA allí. Revísela y corríjala con lo que el paciente refirió; si la edita a "
                  "mano, ya no se reemplaza sola.", style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        self.hea = tk.Text(f_hea, height=6, wrap="word", font=theme.FONT_TEXT, relief="solid", bd=1)
        self.hea.insert("1.0", defaults.get("hea", ""))
        self.hea.pack(fill="x")
        self.hea_aviso = ttk.Label(f_hea, text="", style="Muted.TLabel", wraplength=780, justify="left")
        self.hea_aviso.pack(anchor="w")
        ttk.Label(f_exa, text="Se escribe en «Examen Físico» de APS.", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(f_exa, text="Examen céfalo-caudal normal; cada sección cambia según los diagnósticos elegidos "
                  "(genitourinario solo si algún diagnóstico lo requiere). Puede corregir el texto; vacío = no se llena.", style="Muted.TLabel", wraplength=780,
                  justify="left").pack(anchor="w")
        ttk.Button(f_exa, text="Otra versión del examen", command=lambda: self._regen_examen(True)).pack(anchor="e")
        self.examen = tk.Text(f_exa, height=11, wrap="word", font=theme.FONT_TEXT, relief="solid", bd=1)
        self.examen.insert("1.0", defaults.get("examen_fisico", ""))
        self._exa_auto = defaults.get("examen_fisico", "")
        self.examen.pack(fill="x")
        ttk.Label(f_plan, text="Se escribe en «Plan» de APS.", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(f_plan, text="Medidas generales y signos de alarma según los diagnósticos. Los medicamentos se "
                  "agregan abajo, con su dosis. Puede corregir el texto; vacío = no se llena.", style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        self.plan = tk.Text(f_plan, height=8, wrap="word", font=theme.FONT_TEXT, relief="solid", bd=1)
        self.plan.insert("1.0", defaults.get("plan", ""))
        self._plan_auto = defaults.get("plan", "")
        ttk.Button(f_plan, text="Otra versión del plan", command=lambda: self._regen_plan(True, "aps")).pack(anchor="e")
        self.plan.pack(fill="x")
        self.meds_aps = med_picker.MedPicker(f_plan, defaults.get("meds_aps") or [])
        self.meds_aps.pack(fill="x", pady=(8, 0))
        ttk.Label(f_der, text="Derivación (hacia) y servicio brindado.", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(f_der, text="«¿Referencia Transfronteriza?» está siempre (por defecto No). Si elige Sí en «¿Va a ser derivado?» se "
                  "muestran los demás campos, como en ActivityInfo (recapitulativo interno de MdM). El servicio brindado "
                  "siempre es Salud.", style="Muted.TLabel",
                  wraplength=780, justify="left").pack(anchor="w")
        gf3 = ttk.Frame(f_der)
        gf3.pack(fill="x")
        g3 = widgets.FormGrid(gf3, 3)
        # como en la página: «¿A cuántos servicios se deriva?» y «Servicio brindado» solo aparecen con «¿Va a ser derivado?»
        # = Sí; «¿Referencia Transfronteriza?» está siempre (por defecto No), justo después de «¿Va a ser derivado?»
        self.der_n = ttk.Frame(f_der)
        gfn = ttk.Frame(self.der_n)
        gfn.pack(fill="x")
        gn = widgets.FormGrid(gfn, 3)
        self._der_transf = ttk.Frame(f_der)
        self._der_transf.pack(fill="x")
        gt = widgets.FormGrid(self._der_transf, 3)
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
        add3("n_servicios", "¿A cuántos servicios se deriva?", ai.N_SERVICIOS, gfn, gn)
        add3("transfronteriza", "¿Referencia Transfronteriza?", ai.VA_DERIVADO, self._der_transf, gt)
        if not self.w["transfronteriza"].get_value():
            self.w["transfronteriza"].set_value("No")
        add3("servicio_brindado", "Servicio brindado", ai.SERVICIOS_BRINDADOS, gf4, g4)
        add3("servicio_salud", "Salud (si el servicio es Salud)", ai.SERVICIOS_SALUD, gf4, g4)
        self.w["va_derivado"].bind("<<ComboboxSelected>>", lambda e: self._mostrar_derivacion())
        self._mostrar_derivacion()
        self._construir_ssr(defaults)
        self._hea_auto = defaults.get("hea", "")      # último texto generado: si la persona lo cambia, se respeta
        self._dx_vistos = self._clave_hea()
        self._vit_hta = self._hay_hta()          # con HTA los signos vitales proponen 140/130 y 90/80
        if defaults.get("_restaurado"):          # registro guardado: ningún texto se vuelve a generar solo
            for attr in ("_exa_auto", "_ssr_exa_auto", "_plan_auto", "_ssr_plan_auto", "_hea_auto", "_ssr_hea_auto"):
                setattr(self, attr, "\0")
        if self._exa_auto.strip() != examen_fisico.compose([], ssr=False).strip():
            self._exa_auto = "\0"        # texto puesto a mano desde fuera: no se pisa
        if self._ssr_exa_auto.strip() != examen_fisico.compose([], ssr=True).strip():
            self._ssr_exa_auto = "\0"
        for attr in ("_plan_auto", "_ssr_plan_auto"):
            if getattr(self, attr).strip() not in (ai.PLAN_BASE, ""):
                setattr(self, attr, "\0")        # texto puesto a mano desde fuera: no se pisa
        self._regen_examen()
        self._regen_plan()
        # si se corrige el género o la edad en esta ventana, la HEA se actualiza (salvo que ya la haya editado)
        self.w["genero"].bind("<<ComboboxSelected>>", lambda e: (self._ajustar_vitales(), self._regen_hea(True),
                                                                 self._ssr_condicionales()))
        self.w["edad"].bind("<FocusOut>", lambda e: (self._ajustar_vitales(), self._regen_hea(True)))
        self._marcar_fuentes()
        self._panel_paciente(sf)
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

    CLAVES = [("nombres", "Nombres"), ("apellidos", "Apellidos"), ("genero", "Género"),
              ("fecha", "Fecha de consulta"), ("edad", "Edad")] + list(ai.OBLIGATORIOS)
    NAV = [("datos", "Datos de la ficha"), ("hea", "HEA"), ("vit", "Signos vitales"), ("exa", "Examen físico"),
           ("dx", "Diagnósticos"), ("plan", "Plan"), ("der", "Derivación")]

    def _sec(self, parent, clave, titulo):
        sec = widgets.Seccion(parent, titulo)
        self.secciones[clave] = sec
        return sec.cuerpo

    def _panel_paciente(self, sf):
        """Panel fijo a la izquierda (no se desplaza): paciente, estado de cada sección y acceso directo a ellas."""
        self._sf = sf
        side = ttk.Frame(self, style="Card.TFrame", padding=(12, 12))
        side.pack(side="left", fill="y", padx=(10, 0), pady=10, before=sf)
        side.pack_propagate(False)
        ancho = int(200 * theme.FONT[1] / 11)
        side.configure(width=ancho)
        ttk.Label(side, text="PACIENTE", style="CardField.TLabel").pack(anchor="w")
        self._p_nombre = ttk.Label(side, style="Card.TLabel", font=theme.FONT_B, wraplength=ancho - 35, justify="left")
        self._p_nombre.pack(anchor="w", pady=(2, 6))
        self._p_edad = ttk.Label(side, style="Card.TLabel", wraplength=ancho - 35, justify="left")
        self._p_edad.pack(anchor="w")
        ttk.Separator(side).pack(fill="x", pady=8)
        ttk.Label(side, text="DIAGNÓSTICOS", style="CardField.TLabel").pack(anchor="w")
        self._p_dx = ttk.Label(side, style="Card.TLabel", wraplength=ancho - 35, justify="left")
        self._p_dx.pack(anchor="w", pady=(2, 0))
        self._p_alerta = ttk.Label(side, style="Card.TLabel", foreground=theme.WARN, wraplength=ancho - 35, justify="left")
        self._p_alerta.pack(anchor="w", pady=(6, 0))
        ttk.Separator(side).pack(fill="x", pady=8)
        ttk.Label(side, text="IR A", style="CardField.TLabel").pack(anchor="w")
        self._nav = {}
        for clave, nombre in self.NAV + [("ssr", "Salud sexual y reproductiva")]:
            lb = ttk.Label(side, text=nombre, style="NavItem.TLabel", cursor="hand2", wraplength=ancho - 35)
            lb.bind("<Button-1>", lambda e, c=clave: self._ir(c))
            self._nav[clave] = lb
            if clave != "ssr":
                lb.pack(anchor="w", pady=1)
        self._p_falta = ttk.Label(side, style="Card.TLabel", foreground=theme.DANGER, wraplength=ancho - 35, justify="left")
        self._p_falta.pack(anchor="w", pady=(8, 0))
        self.bind("<Control-Return>", lambda e: self._ok())
        self._refrescar_panel()

    def _ir(self, clave):
        """Despliega la sección y la lleva a la vista."""
        sec = self.secciones.get(clave)
        w = sec if sec is not None else None
        if w is None or (clave == "ssr" and not self.f_ssr.winfo_manager()):
            return
        if sec is not None:
            sec.abrir()
        self.update_idletasks()
        body = self._sf.body
        y = w.winfo_rooty() - body.winfo_rooty()
        self._sf.canvas.yview_moveto(max(0.0, y / max(1, body.winfo_height())))

    def _valor(self, k):
        try:
            return (self.w[k].get_value() or "").strip()
        except Exception:  # noqa: BLE001
            return ""

    def _faltantes(self):
        """[(sección, etiqueta, clave del campo o None)] de lo importante que está vacío."""
        out = [("datos", t, k) for k, t in self.CLAVES if not self._valor(k)]
        consultas = self.w["consultas"].get_value() if "consultas" in self.w else []
        if not consultas:
            out.append(("datos", "Consulta a realizar", None))
        elif ai.CONSULTA_APS in consultas:
            if not self._valor("tipo_consulta"):
                out.append(("datos", "Tipo de consulta (APS)", "tipo_consulta"))
            if not any(cat.from_label(cb.get_value())[0] for _a, cb in self.dx_rows):
                out.append(("dx", "Diagnóstico", None))
        return out

    def _texto(self, t):
        return t.get("1.0", "end").strip()

    def _refrescar_panel(self):
        try:
            nom = " ".join(x for x in (self._valor("nombres"), self._valor("apellidos")) if x)
            p = self._persona()
            sexo = {"M": "Mujer", "H": "Hombre"}.get(p.get("sexo"), self._valor("genero"))
            edad = self._valor("edad")
            u = "año" if edad == "1" else "años"
            self._p_nombre.configure(text=nom or "—")
            self._p_edad.configure(text=" · ".join(x for x in ((f"{edad} {u}" if edad else ""), sexo) if x) or "—")
            dx = [d for d in self._dx_hea() if d]
            self._p_dx.configure(text="\n".join("• " + d for d in dx) if dx else "—")
            anios = (float(edad) if (p.get("unidad") or "años").lower().startswith("a") else
                     float(edad) / 12 if (p.get("unidad") or "").lower().startswith("m") else float(edad) / 365) if edad.isdigit() else None
            al = coherencia.alertas(p.get("sexo"), anios, dx, self._valor("temperatura"))
            self._p_alerta.configure(text=("⚠ Revisar:\n" + "\n".join("• " + a for a in al)) if al else "")
            # lo importante que falta: campos en rojo, marca en cada sección y lista en el panel
            falt = self._faltantes()
            malos = {k for _s, _t, k in falt if k}
            for k, _t in self.CLAVES + [("tipo_consulta", "")]:
                w = self.w.get(k)
                if w is None:
                    continue
                combo = isinstance(w, ttk.Combobox)
                w.configure(style=("Bad." if k in malos else "") + ("TCombobox" if combo else "TEntry"))
            por_sec = {}
            for s_, _t, _k in falt:
                por_sec[s_] = por_sec.get(s_, 0) + 1
            vit = all(self._valor(k) for k in ("sistolica", "diastolica", "fc", "fr", "temperatura", "peso"))
            estado = {
                "datos": (not por_sec.get("datos"), f"faltan {por_sec.get('datos', 0)}"),
                "hea": (bool(self._texto(self.hea)), "vacía"),
                "vit": (vit, "incompletos"),
                "exa": (bool(self._texto(self.examen)), "vacío"),
                "dx": (not por_sec.get("dx"), "sin elegir"),
                "plan": (bool(self._texto(self.plan)), "vacío"),
                "der": (bool(self._valor("va_derivado")), "sin elegir"),
            }
            for clave, (ok, aviso) in estado.items():
                self.secciones[clave].marcar(True if ok else False, "listo" if ok else aviso)
                self._nav[clave].configure(text=("✓ " if ok else "● ") + dict(self.NAV)[clave],
                                           foreground=theme.OK if ok else theme.WARN)
            ssr_visible = bool(self.f_ssr.winfo_manager())
            if ssr_visible:
                self._nav["ssr"].pack(anchor="w", pady=1)
                self._nav["ssr"].configure(text="• Salud sexual y reproductiva", foreground=theme.TEXT)
            else:
                self._nav["ssr"].pack_forget()
            self._p_falta.configure(text=("Falta:\n" + "\n".join("• " + t for _s, t, _k in falt[:5])
                                          + ("\n…" if len(falt) > 5 else "")) if falt else "")
            self.after(700, self._refrescar_panel)
        except tk.TclError:          # la ventana ya se cerró
            pass
        except Exception:  # noqa: BLE001
            self.after(700, self._refrescar_panel)

    def _dx_actuales(self):
        # descripción elegida en la lista de ActivityInfo; si se dejó vacía, el texto del ATA (la HEA lo incluye igual)
        return [hea_banco.fuente_hea(a, cat.from_label(cb.get_value())[0]) for a, cb in self.dx_rows]

    def _ssr_activo(self):
        return hasattr(self, "ssr_rows") and "Salud Sexual y Reproductiva" in self.w["consultas"].get_value()

    def _dx_ssr(self):
        """Diagnósticos elegidos en la lista de SSR (solo si se marcó esa consulta)."""
        if not self._ssr_activo():
            return []
        out = []
        for cb in self.ssr_rows:
            d = ssr_cat.from_label(cb.get_value())[0] if hasattr(ssr_cat, "from_label") else cb.get_value()
            if d and d not in out:
                out.append(d)
        return out

    def _dx_ssr_hea(self):
        """Diagnósticos para la HEA de SSR: la lista de SSR no dice el método de PF («atención relativa a la
        anticoncepción»), así que mientras la fila siga siendo la sugerencia automática se usa el texto del ATA
        («PF (ACOs)») para que la HEA hable de ese método."""
        if not self._ssr_activo():
            return []
        sug = self.defaults.get("ssr_dx") or []
        out = []
        for i, cb in enumerate(self.ssr_rows):
            d = ssr_cat.from_label(cb.get_value())[0] if hasattr(ssr_cat, "from_label") else cb.get_value()
            if not d:
                continue
            abrev = self.dx_rows[i][0] if i < len(self.dx_rows) else ""
            auto = i < len(sug) and (sug[i].get("descripcion") or "") == d
            t = hea_banco.fuente_hea_ssr(abrev, d, auto)
            if t not in out:
                out.append(t)
        return out

    def _dx_hea(self):
        """Todos los diagnósticos (APS y SSR): de ellos sale el examen físico, que es el mismo en ambas fichas."""
        dxs = list(self._dx_actuales())
        for d in self._dx_ssr():
            if d not in dxs:
                dxs.append(d)
        return dxs

    def _dx_aps_hea(self):
        """Diagnósticos de la HEA de APS: los del ATA que NO pasaron a SSR (cada renglón de SSR corresponde al
        diagnóstico del ATA del mismo número). Si todos pasaron a SSR, se usan todos para no dejar la HEA vacía."""
        todos = self._dx_actuales()
        if not hasattr(self, "ssr_rows"):
            return todos
        # los diagnósticos que pasan a SSR no entran en la HEA de APS, esté o no marcada la consulta de SSR
        # (igual que al abrir la ventana); si no, «Otra versión» los volvía a meter
        a_ssr = {i for i, cb in enumerate(self.ssr_rows) if ssr_cat.from_label(cb.get_value())[0]}
        aps = [d for i, d in enumerate(todos) if i not in a_ssr]
        return aps if any(aps) else todos

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
        f = self.ssr_sec.cuerpo
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
            t = tk.Text(f, height=alto, wrap="word", font=theme.FONT_TEXT, relief="solid", bd=1)
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
        nota("Es distinta de la HEA de Atención primaria: sale solo de los diagnósticos de SSR de la lista de abajo (se rehace al "
             "cambiarlos, mientras no la edite aquí). Corríjala si hace falta; vacío = no se llena.")
        bh = ttk.Frame(f)
        bh.pack(fill="x")
        ttk.Button(bh, text="Otra versión de la HEA (SSR)", command=lambda: self._regen_hea_ssr(True)).pack(side="right")
        _h0 = defaults.get("ssr_hea", defaults.get("hea", ""))
        self.ssr_hea = caja("HEA", 6, _h0)
        self._ssr_hea_auto = _h0
        self.ssr_hea_aviso = ttk.Label(f, text="", style="Muted.TLabel", wraplength=780, justify="left")
        self.ssr_hea_aviso.pack(anchor="w")

        titulo("Antecedentes")
        self.ssr_app = ttk.Frame(f)       # ancla (sin contenido) para colocar los campos de ficha larga
        self.ssr_app.pack()
        self.ssr_larga = ttk.Frame(f)           # solo con ficha «Larga»; según el género salen unos u otros, como en la página
        self._ssr_larga_mujer = ttk.Frame(self.ssr_larga)
        gm_ = widgets.FormGrid(self._ssr_larga_mujer, 3)
        entry("ssr_menarquia", "Menarquía (edad en años, 9 a 20)", self._ssr_larga_mujer, gm_)
        combo("ssr_ritmo", "Ritmo menstrual", ai.SSR_RITMOS, self._ssr_larga_mujer, gm_)
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
            combo("ssr_" + k, lab, ai.SSR_NUMEROS, self.ssr_ant_obst, gq)
        combo("ssr_lactancia", "Lactancia materna (en ActivityInfo solo sale si Hijos vivos ≥ 1)", ai.SI_NO, self.ssr_ant_obst, gq)
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
        nota("Es el mismo examen físico de Atención primaria (se copia solo mientras no lo edite aquí). Puede corregirlo; vacío = no se llena.")
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
        # Lista de verificación de embarazo (en la ventana va debajo del método elegido; en ActivityInfo se llena en su orden)
        self.ssr_lve = ttk.LabelFrame(self.ssr_met, text=" Lista de verificación de embarazo ", padding=8)
        ttk.Label(self.ssr_lve, text="Solo para Mujer CIS u Hombre TRANS. Si TODAS son «No» no se puede descartar embarazo; "
                  "con alguna «Sí» se puede estar razonablemente seguro/a. Vacío = no se llena.", style="Muted.TLabel",
                  wraplength=740, justify="left").pack(anchor="w")
        glv = ttk.Frame(self.ssr_lve)
        glv.pack(fill="x")
        grlv = widgets.FormGrid(glv, 2)
        for k, _rot, preg in ai.LVE_PREGUNTAS:
            combo("ssr_lve_" + k, preg, ai.SI_NO, glv, grlv)
            self.w["ssr_lve_" + k].bind("<<ComboboxSelected>>", lambda e: self._lve_actualizar())
        fb = ttk.Frame(self.ssr_lve)
        fb.pack(fill="x", pady=(4, 0))
        ttk.Button(fb, text="Todas «No»", command=lambda: self._lve_todas("No")).pack(side="left")
        ttk.Button(fb, text="Limpiar", command=lambda: self._lve_todas("")).pack(side="left", padx=6)
        self.ssr_lve_res = ttk.Label(self.ssr_lve, text="", wraplength=740, justify="left")
        self.ssr_lve_res.pack(anchor="w", pady=(4, 0))
        marco_e = ttk.LabelFrame(self.ssr_met, text=" 2) Método ELEGIDO HOY (después de la consejería) ", padding=8)
        marco_e.pack(fill="x", pady=(8, 0))
        self._ssr_marco_e = marco_e
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
        nota("Medidas generales según los diagnósticos de SSR (distintas a las del plan de Atención primaria); los medicamentos "
             "se agregan abajo, con su dosis. Vacío = no se llena.")
        bp = ttk.Frame(f)
        bp.pack(fill="x")
        ttk.Button(bp, text="Otra versión del plan (SSR)", command=lambda: self._regen_plan(True, "ssr")).pack(side="right")
        self.ssr_plan = caja("Plan", 7, defaults.get("ssr_plan", defaults.get("plan", "")))
        self._ssr_plan_auto = defaults.get("ssr_plan", defaults.get("plan", ""))
        self.meds_ssr = med_picker.MedPicker(f, defaults.get("meds_ssr") or [])
        self.meds_ssr.pack(fill="x", pady=(8, 0))

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
        self.ssr_lve.pack_forget()
        if self._lve_aplica():
            self.ssr_lve.pack(fill="x", after=self._ssr_marco_e, pady=(8, 0))   # en la ventana va debajo del método elegido
        self._lve_actualizar()

    def _lve_aplica(self):
        return (self.w["ssr_consejeria"].get_value() == "Si" and self.w["genero"].get_value() in ai.LVE_GENEROS)

    def _lve_respuestas(self):
        return {k: self.w["ssr_lve_" + k].get_value() for k, _, _ in ai.LVE_PREGUNTAS}

    def _lve_todas(self, v):
        for k, _, _ in ai.LVE_PREGUNTAS:
            self.w["ssr_lve_" + k].set_value(v)
        self._lve_actualizar()

    def _lve_actualizar(self):
        r = ai.lve_resultado(self._lve_respuestas())
        self.ssr_lve_res.configure(text=("Resultado: " + r) if r else "Resultado: (responda las preguntas)",
                                   foreground="#b54708" if r.startswith("No se puede") else "")

    def _mostrar_derivado_desde(self):
        """«Derivación (desde)»: Procedencia, observaciones y código solo existen en la página si «¿Ha sido derivado/a?» es Sí."""
        si = self.w["derivado"].get_value() == "Sí"
        for k, cosas in self._der_desde.items():
            if not si:
                self.w[k].set_value("")
            for c in cosas:
                c.grid() if si else c.grid_remove()

    def _mostrar_disc(self):
        """El tipo de discapacidad solo se pide (y se llena en ActivityInfo) cuando la respuesta es «Sí»."""
        cosas = [self._disc_tipo] + list(self._disc_lbl)
        if self.w["discapacidad"].get_value() == "Sí":
            for c in cosas:
                c.grid()
        else:
            self._disc_tipo.set_value([])
            for c in cosas:
                c.grid_remove()

    def _mostrar_ssr_der(self):
        self.ssr_der_extra.pack_forget()
        self.ssr_f_victima.pack_forget()
        if self.w["ssr_va_derivado"].get_value() == "Sí":
            self.ssr_der_extra.pack(fill="x", after=self.w["ssr_va_derivado"].master)
        self.ssr_f_victima.pack(fill="x", pady=(6, 0))

    def _sync_ssr_exa(self):
        """El examen físico de SSR es el mismo de APS: copia el de APS mientras la persona no lo haya editado aquí."""
        actual = self.ssr_examen.get("1.0", "end").strip()
        if actual == self._ssr_exa_auto.strip():
            nuevo = self.examen.get("1.0", "end").strip()
            self.ssr_examen.delete("1.0", "end")
            self.ssr_examen.insert("1.0", nuevo)
            self._ssr_exa_auto = nuevo

    def _mostrar_ssr(self):
        if "Salud Sexual y Reproductiva" in self.w["consultas"].get_value():
            self.f_ssr.pack(fill="x")
            self._regen_hea(True)
            self._regen_hea_ssr(False)
        else:
            self.f_ssr.pack_forget()
            if hasattr(self, "_dx_vistos"):          # (no durante la construcción de la ventana)
                self._regen_examen()

    def _mostrar_derivacion(self):
        """«Servicio brindado» y lo demás solo existen en la página cuando «¿Va a ser derivado?» es Sí."""
        if self.w["va_derivado"].get_value() == "Sí":
            self.der_n.pack(fill="x", before=self._der_transf)
            self.der_extra.pack(fill="x")
        else:
            self.der_n.pack_forget()
            self.der_extra.pack_forget()

    def _hay_hta(self):
        return any(ai.es_hta(d) for d in self._dx_actuales() if d)

    def _ajustar_vitales(self):
        """Si cambian el género o la edad a otra franja (p. ej. de lactante a escolar), o se agrega/quita un diagnóstico de
        HTA, se proponen de nuevo los signos vitales, solo en los campos que la persona no había cambiado."""
        p = self._persona()
        grupo = ai.grupo_vitales(p.get("sexo"), p.get("edad"), p.get("unidad", "años"))
        hta = self._hay_hta()
        if grupo == self._vit_grupo and hta == getattr(self, "_vit_hta", hta):
            return
        self._vit_grupo = grupo
        self._vit_hta = hta
        nuevo = ai.vitales_defecto(p.get("sexo"), p.get("edad"), p.get("unidad", "años"), hta=hta)
        for k in ("sistolica", "diastolica", "fc", "fr"):
            if self.w[k].get_value() == self._vit_auto.get(k):
                self.w[k].set_value(nuevo[k])
                self._vit_auto[k] = nuevo[k]

    def _ajustar_social(self):
        """Si la edad cambia de menor a mayor de 18 años (o al revés), estado civil, escolaridad y sector de ocupación se
        proponen de nuevo, solo en los campos que la persona no había cambiado."""
        if self._restaurado or not hasattr(self, "_soc_menor"):
            return
        p = self._persona()
        menor = ai.es_menor_de_edad(p.get("edad"), p.get("unidad", "años"))
        if menor == self._soc_menor:
            return
        self._soc_menor = menor
        nuevo = ai.defectos_ficha(menor=menor)
        for k in ("estado_civil", "escolaridad", "ocupacion"):
            if self.w[k].get_value() == self._soc_auto.get(k):
                self.w[k].set_value(nuevo[k])
                self._soc_auto[k] = nuevo[k]

    def _clave_hea(self):
        p = self._persona()
        return (tuple(self._dx_aps_hea()), tuple(self._dx_ssr()), p.get("sexo"), p.get("edad"), p.get("unidad"))

    def _regen_plan(self, forzar=False, cual=None):
        """Plan general (sin medicamentos) según los diagnósticos; si se editó a mano, no se pisa (salvo «Otra versión»).
        El plan de APS usa los diagnósticos de APS y el de SSR los de SSR (cada uno con sus propias frases).
        cual: "aps" o "ssr" para cambiar solo uno; None = los dos."""
        if self._restaurado and not forzar:          # registro guardado: los textos se dejan como estaban
            return
        def poner(caja, texto, auto_attr):
            if not texto:
                return
            actual = caja.get("1.0", "end").strip()
            if not forzar and actual not in ("", ai.PLAN_BASE, getattr(self, auto_attr, "").strip()):
                return
            caja.delete("1.0", "end")
            caja.insert("1.0", texto)
            setattr(self, auto_attr, texto)
        rng = random.Random()
        if cual in (None, "aps"):
            poner(self.plan, plan_banco.compose([d for d in self._dx_aps_hea() if d], rng=rng), "_plan_auto")
        if cual in (None, "ssr") and hasattr(self, "ssr_plan"):
            cuerpo = plan_banco.compose([d for d in (self._dx_ssr() or self._dx_hea()) if d], rng=rng, ssr=True)
            poner(self.ssr_plan, (ai.PLAN_SSR_INICIO + " " + cuerpo).strip(), "_ssr_plan_auto")

    def _regen_examen(self, forzar=False):
        """Examen físico por secciones según los diagnósticos; si se editó a mano, no se pisa (salvo «Otra versión»)."""
        if self._restaurado and not forzar:          # registro guardado: los textos se dejan como estaban
            return
        def poner(caja, texto, auto_attr):
            if not forzar and caja.get("1.0", "end").strip() != getattr(self, auto_attr, "").strip():
                return
            caja.delete("1.0", "end")
            caja.insert("1.0", texto)
            setattr(self, auto_attr, texto)
        aps = [d for d in self._dx_actuales() if d]
        todos = [d for d in self._dx_hea() if d]
        ata = [a for a, _cb in self.dx_rows]          # lo que dice el ATA: ahí se ve si una crónica está en crisis
        rng = random.Random()
        if self._ssr_activo() and hasattr(self, "ssr_examen"):
            # con SSR marcado, el examen físico es UNO SOLO (todos los diagnósticos, con genitourinario) y va igual en ambas fichas
            texto = examen_fisico.compose(todos, ssr=True, rng=rng, ata=ata)
            poner(self.examen, texto, "_exa_auto")
            poner(self.ssr_examen, texto, "_ssr_exa_auto")
        else:
            poner(self.examen, examen_fisico.compose(aps, ssr=False, rng=rng, ata=ata), "_exa_auto")
            if hasattr(self, "ssr_examen"):
                poner(self.ssr_examen, examen_fisico.compose(todos, ssr=True, rng=rng, ata=ata), "_ssr_exa_auto")

    def _regen_hea(self, solo_si_cambio):
        """Vuelve a armar la HEA de APS (diagnósticos de APS) y la de SSR (diagnósticos de SSR). Si la persona editó
        un texto a mano, ese no se pisa (salvo con «Otra versión»)."""
        if not hasattr(self, "_dx_vistos"):        # todavía se está armando la ventana
            return
        self._marcar_fuentes()
        self._ajustar_vitales()
        self._ajustar_social()
        self._regen_examen()
        self._regen_plan()
        if solo_si_cambio:
            clave = self._clave_hea()
            if clave == self._dx_vistos:
                return
            self._dx_vistos = clave
        self._regen_hea_aps(not solo_si_cambio)
        self._regen_hea_ssr(not solo_si_cambio)

    def _regen_hea_aps(self, forzar):
        if self._restaurado and not forzar:          # registro guardado: los textos se dejan como estaban
            return
        if not forzar and self.hea.get("1.0", "end").strip() != self._hea_auto.strip():
            return
        p = self._persona()
        texto, avisos = hea_banco.compose(p.get("sexo"), p.get("edad"), [d for d in self._dx_aps_hea() if d], p.get("unidad", "años"))
        self.hea.delete("1.0", "end")
        self.hea.insert("1.0", texto)
        self._hea_auto = texto
        self.hea_aviso.configure(text="\n".join("⚠ " + a for a in avisos))

    def _regen_hea_ssr(self, forzar):
        if self._restaurado and not forzar:          # registro guardado: los textos se dejan como estaban
            return
        if not self._ssr_activo() or not hasattr(self, "ssr_hea"):
            return
        dxs = self._dx_ssr_hea()
        if not dxs:
            return
        if not forzar and self.ssr_hea.get("1.0", "end").strip() != self._ssr_hea_auto.strip():
            return
        p = self._persona()
        texto, avisos = hea_banco.compose(p.get("sexo"), p.get("edad"), dxs, p.get("unidad", "años"))
        self.ssr_hea.delete("1.0", "end")
        self.ssr_hea.insert("1.0", texto)
        self._ssr_hea_auto = texto
        self.ssr_hea_aviso.configure(text="\n".join("⚠ " + a for a in avisos))

    def run(self):                      # ya tiene tamaño y posición propios (900 x 700, centrada)
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.wait_window(self)
        return self.result

    def snapshot(self):
        """Todo lo que hay en la ventana, en el mismo formato de `defaults`, para volver a abrirla igual."""
        s = {k: w.get_value() for k, w in self.w.items()}
        txt = lambda c: c.get("1.0", "end").strip()  # noqa: E731
        s.update(hea=txt(self.hea), examen_fisico=txt(self.examen), plan=txt(self.plan), meds_aps=self.meds_aps.valores())
        if hasattr(self, "ssr_hea"):
            s.update(ssr_hea=txt(self.ssr_hea), ssr_examen_fisico=txt(self.ssr_examen), ssr_plan=txt(self.ssr_plan),
                     meds_ssr=self.meds_ssr.valores())
        s["dx"] = [{"abrev": a, "descripcion": cb.get_value(), "cie11": ""} for a, cb in self.dx_rows]
        if hasattr(self, "ssr_rows"):
            sug = self.defaults.get("ssr_dx") or []
            s["ssr_dx"] = [{"abrev": (sug[i].get("abrev", "") if i < len(sug) else ""),
                            "descripcion": ssr_cat.from_label(cb.get_value())[0], "cie11": ""}
                           for i, cb in enumerate(self.ssr_rows)]
        return s

    def _ok(self):
        data = {k: (w.get_value() if isinstance(w, ChecksField) else w.get_value().strip())
                for k, w in self.w.items()}
        if not data["consultas"]:
            dialogs.info(self, "Marque al menos una consulta a realizar.")
            return
        falta = [t for k, t in self.CLAVES if not data.get(k)]
        if "Atención Primaria de Salud" in data["consultas"] and not data.get("tipo_consulta"):
            falta.append("Tipo de consulta (APS)")
        if data.get("discapacidad") == "Sí" and not data.get("discapacidad_tipo"):
            falta.append("¿Qué tipo de discapacidad?")
        if ai.CONSULTA_APS in data["consultas"] and not any(cat.from_label(cb.get_value())[0] for _a, cb in self.dx_rows):
            falta.append("Diagnóstico (ninguno elegido de la lista)")
        if falta and not dialogs.confirm(
                self, "Faltan datos obligatorios", "Estos campos obligatorios están vacíos y quedarán sin llenar "
                "en ActivityInfo:\n\n" + "\n".join(f"• {t}" for t in falta) + "\n\n¿Abrir Chrome de todos modos?",
                yes="Abrir de todos modos", no="Volver y elegir"):
            self._ir("datos" if any(s_ == "datos" for s_, _t, _k in self._faltantes()) else "dx")
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
            self._sync_ssr_exa()
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
        data["plan"] = medicamentos.agregar_al_plan(self.plan.get("1.0", "end"), self.meds_aps.valores())
        if data.get("va_derivado") != "Sí":       # sin Sí no existen esos campos en la página
            for k in ("n_servicios", "servicio_brindado", "servicio_salud"):
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
                           "lve": ({k: v for k, v in self._lve_respuestas().items() if v} if self._lve_aplica() else {}),
                           "plan": medicamentos.agregar_al_plan(self.ssr_plan.get("1.0", "end"), self.meds_ssr.valores()),
                           "va_derivado": W("ssr_va_derivado"), "victima_sexual": W("ssr_victima_sexual")}
            if data["ssr"]["va_derivado"] == "Sí":
                data["ssr"].update({"transfronteriza": self.w["ssr_transfronteriza"].get_value(),
                                    "servicio_brindado": self.w["ssr_servicio_brindado"].get_value(),
                                    "servicio_salud": self.w["ssr_servicio_salud"].get_value()})
        self.result = data
        try:
            self.snap = self.snapshot()
        except Exception:  # noqa: BLE001  (guardar el registro nunca debe impedir llenar el formulario)
            self.snap = None
        self.destroy()
