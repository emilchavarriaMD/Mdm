"""Ventana principal: menú lateral y navegación."""
import sys
import tkinter as tk
import traceback
from tkinter import ttk

import backup
import config
import security
from ui import dialogs, theme, widgets

NAV = [
    ("ata", "Cargar ATA"),
    ("pacientes", "Pacientes"),
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
        self.pages = {}
        self.current = None
        self.current_name = None
        self._nav_buttons = {}
        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind_all("<Control-s>", lambda e: self._shortcut())
        for i, (key, _t) in enumerate(NAV, 1):             # Ctrl+1…4: cambiar de pantalla
            self.root.bind_all(f"<Control-Key-{i}>", lambda e, k=key: self.show(k))

    def _build(self):
        side = ttk.Frame(self.root, style="Sidebar.TFrame", width=int(240 * theme.FONT[1] / 11))
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        ttk.Label(side, text="Brigadas Médicas", style="SidebarTitle.TLabel").pack(
            anchor="w", padx=18, pady=(20, 0))
        ttk.Label(side, text="ATA y ActivityInfo", style="SidebarSub.TLabel").pack(
            anchor="w", padx=18, pady=(0, 16))
        for key, text in NAV:
            b = ttk.Button(side, text=text, style="Nav.TButton", command=lambda k=key: self.show(k))
            b.pack(fill="x")
            self._nav_buttons[key] = b
        ttk.Frame(side, style="Sidebar.TFrame").pack(fill="both", expand=True)
        ttk.Label(side, text="Ctrl+S  guardar hoja\nCtrl+1…4  cambiar de pantalla", style="SidebarSub.TLabel",
                  justify="left").pack(anchor="w", padx=18, pady=(0, 6))
        ttk.Button(side, text="Salir", style="Nav.TButton", command=self.close).pack(fill="x", pady=(0, 10))
        main = ttk.Frame(self.root)
        main.pack(side="left", fill="both", expand=True)
        self.content = ttk.Frame(main, padding=(20, 14, 20, 10))
        self.content.pack(fill="both", expand=True)

    def _page(self, name):
        if name not in self.pages:
            from ui.page_ata import AtaPage
            from ui.page_backup import BackupPage
            from ui.page_pacientes import PacientesPage
            from ui.page_settings import SettingsPage
            factories = {"ata": lambda: AtaPage(self), "pacientes": lambda: PacientesPage(self),
                         "backup": lambda: BackupPage(self), "settings": lambda: SettingsPage(self)}
            self.pages[name] = factories[name]()
        return self.pages[name]

    def show(self, name, **kw):
        """Muestra una página. Devuelve False si el usuario decidió quedarse."""
        if self.current is not None and not self.current.can_leave():
            return False
        page = self._page(name)
        if self.current is not None:
            self.current.pack_forget()
        self.current, self.current_name = page, name
        page.pack(fill="both", expand=True)
        page.on_show(**kw)
        for k, b in self._nav_buttons.items():
            b.configure(style="NavActive.TButton" if k == name else "Nav.TButton")
        return True

    def refresh_all(self):
        for p in self.pages.values():
            p.refresh()

    def _shortcut(self):
        if self.current is not None:
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
            dialogs.error(self.root, f"Contraseña incorrecta. Intentos restantes: {2 - attempt}.",
                          title="Acceso")
        return False

    def run(self):
        self.root.deiconify()
        if not self.login():
            self.root.destroy()
            return
        self.show("ata")
        self._programar_respaldo()
        self.root.mainloop()

    INTERVALO_RESPALDO_MS = 30 * 60 * 1000

    def _programar_respaldo(self):
        """Copia automática cada 30 minutos mientras el programa está abierto (si no se desactivó)."""
        def tick():
            try:
                if self.db.get_setting("respaldo_periodico", "1") == "1":
                    backup.auto_backup(self.db, prefix="periodica", keep=12)
            except Exception:  # noqa: BLE001
                pass
            self._respaldo_job = self.root.after(self.INTERVALO_RESPALDO_MS, tick)
        self._respaldo_job = self.root.after(self.INTERVALO_RESPALDO_MS, tick)

    def close(self):
        if self.current is not None and not self.current.can_leave():
            return
        if self.db.get_setting("respaldo_al_salir", "1") == "1":
            try:
                backup.auto_backup(self.db)
            except Exception:  # noqa: BLE001
                pass
        self.db.close()
        self.root.destroy()
