"""Configuración: encabezado de los documentos, listas configurables y contraseña."""
import tkinter as tk
from tkinter import ttk

import security
from ui import dialogs, theme, widgets
from ui.page import Page

CATALOGS = [
    ("estado_migratorio", "Estados migratorios"),
    ("categoria_ssr", "Categorías de atención SSR"),
    ("personal", "Personal médico"),
    ("via_administracion", "Vías de administración"),
    ("unidad_cantidad", "Unidades de cantidad"),
    ("departamento", "Departamentos"),
]


class SettingsPage(Page):
    nav_key = "settings"

    def __init__(self, app):
        super().__init__(app)
        ttk.Label(self, text="Configuración", style="H1.TLabel").pack(anchor="w")
        sf = widgets.ScrollFrame(self)
        sf.pack(fill="both", expand=True, pady=(6, 0))
        body = sf.body

        s1 = widgets.section(body, "Encabezado de los documentos PDF y nombre del operador")
        g = widgets.FormGrid(s1, 2)
        self.f = {}
        for key, label in (("encabezado_institucion", "Nombre del proyecto, institución o brigada"),
                           ("encabezado_subtitulo", "Subtítulo del encabezado"),
                           ("operador", "Nombre de quien registra (aparece en el historial de cambios)")):
            self.f[key] = widgets.EntryField(s1)
            g.add(label, self.f[key])
        row = ttk.Frame(s1)
        ttk.Button(row, text="Guardar", style="Accent.TButton", command=self.save_header).pack(side="left")
        self.h_status = ttk.Label(row, text="", style="Saved.TLabel")
        self.h_status.pack(side="left", padx=10)
        g.full(row, pady=(12, 0))
        g.full(ttk.Label(s1, text="No se usan logotipos oficiales: los documentos son formatos "
                         "clínicos digitales de uso interno.", style="Hint.TLabel"), pady=(6, 0))

        s2 = widgets.section(body, "Listas configurables (se pueden ampliar sin tocar el código)")
        top = ttk.Frame(s2)
        top.pack(fill="x")
        ttk.Label(top, text="Lista:", style="Field.TLabel").pack(side="left")
        self.cat_combo = widgets.ComboField(top, [t for _k, t in CATALOGS], width=34)
        self.cat_combo.set_value(CATALOGS[0][1])
        self.cat_combo.pack(side="left", padx=8)
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self._load_catalog())
        mid = ttk.Frame(s2)
        mid.pack(fill="x", pady=(8, 0))
        lb_frame = ttk.Frame(mid)
        lb_frame.pack(side="left", fill="both", expand=True)
        self.listbox = tk.Listbox(lb_frame, height=9, font=theme.FONT, activestyle="none",
                                  selectbackground=theme.PRIMARY, relief="solid", bd=1,
                                  highlightthickness=0)
        vs = ttk.Scrollbar(lb_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=vs.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        vs.pack(side="left", fill="y")
        right = ttk.Frame(mid)
        right.pack(side="left", padx=(14, 0), anchor="n")
        self.new_entry = widgets.EntryField(right, width=34)
        self.new_entry.pack(anchor="w")
        self.new_entry.bind("<Return>", lambda e: self.add_item())
        ttk.Button(right, text="Agregar a la lista", style="Accent.TButton", command=self.add_item).pack(
            anchor="w", pady=(6, 14))
        ttk.Button(right, text="Quitar el seleccionado", style="Danger.TButton",
                   command=self.remove_item).pack(anchor="w")
        ttk.Label(right, text="Quitar un valor no borra lo ya registrado\nen las fichas.",
                  style="Hint.TLabel").pack(anchor="w", pady=(6, 0))

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
        self._keys = {t: k for k, t in CATALOGS}

    def on_show(self, **kw):
        self.refresh()

    def refresh(self):
        for k, w in self.f.items():
            w.set_value(self.db.get_setting(k, ""))
        self._load_catalog()
        self._pw_state()
        self.h_status.configure(text="")

    def save_header(self):
        for k, w in self.f.items():
            self.db.set_setting(k, w.get_value().strip())
        self.h_status.configure(text="Configuración guardada.")

    # -- listas -------------------------------------------------------------
    def _cat(self):
        return self._keys[self.cat_combo.get_value()]

    def _load_catalog(self):
        self.listbox.delete(0, "end")
        for v in self.db.catalog(self._cat()):
            self.listbox.insert("end", v)

    def add_item(self):
        value = self.new_entry.get_value().strip()
        if not value:
            return
        if not self.db.add_catalog(self._cat(), value):
            dialogs.info(self, "Ese valor ya existe en la lista.")
        self.new_entry.set_value("")
        self._load_catalog()
        self.app.refresh_all()

    def remove_item(self):
        sel = self.listbox.curselection()
        if not sel:
            dialogs.info(self, "Seleccione un valor de la lista.")
            return
        value = self.listbox.get(sel[0])
        if dialogs.confirm(self, "Quitar de la lista", f"¿Quitar '{value}' de la lista?",
                           yes="Quitar", no="Cancelar", danger=True):
            self.db.remove_catalog(self._cat(), value)
            self._load_catalog()
            self.app.refresh_all()

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
