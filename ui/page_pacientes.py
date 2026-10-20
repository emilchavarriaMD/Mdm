"""Pacientes cargados desde los ATA, con el botón «Añadir registro» al lado de cada uno."""
import threading
from tkinter import ttk

from services import activityinfo
from services import ata as ata_svc
from services import coherencia, fill_log, resumen
from services.validators import fmt_date
from ui import dialogs, dialogs_extra, theme, widgets
from ui.dialog_activityinfo import ActivityInfoDialog
from ui.page import Page

ACTION = "➕ Añadir registro"
GRUPOS_EDAD = ["Todas las edades"] + [g[0] for g in resumen.GRUPOS]


class PacientesPage(Page):
    nav_key = "pacientes"

    def __init__(self, app):
        super().__init__(app)
        self._after = None
        self._rows = {}
        self._alertas = {}
        self._busy = False
        self._result = None
        self._checked = set()
        ttk.Label(self, text="Pacientes", style="H1.TLabel").pack(anchor="w")
        bar = ttk.Frame(self)
        bar.pack(fill="x")
        ttk.Label(bar, text="Buscar:").pack(side="left")
        self.q = widgets.EntryField(bar, width=30)
        self.q.pack(side="left", padx=(6, 12))
        self.q.var.trace_add("write", lambda *a: self._schedule())
        ttk.Label(bar, text="Estado:").pack(side="left")
        self.estado = widgets.ComboField(bar, ["Todos", "Pendiente", "Llenado", "Registrado"], readonly=True, width=14)
        self.estado.set_value("Todos")
        self.estado.pack(side="left", padx=(6, 12))
        self.estado.bind("<<ComboboxSelected>>", lambda e: self.load())
        ttk.Label(bar, text="Sexo:").pack(side="left")
        self.sexo = widgets.ComboField(bar, ["Todos", "Mujer", "Hombre"], readonly=True, width=9)
        self.sexo.set_value("Todos")
        self.sexo.pack(side="left", padx=(6, 12))
        self.sexo.bind("<<ComboboxSelected>>", lambda e: self.load())
        ttk.Label(bar, text="Edad:").pack(side="left")
        self.grupo = widgets.ComboField(bar, GRUPOS_EDAD, readonly=True, width=18)
        self.grupo.set_value(GRUPOS_EDAD[0])
        self.grupo.pack(side="left", padx=(6, 12))
        self.grupo.bind("<<ComboboxSelected>>", lambda e: self.load())
        self.count = ttk.Label(bar, text="", style="Muted.TLabel")
        self.count.pack(side="left", padx=6)
        bar2 = ttk.Frame(self)
        bar2.pack(fill="x", pady=(8, 0))
        ttk.Button(bar2, text="Seleccionar paciente", command=self.toggle_current).pack(side="left")
        ttk.Button(bar2, text="Seleccionar todo", command=self.toggle_all).pack(side="left", padx=8)
        self.btn_del = ttk.Button(bar2, text="Borrar", command=self.delete_checked)
        self.btn_del.pack(side="left")
        ttk.Button(bar2, text="Papelera", command=self.papelera).pack(side="left", padx=(8, 0))

        frame, self.tree = widgets.make_tree(self, [
            ("sel", "", 46, "center"), ("fecha", "Fecha", 108), ("nombre", "Paciente", 270), ("accion", "Acción", 160, "center"),
            ("estado", "ActivityInfo", 120, "center"), ("sexo", "Sexo", 50, "center"),
            ("edad", "Edad", 70), ("dx", "Diagnósticos", 340)], height=10)
        frame.pack(fill="both", expand=True, pady=(8, 0))
        self.tree.tag_configure("e_Pendiente", foreground=theme.TEXT)
        self.tree.tag_configure("e_Llenado", foreground=theme.WARN)
        self.tree.tag_configure("e_Registrado", foreground=theme.OK)
        self.tree.bind("<Button-1>", self._click)
        self.tree.bind("<Return>", lambda e: self.add_record())
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._mostrar_alertas())
        self.alerta = ttk.Label(self, text="", foreground=theme.WARN, wraplength=1000, justify="left")
        self.alerta.pack(anchor="w", pady=(4, 0))
        self.bind_all("<Control-f>", lambda e: self.q.focus_set() if self.winfo_ismapped() else None)
        self.progreso = ttk.Progressbar(self, maximum=100, mode="determinate")
        self.progreso.pack(fill="x", pady=(6, 0))
        bot = ttk.Frame(self)
        bot.pack(fill="x", pady=(10, 0))
        ttk.Button(bot, text="Añadir registro al seleccionado", style="Accent.TButton",
                   command=self.add_record).pack(side="left")
        ttk.Button(bot, text="Ver registro guardado", command=self.ver_registro).pack(side="left", padx=(8, 0))
        ttk.Button(bot, text="Siguiente pendiente ▶", command=self.siguiente_pendiente).pack(side="left", padx=8)
        bot2 = ttk.Frame(self)
        ttk.Button(bot2, text="Marcar como registrado", command=lambda: self.mark(True)).pack(side="left")
        ttk.Button(bot2, text="Marcar como pendiente", command=lambda: self.mark(False)).pack(side="left", padx=8)
        ttk.Button(bot2, text="Bitácora del llenado", command=lambda: dialogs_extra.bitacora(self)).pack(side="right")
        ttk.Button(bot2, text="Resumen a Excel", command=self.resumen_excel).pack(side="right", padx=8)
        ttk.Button(bot2, text="Cargar otro ATA", command=lambda: self.app.show("ata")).pack(side="right")
        # lo de abajo se reserva primero: con ventanas bajas la lista se encoge y los botones nunca se cortan
        for w in (frame, self.alerta, self.progreso, bot):
            w.pack_forget()
        bot2.pack(side="bottom", fill="x", pady=(8, 0))
        bot.pack(side="bottom", fill="x", pady=(10, 0))
        self.progreso.pack(side="bottom", fill="x", pady=(6, 0))
        self.alerta.pack(side="bottom", anchor="w", pady=(4, 0))
        frame.pack(fill="both", expand=True, pady=(8, 0))

    def on_show(self, **kw):
        self.load()
        self.q.focus_set()

    def refresh(self):
        self.load()

    def _schedule(self):
        if self._after:
            self.after_cancel(self._after)
        self._after = self.after(250, self.load)

    def load(self):
        self._after = None
        rows = ata_svc.list_records(self.db, self.q.get_value(), self.estado.get_value())
        sx = {"Mujer": "M", "Hombre": "H"}.get(self.sexo.get_value())
        if sx:
            rows = [r for r in rows if r["sexo"] == sx]
        g = self.grupo.get_value()
        if g in GRUPOS_EDAD[1:]:
            rows = [r for r in rows if resumen.grupo_edad(r) == g]
        self._alertas = {r["id"]: coherencia.alertas_registro(r) for r in rows}
        self._rows = {r["id"]: r for r in rows}
        self._checked &= set(self._rows)
        marca = {"Pendiente": "○ Pendiente", "Llenado": "◐ Llenado", "Registrado": "● Registrado"}
        widgets.fill_tree(self.tree, [(
            r["id"], ("☑" if r["id"] in self._checked else "☐", fmt_date(r["fecha"]),
                      ("⚠ " if self._alertas.get(r["id"]) else "") + r["nombre"],
                      ACTION if r["ai_estado"] != "Registrado" else "Registrado ✔",
                      marca.get(r["ai_estado"], r["ai_estado"]), r["sexo"], ata_svc.age_text(r),
                      " · ".join(x for x in (r["dx1"], r["dx2"], r["dx3"]) if x)),
            ["e_" + r["ai_estado"]]) for r in rows])
        pend = sum(1 for r in rows if r["ai_estado"] == "Pendiente")
        llen = sum(1 for r in rows if r["ai_estado"] == "Llenado")
        reg = sum(1 for r in rows if r["ai_estado"] == "Registrado")
        self.count.configure(text=f"{len(rows)} paciente(s) · {pend} pendiente(s) · {llen} llenado(s) sin registrar")
        self.progreso.configure(value=(100 * (llen + reg) / len(rows)) if rows else 0)
        self._update_buttons()
        self._mostrar_alertas()

    def _mostrar_alertas(self):
        iid = widgets.selected_iid(self.tree)
        al = self._alertas.get(int(iid)) if iid and iid.isdigit() else None
        self.alerta.configure(text=("⚠ Revisar: " + " · ".join(al)) if al else "")

    def siguiente_pendiente(self):
        """Selecciona (y abre) el siguiente paciente que todavía está pendiente, después del seleccionado."""
        ids = [i for i in self.tree.get_children("") if self._rows.get(int(i), {}).get("ai_estado") == "Pendiente"]
        if not ids:
            dialogs.info(self, "No quedan pacientes pendientes en esta lista.")
            return
        actual = widgets.selected_iid(self.tree)
        todos = list(self.tree.get_children(""))
        despues = [i for i in ids if actual in todos and todos.index(i) > todos.index(actual)]
        iid = (despues or ids)[0]
        self.tree.selection_set(iid)
        self.tree.see(iid)
        self.add_record()

    def papelera(self):
        if dialogs_extra.papelera(self, self.db):
            self.app.refresh_all()

    def resumen_excel(self):
        from datetime import date
        path = dialogs.ask_save_path(self, "Guardar resumen de la brigada", initialfile=f"Resumen_brigada_{date.today():%Y%m%d}.xlsx",
                                     ext=".xlsx", types=[("Excel", "*.xlsx")])
        if not path:
            return
        try:
            n = resumen.exportar(self.db, path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear el archivo de Excel:\n{exc}")
            return
        if dialogs.confirm(self, "Excel generado", f"Resumen de {n} paciente(s) guardado en:\n{path}", yes="Abrir", no="Cerrar"):
            widgets.open_path(path)

    # -- selección y borrado ---------------------------------------------------
    def _update_buttons(self):
        n = len(self._checked)
        self.btn_del.configure(text=f"Borrar ({n})" if n else "Borrar")

    def _set_check(self, rid, on):
        (self._checked.add if on else self._checked.discard)(rid)
        if self.tree.exists(str(rid)):
            self.tree.set(str(rid), "sel", "☑" if on else "☐")
        self._update_buttons()

    def toggle_current(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Pulse primero un paciente de la lista.")
            return
        self._set_check(int(iid), int(iid) not in self._checked)

    def toggle_all(self):
        ids = [int(i) for i in self.tree.get_children("")]
        on = not (ids and all(i in self._checked for i in ids))
        for i in ids:
            self._set_check(i, on)

    def delete_checked(self):
        ids = sorted(self._checked)
        if not ids:
            dialogs.info(self, "No hay pacientes marcados. Use «Seleccionar paciente» o «Seleccionar todo».")
            return
        nombres = [self._rows[i]["nombre"] for i in ids if i in self._rows]
        resumen = "\n".join(f"• {n}" for n in nombres[:8]) + (f"\n… y {len(nombres) - 8} más" if len(nombres) > 8 else "")
        if not dialogs.confirm(self, "Borrar pacientes", f"¿Quitar {len(ids)} paciente(s) del programa?\n\n{resumen}\n\n"
                               "Se mandan a la Papelera (puede recuperarlos desde el botón «Papelera»). "
                               "Esto no toca ActivityInfo.", yes="Borrar", no="Cancelar"):
            return
        ata_svc.delete_records(self.db, ids)
        self._checked.clear()
        self.app.refresh_all()

    def _click(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        col = self.tree.identify_column(event.x)
        iid = self.tree.identify_row(event.y)
        if iid and col == "#1":
            self._set_check(int(iid), int(iid) not in self._checked)
            return "break"
        if iid and col == f"#{list(self.tree['columns']).index('accion') + 1}":
            self.tree.selection_set(iid)
            self.after(10, self.add_record)

    def _selected(self):
        iid = widgets.selected_iid(self.tree)
        if not iid:
            dialogs.info(self, "Seleccione primero un paciente de la lista.")
            return None
        return int(iid)

    def add_record(self):
        rid = self._selected()
        if rid is None:
            return
        rec = ata_svc.get_record(self.db, rid)
        if rec["ai_estado"] == "Registrado" and not dialogs.confirm(
                self, "Ya registrado", f"{rec['nombre']} ya está marcado como registrado en "
                "ActivityInfo. ¿Llenar el formulario otra vez?", yes="Llenar de nuevo", no="Cancelar"):
            return
        self._abrir_dialogo(rid, rec, activityinfo.build_defaults(self.db, rec))

    def ver_registro(self):
        """Vuelve a abrir, tal como se dejó, lo que se revisó y llenó la última vez para este paciente."""
        rid = self._selected()
        if rid is None:
            return
        rec = ata_svc.get_record(self.db, rid)
        guardado = ata_svc.load_datos(self.db, rid)
        if not guardado:
            dialogs.info(self, f"Todavía no hay un registro guardado de {rec['nombre']}. Se guarda al pulsar "
                         "«Abrir Chrome y llenar» en «Añadir registro».")
            return
        d = activityinfo.build_defaults(self.db, rec)
        d.update(guardado)
        d["_restaurado"] = True
        self._abrir_dialogo(rid, rec, d, titulo=f"Registro guardado — {rec['nombre']}")

    def _abrir_dialogo(self, rid, rec, defaults, titulo=None):
        dlg = ActivityInfoDialog(self, defaults, db=self.db, **({"title": titulo} if titulo else {}))
        data = dlg.run()
        if not data:
            return
        snap = getattr(dlg, "snap", None)
        if snap:
            ata_svc.save_datos(self.db, rid, snap)      # se guarda antes de llenar: así se puede volver a ver
        activityinfo.remember_dx(self.db, data)
        self._busy = True
        self.count.configure(text="Abriendo Chrome… si pide iniciar sesión, hágalo en esa ventana.")
        threading.Thread(target=self._worker, args=(rid, rec["nombre"], data), daemon=True).start()
        self.after(400, self._poll)

    def _worker(self, rid, nombre, data):
        try:
            self._result = (rid, nombre, data, activityinfo.fill_form(data), None)
        except Exception as exc:  # noqa: BLE001
            self._result = (rid, nombre, data, None, exc)

    def _poll(self):
        if self._result is None:
            self.after(400, self._poll)
            return
        rid, nombre, data, report, exc = self._result
        self._result = None
        fill_log.registrar(nombre, report, exc, data.get("consultas"))
        if exc is None:
            ata_svc.set_llenado(self.db, rid)
        self.load()
        if exc is not None:
            dialogs.error(self, f"No se pudo llenar el formulario:\n{exc}")
            return
        falta = (report.get("ficha") or []) + (report.get("aps") or []) + (report.get("ssr") or [])
        msg = f"Se llenó el formulario de {nombre} en Chrome. REVÍSELO y cree la ficha usted en ActivityInfo " \
              "(el programa no guarda nada)."
        if (data.get("ssr") or {}).get("dx") is not None and "Salud Sexual y Reproductiva" in (data.get("consultas") or []):
            msg += "\nEl subformulario de Salud Sexual y Reproductiva quedó abierto: revíselo y pulse «Está hecho» usted."
        info = report.get("info") or []
        if info:
            msg += "\n\nDiagnósticos elegidos en ActivityInfo (verifíquelos):\n" + "\n".join(f"• {i}" for i in info)
        verif = report.get("verif") or []
        if verif:
            msg += "\n\nVerificación (algo no quedó como se escribió):\n" + "\n".join(f"• {v}" for v in verif)
        if falta:
            msg += "\n\nNo se pudieron llenar (hágalo a mano):\n" + "\n".join(f"• {f}" for f in falta)
        dialogs.info(self, msg, title="Formulario llenado")
        if dialogs.confirm(self, "¿Se registró?", f"Cuando haya creado la ficha de {nombre} en ActivityInfo, "
                           "¿la marco como registrada?", yes="Sí, marcar", no="Todavía no"):
            ata_svc.set_registered(self.db, rid, True)
            self.load()

    def mark(self, registered):
        rid = self._selected()
        if rid is not None:
            ata_svc.set_registered(self.db, rid, registered)
            self.load()
