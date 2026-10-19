"""Ventana de revisión antes de llenar ActivityInfo: la persona confirma o corrige cada dato."""
import tkinter as tk
from tkinter import ttk

from services import activityinfo as ai
from services import cie11_catalog as cat
from services import hea_banco
from ui import dialogs, widgets
from ui.dialogs import _Modal


class ChecksField(ttk.Frame):
    """Varias opciones marcables a la vez (por ejemplo, las consultas a realizar)."""

    def __init__(self, parent, options, columns=2):
        super().__init__(parent)
        self.vars = {}
        for i, opt in enumerate(options):
            v = tk.BooleanVar(value=False)
            self.vars[opt] = v
            ttk.Checkbutton(self, text=opt, variable=v).grid(row=i // columns, column=i % columns,
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
        add("consultas", "Consulta a realizar (puede marcar más de una)", ChecksField(gf, ai.CONSULTAS), span=3)
        add("profesional", "Profesional que atiende (APS)", E())
        add("tipo_consulta", "Tipo de consulta (APS)", C(ai.TIPOS_CONSULTA))
        V = lambda vals: widgets.ComboField(gf, [""] + list(vals), readonly=False, width=26)  # noqa: E731
        add("sistolica", "Sistólica (mayor) mmHg", V(ai.LISTA_SISTOLICA))
        add("diastolica", "Diastólica (menor) mmHg", V(ai.LISTA_DIASTOLICA))
        add("fc", "Frecuencia cardiaca o pulso (latidos/min)", V(ai.LISTA_FC))
        add("fr", "Frecuencia respiratoria (resp/min) — en niños, elíjala", V(ai.LISTA_FR))
        add("temperatura", "Temperatura (ºC)", V(ai.LISTA_TEMP))
        add("peso", "Peso (kg) — escríbalo; vacío = no se llena", E())
        add("examen_fisico", "Examen físico (por ahora solo «Cefalo-caudal»)", widgets.EntryField(gf, width=26))
        self._vit_auto = {k: self.w[k].get_value() for k in ("diastolica", "fr")}

        dxs = defaults.get("dx") or []
        ttk.Label(body, text="Diagnósticos — lista de ActivityInfo (descripción y código)",
                  style="H2.TLabel").pack(anchor="w", pady=(10, 2))
        self.dx_rows = []
        self.dx_tags = []
        labels = [cat.label(d) for d in cat.descriptions()]
        self._labels = labels
        if dxs:
            for i, d in enumerate(dxs):
                row = ttk.Frame(body)
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
                tag = ttk.Label(body, text="", style="Muted.TLabel")
                tag.pack(anchor="w", padx=(170, 0))
                self.dx_tags.append(tag)
                self.dx_rows.append((d["abrev"], cb))
            ttk.Label(body, text="Elija en la lista de ActivityInfo (puede escribir para buscar). Al elegir la "
                      "descripción, ActivityInfo pone el código solo. Si uno no está en la lista, déjelo vacío: no se llena en "
                      "ActivityInfo, pero la HEA sí lo incluye (vea «HEA usa» debajo de cada uno).",
                      style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
            self.recordar = tk.BooleanVar(value=True)
            ttk.Checkbutton(body, text="Recordar estas equivalencias para los próximos pacientes",
                            variable=self.recordar).pack(anchor="w")
        else:
            self.recordar = tk.BooleanVar(value=False)
            ttk.Label(body, text="El ATA no trae diagnósticos para este paciente.",
                      style="Muted.TLabel").pack(anchor="w")
        hh = ttk.Frame(body)
        hh.pack(fill="x", pady=(10, 2))
        ttk.Label(hh, text="HEA — se escribe en «Historia de la enfermedad actual» de APS", style="H2.TLabel").pack(
            side="left")
        ttk.Button(hh, text="Otra versión", command=lambda: self._regen_hea(False)).pack(side="right")
        ttk.Label(body, text="Una sola historia con los diagnósticos elegidos (crónicos como antecedente, el agudo como cuadro "
                  "actual, los demás como síntomas). Revísela y corríjala con lo que el paciente refirió; si la edita a "
                  "mano, ya no se reemplaza sola.", style="Muted.TLabel", wraplength=780, justify="left").pack(anchor="w")
        self.hea = tk.Text(body, height=6, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1)
        self.hea.insert("1.0", defaults.get("hea", ""))
        self.hea.pack(fill="x")
        self.hea_aviso = ttk.Label(body, text="", style="Muted.TLabel", wraplength=780, justify="left")
        self.hea_aviso.pack(anchor="w")
        self._hea_auto = defaults.get("hea", "")      # último texto generado: si la persona lo cambia, se respeta
        self._dx_vistos = self._clave_hea()
        # si se corrige el género o la edad en esta ventana, la HEA se actualiza (salvo que ya la haya editado)
        self.w["genero"].bind("<<ComboboxSelected>>", lambda e: (self._ajustar_vitales(), self._regen_hea(True)))
        self.w["edad"].bind("<FocusOut>", lambda e: (self._ajustar_vitales(), self._regen_hea(True)))
        self._marcar_fuentes()
        ttk.Button(bar, text="Cancelar", command=self.cancel).pack(side="right")
        ttk.Button(bar, text="Abrir Chrome y llenar", style="Accent.TButton", command=self._ok).pack(
            side="right", padx=8)

    def _filtrar(self, cb, event):
        """Al escribir en un diagnóstico, la lista desplegable muestra solo las opciones que contienen ese texto."""
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        q = cat.plain(cb.get_value())
        cb.set_values([x for x in self._labels if q in cat.plain(x)] or self._labels if q else self._labels)

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
        data["hea"] = self.hea.get("1.0", "end").strip()
        data["tiene_fecha_nac"] = "No"  # siempre se usa la edad
        self.result = data
        self.destroy()
