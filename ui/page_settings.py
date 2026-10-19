"""Configuración: operador y contraseña."""
from tkinter import ttk

import security
from services import activityinfo as ai
from ui import dialogs, widgets
from ui.page import Page


class SettingsPage(Page):
    nav_key = "settings"

    def __init__(self, app):
        super().__init__(app)
        ttk.Label(self, text="Configuración", style="H1.TLabel").pack(anchor="w")
        sf = widgets.ScrollFrame(self)
        sf.pack(fill="both", expand=True, pady=(6, 0))
        body = sf.body

        s1 = widgets.section(body, "Operador")
        g = widgets.FormGrid(s1, 2)
        self.f = {}
        for key, label in (("operador", "Nombre de quien registra (aparece en el historial de cambios)"),):
            self.f[key] = widgets.EntryField(s1)
            g.add(label, self.f[key])
        row = ttk.Frame(s1)
        ttk.Button(row, text="Guardar", style="Accent.TButton", command=self.save_header).pack(side="left")
        self.h_status = ttk.Label(row, text="", style="Saved.TLabel")
        self.h_status.pack(side="left", padx=10)
        g.full(row, pady=(12, 0))

        s2 = widgets.section(body, "ActivityInfo: valores fijos")
        g2 = widgets.FormGrid(s2, 2)
        self.ai = {}
        for key, label, _d in ai.SETTINGS:
            self.ai[key] = widgets.EntryField(s2)
            g2.add(label, self.ai[key])
        row2 = ttk.Frame(s2)
        ttk.Button(row2, text="Guardar", style="Accent.TButton", command=self.save_ai).pack(side="left")
        self.ai_status = ttk.Label(row2, text="", style="Saved.TLabel")
        self.ai_status.pack(side="left", padx=10)
        g2.full(row2, pady=(12, 0))

        s4 = widgets.section(body, "Equivalencias CIE-11 (abreviatura del ATA → diagnóstico y código)")
        ttk.Label(s4, text="Escriba cada abreviatura tal como aparece en el ATA (HTA, ITU, RC…) y el "
                  "diagnóstico y código CIE-11 que usted decide usar. El programa no inventa códigos.",
                  style="Hint.TLabel", wraplength=900, justify="left").pack(anchor="w")
        frame, self.dx_tree = widgets.make_tree(s4, [("a", "Abreviatura", 120), ("d", "Descripción CIE-11", 380),
                                                     ("c", "Código CIE-11", 120)], height=6)
        frame.pack(fill="x", pady=(6, 6))
        self.dx_tree.bind("<<TreeviewSelect>>", lambda e: self._dx_pick())
        r3 = ttk.Frame(s4)
        r3.pack(fill="x")
        self.dx_a = widgets.EntryField(r3, width=12)
        self.dx_d = widgets.EntryField(r3, width=42)
        self.dx_c = widgets.EntryField(r3, width=12)
        for lbl, w in (("Abreviatura", self.dx_a), ("Descripción", self.dx_d), ("Código", self.dx_c)):
            ttk.Label(r3, text=lbl, style="Muted.TLabel").pack(side="left", padx=(0, 4))
            w.pack(side="left", padx=(0, 10))
        ttk.Button(r3, text="Guardar equivalencia", style="Accent.TButton", command=self.save_dx).pack(side="left")
        ttk.Button(r3, text="Quitar", style="Danger.TButton", command=self.remove_dx).pack(side="left", padx=8)

        s3 = widgets.section(body, "Seguridad: contraseña de acceso")
        self.pw_lbl = ttk.Label(s3, text="")
        self.pw_lbl.pack(anchor="w")
        row = ttk.Frame(s3)
        row.pack(anchor="w", pady=(8, 0))
        self.btn_set = ttk.Button(row, text="Establecer contraseña", style="Accent.TButton",
                                  command=self.set_password)
        self.btn_set.pack(side="left")
        self.btn_rm = ttk.Button(row, text="Quitar contraseña", style="Danger.TButton",
                                 command=self.remove_password)
        self.btn_rm.pack(side="left", padx=8)
        ttk.Label(s3, text="La contraseña se guarda cifrada (PBKDF2). Si la olvida no hay forma de "
                  "recuperarla: anótela en un lugar seguro.", style="Hint.TLabel",
                  wraplength=900, justify="left").pack(anchor="w", pady=(6, 0))

    def on_show(self, **kw):
        self.refresh()

    def refresh(self):
        vals = ai.get_setting_values(self.db)
        for k, w in self.ai.items():
            w.set_value(vals.get(k, ""))
        self._load_dx()
        self.ai_status.configure(text="")
        for k, w in self.f.items():
            w.set_value(self.db.get_setting(k, ""))
        self._pw_state()
        self.h_status.configure(text="")

    def save_header(self):
        for k, w in self.f.items():
            self.db.set_setting(k, w.get_value().strip())
        self.h_status.configure(text="Configuración guardada.")

    # -- ActivityInfo ---------------------------------------------------------
    def save_ai(self):
        for k, w in self.ai.items():
            self.db.set_setting(k, w.get_value().strip())
        self.ai_status.configure(text="Guardado.")

    def _load_dx(self):
        widgets.fill_tree(self.dx_tree, [(r["abrev"], (r["abrev"], r["descripcion"], r["cie11"]))
                                         for r in ai.list_dx_map(self.db)])

    def _dx_pick(self):
        iid = widgets.selected_iid(self.dx_tree)
        if iid:
            v = self.dx_tree.item(iid, "values")
            self.dx_a.set_value(v[0])
            self.dx_d.set_value(v[1])
            self.dx_c.set_value(v[2])

    def save_dx(self):
        try:
            ai.save_dx_map(self.db, self.dx_a.get_value(), self.dx_d.get_value(), self.dx_c.get_value())
        except ValueError as exc:
            dialogs.info(self, str(exc))
            return
        for w in (self.dx_a, self.dx_d, self.dx_c):
            w.set_value("")
        self._load_dx()

    def remove_dx(self):
        iid = widgets.selected_iid(self.dx_tree)
        if iid:
            ai.delete_dx_map(self.db, iid)
            self._load_dx()

    # -- contraseña -----------------------------------------------------------
    def _pw_state(self):
        has = bool(self.db.get_setting("password_hash", ""))
        self.pw_lbl.configure(text="El programa está PROTEGIDO con contraseña." if has
                              else "El programa no tiene contraseña (cualquiera con acceso a la "
                                   "computadora puede abrirlo).")
        self.btn_set.configure(text="Cambiar contraseña" if has else "Establecer contraseña")
        self.btn_rm.state(["!disabled"] if has else ["disabled"])

    def _verify_current(self):
        stored = self.db.get_setting("password_hash", "")
        if not stored:
            return True
        pw = dialogs.ask_password(self, "Contraseña actual", "Escriba la contraseña actual:")
        if pw is None:
            return False
        if not security.verify_password(pw, stored):
            dialogs.error(self, "Contraseña incorrecta.")
            return False
        return True

    def set_password(self):
        if not self._verify_current():
            return
        pw = dialogs.ask_password(self, "Nueva contraseña", "Escriba la nueva contraseña:",
                                  confirm_twice=True)
        if pw:
            self.db.set_setting("password_hash", security.hash_password(pw))
            self._pw_state()
            dialogs.info(self, "Contraseña guardada. Se pedirá al abrir el programa.")

    def remove_password(self):
        if not self._verify_current():
            return
        self.db.set_setting("password_hash", "")
        self._pw_state()
        dialogs.info(self, "Se quitó la contraseña.")
