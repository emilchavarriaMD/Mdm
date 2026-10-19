"""Copias de seguridad y restauración."""
from datetime import datetime
from tkinter import ttk

import backup
import config
from ui import dialogs, widgets
from ui.page import Page


class BackupPage(Page):
    nav_key = "backup"

    def __init__(self, app):
        super().__init__(app)
        ttk.Label(self, text="Copias de seguridad", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Haga una copia al terminar cada jornada y guárdela también en una "
                  "memoria USB o disco externo.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))

        s1 = widgets.section(self, "Dónde están sus datos")
        self.path_lbl = ttk.Label(s1, text="", wraplength=900, justify="left")
        self.path_lbl.pack(anchor="w")
        row = ttk.Frame(s1)
        row.pack(anchor="w", pady=(8, 0))
        ttk.Button(row, text="Abrir carpeta de datos", command=lambda: widgets.open_path(config.data_dir())
                   ).pack(side="left")
        ttk.Button(row, text="Abrir carpeta de respaldos",
                   command=lambda: widgets.open_path(config.backups_dir())).pack(side="left", padx=8)

        s2 = widgets.section(self, "Crear copia de seguridad")
        row = ttk.Frame(s2)
        row.pack(anchor="w")
        ttk.Button(row, text="Crear copia ahora", style="Accent.TButton", command=self.create_here).pack(
            side="left")
        ttk.Button(row, text="Guardar copia en otra ubicación (USB, disco…)",
                   command=self.create_elsewhere).pack(side="left", padx=8)
        self.auto = widgets.CheckField(s2, text="Crear una copia automática al cerrar el programa")
        self.auto.configure(command=self._auto_changed)
        self.auto.pack(anchor="w", pady=(10, 0))
        self.status = ttk.Label(s2, text="", style="Saved.TLabel")
        self.status.pack(anchor="w", pady=(6, 0))

        s3 = widgets.section(self, "Restaurar")
        ttk.Label(s3, text="Al restaurar se reemplazan los datos actuales por los de la copia. "
                  "Antes se guarda automáticamente una copia 'previa_restauracion' de lo actual.",
                  style="Hint.TLabel", wraplength=900, justify="left").pack(anchor="w", pady=(0, 6))
        frame, self.tree = widgets.make_tree(s3, [("n", "Archivo", 360), ("f", "Fecha", 140),
                                                  ("s", "Tamaño", 90, "e")], height=7)
        frame.pack(fill="x")
        row = ttk.Frame(s3)
        row.pack(anchor="w", pady=(8, 0))
        ttk.Button(row, text="Restaurar la copia seleccionada", command=self.restore_selected).pack(
            side="left")
        ttk.Button(row, text="Restaurar desde un archivo…", command=self.restore_file).pack(
            side="left", padx=8)
        self._files = {}

    def on_show(self, **kw):
        self.refresh()

    def refresh(self):
        self.path_lbl.configure(text=f"Base de datos: {config.db_path()}\n"
                                     f"Copias automáticas y manuales: {config.backups_dir()}")
        self.auto.set_value(self.db.get_setting("respaldo_al_salir", "1") == "1")
        files = backup.list_backups()
        self._files = {str(p): p for p in files}
        widgets.fill_tree(self.tree, [(
            str(p), (p.name, datetime.fromtimestamp(p.stat().st_mtime).strftime("%d/%m/%Y %H:%M"),
                     f"{p.stat().st_size / 1024:.0f} KB")) for p in files])

    def _auto_changed(self):
        self.db.set_setting("respaldo_al_salir", "1" if self.auto.get_value() else "0")

    def create_here(self):
        try:
            path = backup.create_backup(self.db)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear la copia de seguridad:\n{exc}")
            return
        self.status.configure(text=f"Copia creada: {path.name}")
        self.refresh()

    def create_elsewhere(self):
        folder = dialogs.ask_directory(self, "Elija la carpeta o unidad donde guardar la copia")
        if not folder:
            return
        try:
            path = backup.create_backup(self.db, folder)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo guardar la copia en esa ubicación:\n{exc}")
            return
        self.status.configure(text=f"Copia guardada en: {path}")

    def restore_selected(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Seleccione una copia de la lista.")
            return
        self._restore(iid)

    def restore_file(self):
        path = dialogs.ask_open_path(self, "Elija la copia de seguridad (.db)")
        if path:
            self._restore(path)

    def _restore(self, path):
        try:
            stats = backup.validate_backup(path)
        except backup.BackupError as exc:
            dialogs.error(self, str(exc), title="Copia no válida")
            return
        if not dialogs.confirm(
                self, "Restaurar copia de seguridad",
                f"La copia contiene {stats['ata']} paciente(s) de hojas ATA.\n\nSe reemplazarán los datos actuales. "
                "¿Desea continuar?", yes="Restaurar", no="Cancelar", danger=True):
            return
        try:
            backup.restore_backup(self.db, path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo restaurar:\n{exc}")
            return
        self.app.refresh_all()
        self.refresh()
        dialogs.info(self, "Copia restaurada correctamente.", title="Restauración")
