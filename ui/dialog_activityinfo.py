"""Ventana de revisión antes de llenar ActivityInfo: la persona confirma o corrige cada dato."""
import tkinter as tk
from tkinter import ttk

from services import activityinfo as ai
from ui import dialogs, theme, widgets
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
    def __init__(self, parent, defaults: dict, title="Añadir registro en ActivityInfo"):
        super().__init__(parent, title)
        self.defaults = defaults
        self.w = {}
        body = ttk.Frame(self, padding=(18, 14, 18, 8))
        body.pack(fill="both", expand=True)
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
        add("lugar", "Lugar de atención", E())
        add("nacionalidad", "País de nacionalidad", E())
        add("idioma", "Idioma", E())
        add("consultas", "Consulta a realizar (puede marcar más de una)", ChecksField(gf, ai.CONSULTAS), span=3)
        add("profesional", "Profesional que atiende (APS)", E())
        add("tipo_consulta", "Tipo de consulta (APS)", C(ai.TIPOS_CONSULTA))

        dxs = defaults.get("dx") or []
        ttk.Label(body, text="Diagnósticos del ATA (se anota la cantidad; el diagnóstico CIE-11 "
                  "se elige a mano en ActivityInfo)", style="H2.TLabel").pack(anchor="w", pady=(10, 2))
        if dxs:
            for i, d in enumerate(dxs, 1):
                cie = f"{d['descripcion']} · {d['cie11']}" if d["descripcion"] or d["cie11"] else \
                    "(sin equivalencia: agréguela en Configuración → Equivalencias CIE-11)"
                ttk.Label(body, text=f"{i}. {d['abrev']}  →  {cie}", wraplength=760, justify="left").pack(
                    anchor="w")
        else:
            ttk.Label(body, text="El ATA no trae diagnósticos para este paciente.",
                      style="Muted.TLabel").pack(anchor="w")
        bar = ttk.Frame(body)
        bar.pack(fill="x", pady=(14, 0))
        ttk.Button(bar, text="Cancelar", command=self.cancel).pack(side="right")
        ttk.Button(bar, text="Abrir Chrome y llenar", style="Accent.TButton", command=self._ok).pack(
            side="right", padx=8)

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
        data["tiene_fecha_nac"] = "No"  # siempre se usa la edad
        data["dx"] = self.defaults.get("dx") or []
        self.result = data
        self.destroy()
