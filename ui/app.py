"""Ventana principal: menú lateral, barra del paciente activo y navegación."""
import sys
import tkinter as tk
import traceback
from tkinter import ttk

import backup
import config
import security
from services import brigades as brigade_svc
from services import patients as patient_svc
from ui import dialogs, theme, widgets

NAV = [
    ("home", "Inicio"),
    ("new_patient", "Registrar paciente"),
    ("search", "Buscar pacientes"),
    ("patient", "Ficha Integral"),
    ("aps", "Atención Primaria (APS)"),
    ("ssr", "Salud Sexual y Repr. (SSR)"),
    ("history", "Historial de atenciones"),
    ("brigades", "Brigadas"),
    ("reports", "Reportes y exportaciones"),
    ("backup", "Copias de seguridad"),
    ("settings", "Configuración"),
]


class App:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title(f"{config.APP_NAME}")
        self.root.geometry("1320x820")
        self.root.minsize(1120, 700)
        theme.setup(self.root)
        widgets.install_global_bindings(self.root)
        self.root.report_callback_exception = self._on_exception
        self.active_pid = None
        self.pages = {}
        self.current = None
        self.current_name = None
        self._history = []
        self._last_kw = {}
        self._nav_buttons = {}
        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind_all("<Control-s>", lambda e: self._shortcut("save"))
        self.root.bind_all("<Control-n>", lambda e: self.show("patient", new=True))
        self.root.bind_all("<Control-b>", lambda e: self.show("search"))

    # -- construcción -----------------------------------------------------------
    def _build(self):
        side = ttk.Frame(self.root, style="Sidebar.TFrame", width=280)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        ttk.Label(side, text="Brigadas Médicas", style="SidebarTitle.TLabel").pack(
            anchor="w", padx=18, pady=(20, 0))
        ttk.Label(side, text="Registro clínico digital", style="SidebarSub.TLabel").pack(
            anchor="w", padx=18, pady=(0, 16))
        for key, text in NAV:
            b = ttk.Button(side, text=text, style="Nav.TButton",
                           command=lambda k=key: self.navigate(k))
            b.pack(fill="x")
            self._nav_buttons[key] = b
        spacer = ttk.Frame(side, style="Sidebar.TFrame")
        spacer.pack(fill="both", expand=True)
        self.side_brigade = ttk.Label(side, text="", style="SidebarSub.TLabel", wraplength=210,
                                      justify="left")
        self.side_brigade.pack(anchor="w", padx=18, pady=(0, 4))
        ttk.Label(side, text="Ctrl+N  nuevo paciente\nCtrl+B  buscar paciente\nCtrl+S  guardar ficha",
                  style="SidebarSub.TLabel", justify="left").pack(anchor="w", padx=18, pady=(0, 6))
        ttk.Button(side, text="Salir", style="Nav.TButton", command=self.close).pack(
            fill="x", pady=(0, 10))

        main = ttk.Frame(self.root)
        main.pack(side="left", fill="both", expand=True)
        self.strip = ttk.Frame(main, style="Strip.TFrame", padding=(16, 8))
        self._build_strip()
        self.content = ttk.Frame(main, padding=(20, 14, 20, 10))
        self.content.pack(fill="both", expand=True)
        self.refresh_brigade_label()

    def _build_strip(self):
        s = self.strip
        left = ttk.Frame(s, style="Strip.TFrame")
        left.pack(side="left")
        self.strip_name = ttk.Label(left, text="", style="StripB.TLabel")
        self.strip_name.pack(anchor="w")
        self.strip_info = ttk.Label(left, text="", style="Strip.TLabel")
        self.strip_info.pack(anchor="w")
        ttk.Button(s, text="Quitar", style="Strip.TButton", command=self.clear_active).pack(
            side="right")
        ttk.Button(s, text="Historial", style="Strip.TButton",
                   command=lambda: self.show("history", patient_id=self.active_pid)).pack(
            side="right", padx=(0, 6))
        ttk.Button(s, text="Nueva SSR", style="Strip.TButton",
                   command=lambda: self.new_visit("ssr")).pack(side="right", padx=(0, 6))
        ttk.Button(s, text="Nueva APS", style="Strip.TButton",
                   command=lambda: self.new_visit("aps")).pack(side="right", padx=(0, 6))
        ttk.Button(s, text="Ficha Integral", style="Strip.TButton",
                   command=lambda: self.open_patient(self.active_pid)).pack(
            side="right", padx=(0, 6))

    # -- páginas ----------------------------------------------------------------
    def _page(self, name):
        if name not in self.pages:
            from ui.page_backup import BackupPage
            from ui.page_brigades import BrigadesPage
            from ui.page_history import HistoryPage
            from ui.page_home import HomePage
            from ui.page_patient import PatientPage
            from ui.page_reports import ReportsPage
            from ui.page_search import SearchPage
            from ui.page_settings import SettingsPage
            from ui.page_visit import VisitPage
            factories = {
                "home": lambda: HomePage(self), "patient": lambda: PatientPage(self),
                "search": lambda: SearchPage(self), "aps": lambda: VisitPage(self, "aps"),
                "ssr": lambda: VisitPage(self, "ssr"), "history": lambda: HistoryPage(self),
                "brigades": lambda: BrigadesPage(self), "reports": lambda: ReportsPage(self),
                "backup": lambda: BackupPage(self), "settings": lambda: SettingsPage(self),
            }
            self.pages[name] = factories[name]()
        return self.pages[name]

    def navigate(self, key):
        """Navegación desde el menú lateral."""
        if key == "new_patient":
            return self.show("patient", new=True)
        if key == "patient":
            return self.show("patient")
        return self.show(key)

    def back(self):
        """Regresa a la pantalla anterior (o al inicio si no hay)."""
        while self._history:
            name, kw = self._history.pop()
            if name != self.current_name or kw:
                return self.show(name, _from_back=True, **kw)
        return self.show("home", _from_back=True)

    def show(self, name, _from_back=False, **kw):
        """Muestra una página. Devuelve False si el usuario decidió quedarse."""
        if self.current is not None and not self.current.can_leave():
            return False
        page = self._page(name)
        if self.current is not None:
            if not _from_back and self.current_name != name:
                self._history.append((self.current_name, dict(self._last_kw)))
                del self._history[:-20]
            self.current.pack_forget()
        self._last_kw = {k: v for k, v in kw.items() if k in ("patient_id", "visit_id")
                         and v is not None}
        self.current, self.current_name = page, name
        page.pack(fill="both", expand=True)
        page.on_show(**kw)
        key = "new_patient" if (name == "patient" and kw.get("new")) else name
        self._highlight(key)
        self._update_strip()
        return True

    def _highlight(self, key):
        for k, b in self._nav_buttons.items():
            b.configure(style="NavActive.TButton" if k == key else "Nav.TButton")

    def refresh_all(self):
        for p in self.pages.values():
            p.refresh()
        self.refresh_brigade_label()
        self._update_strip()

    # -- paciente activo ---------------------------------------------------------
    def set_active(self, pid):
        self.active_pid = pid
        self._update_strip()

    def clear_active(self):
        if self.current is not None and self.current_name in ("patient", "aps", "ssr") \
                and not self.current.can_leave():
            return
        self.active_pid = None
        self._update_strip()
        if self.current_name in ("patient", "aps", "ssr"):
            self.current.on_show()

    def _update_strip(self):
        p = patient_svc.get_patient(self.db, self.active_pid) if self.active_pid else None
        if not p:
            self.active_pid = None
            self.strip.pack_forget()
            return
        aps_n, ssr_n = patient_svc.patient_counts(self.db, p["id"])
        self.strip_name.configure(text=f"Paciente activo:  {patient_svc.display_name(p)}")
        self.strip_info.configure(
            text=f"{p['codigo']}  ·  {patient_svc.age_text(p) or 'edad no registrada'}  ·  "
                 f"{p['sexo'] or ''}  ·  atenciones APS: {aps_n}  ·  SSR: {ssr_n}")
        if self.current_name in ("patient", "aps", "ssr"):
            self.strip.pack_forget()  # esas pantallas ya muestran al paciente
        else:
            self.strip.pack(side="top", fill="x", before=self.content)

    def open_patient(self, pid):
        if pid:
            self.set_active(pid)
            self.show("patient", patient_id=pid)

    def new_visit(self, kind, pid=None):
        pid = pid or self.active_pid
        if pid:
            self.set_active(pid)
        self.show(kind, patient_id=pid, visit_id=None)

    def open_visit(self, kind, vid):
        row = self.db.one(f"SELECT patient_id FROM {kind}_visits WHERE id=?", (vid,))
        if row:
            self.set_active(row["patient_id"])
            self.show(kind, patient_id=row["patient_id"], visit_id=vid)

    # -- brigada actual -----------------------------------------------------------
    def current_brigade_id(self):
        v = self.db.get_setting("brigada_actual", "")
        if v and v.isdigit() and brigade_svc.get_brigade(self.db, int(v)):
            return int(v)
        return None

    def set_current_brigade(self, bid):
        self.db.set_setting("brigada_actual", "" if bid is None else str(bid))
        self.refresh_brigade_label()

    def refresh_brigade_label(self):
        bid = self.current_brigade_id()
        if bid:
            self.side_brigade.configure(
                text="Brigada actual:\n" + brigade_svc.label(brigade_svc.get_brigade(self.db, bid)))
        else:
            self.side_brigade.configure(text="Brigada actual: (ninguna)")

    # -- ciclo de vida -------------------------------------------------------------
    def _shortcut(self, what):
        if self.current is not None and what == "save":
            self.current.on_save_shortcut()

    def _on_exception(self, exc_type, exc, tb):
        text = "".join(traceback.format_exception(exc_type, exc, tb))
        try:
            with open(config.log_path(), "a", encoding="utf-8") as fh:
                from datetime import datetime
                fh.write(f"\n--- {datetime.now():%Y-%m-%d %H:%M:%S} ---\n{text}")
        except OSError:
            pass
        try:
            dialogs.error(self.root,
                          "Ocurrió un error inesperado. Sus datos guardados no se han perdido.\n"
                          f"Detalle: {exc}\n\nSe registró en: {config.log_path()}",
                          title="Error del programa")
        except Exception:  # noqa: BLE001
            print(text, file=sys.stderr)

    def login(self):
        stored = self.db.get_setting("password_hash", "")
        if not stored:
            return True
        for attempt in range(3):
            pw = dialogs.ask_password(self.root, "Acceso protegido",
                                      "Escriba la contraseña para abrir el programa:")
            if pw is None:
                return False
            if security.verify_password(pw, stored):
                return True
            dialogs.error(self.root, "Contraseña incorrecta. "
                          f"Intentos restantes: {2 - attempt}.", title="Acceso")
        return False

    def run(self):
        self.root.deiconify()
        if not self.login():
            self.root.destroy()
            return
        self.show("home")
        self.root.mainloop()

    def close(self):
        if self.current is not None and not self.current.can_leave():
            return
        if self.db.get_setting("respaldo_al_salir", "1") == "1":
            try:
                backup.auto_backup(self.db)
            except Exception:  # noqa: BLE001  (un fallo de respaldo no debe impedir cerrar)
                pass
        self.db.close()
        self.root.destroy()
