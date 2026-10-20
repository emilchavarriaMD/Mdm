"""Pacientes atendidos: tabla editable (se carga desde el Excel ATA-2023) para confirmar lo que se registra."""
import json
import tkinter as tk
from datetime import date
from tkinter import ttk

from services import ata as ata_svc
from services.validators import fmt_date
from ui import common, dialogs, theme, widgets
from ui.page import Page

START_ROWS = 20


class AtaPage(Page):
    nav_key = "ata"

    def __init__(self, app):
        super().__init__(app)
        self.sheet_id = None
        self.image_name = None
        self._clean = None
        self.cells = []          # filas: {clave: StringVar}
        self.h = {}              # encabezado: {clave: StringVar}
        self._sheets = {}

        ttk.Label(self, text="Pacientes atendidos", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Suba el Excel del ATA (formato ATA-2023), revise la tabla y confírmela. También puede escribir o pegar los datos. "
                  "Nada se llena solo. "
                  "Las comillas (\") en departamento, municipio y localidad se repiten desde la fila anterior.", style="Muted.TLabel",
                  wraplength=1000, justify="left").pack(anchor="w", pady=(0, 6))

        bar = ttk.Frame(self)
        bar.pack(fill="x")
        ttk.Label(bar, text="Hoja:").pack(side="left")
        self.combo = widgets.ComboField(bar, [], readonly=True)
        self.combo.configure(width=26)
        self.combo.pack(side="left", padx=(6, 8))
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._on_pick())
        ttk.Button(bar, text="+ Nueva hoja", command=self.new).pack(side="left")
        self.btn_delete = ttk.Button(bar, text="Eliminar hoja", style="Danger.TButton", command=self.delete)
        self.btn_delete.pack(side="left", padx=8)
        self.status = ttk.Label(bar, text="", style="Saved.TLabel")
        self.status.pack(side="left", padx=10)
        # segunda fila: así ningún botón queda cortado en pantallas de 1366 px
        bar2 = ttk.Frame(self)
        bar2.pack(fill="x", pady=(6, 0))
        ttk.Button(bar2, text="Subir Excel (ATA-2023)", style="Accent.TButton", command=self.load_excel).pack(side="left")
        ttk.Button(bar2, text="Guardar en la base", style="Accent.TButton", command=self.save).pack(side="left", padx=8)
        ttk.Button(bar2, text="Exportar Excel", command=self.export).pack(side="left", padx=8)
        self.hint = ttk.Label(self, text="", style="Hint.TLabel")
        self.hint.pack(anchor="w", pady=(4, 0))

        # Todo lo de abajo se desliza junto, como una sola pantalla (no hay barras internas verticales)
        self.scroller = widgets.ScrollFrame(self)
        self.scroller.pack(fill="both", expand=True, pady=(8, 0))
        body = self.scroller.body

        # --- encabezado ---
        hb = ttk.Frame(body, style="Card.TFrame", padding=(14, 10, 14, 12))
        hb.pack(fill="x", padx=(0, 6), pady=(0, 12))
        ttk.Label(hb, text="Encabezado de la hoja", style="H2.TLabel", background=theme.CARD).grid(
            row=0, column=0, columnspan=len(ata_svc.HEADER_FIELDS), sticky="w", pady=(0, 6))
        for i, (k, label) in enumerate(ata_svc.HEADER_FIELDS):
            self.h[k] = tk.StringVar()
            ttk.Label(hb, text=label, style="CardMuted.TLabel").grid(row=1, column=i, sticky="w", padx=3)
            ttk.Entry(hb, textvariable=self.h[k], width=18 if k != "fecha" else 14).grid(
                row=2, column=i, sticky="we", padx=3)
            hb.columnconfigure(i, weight=1)

        # --- pacientes ---
        pc = ttk.Frame(body, style="Card.TFrame", padding=(14, 10, 14, 12))
        pc.pack(fill="x", padx=(0, 6), pady=(0, 12))
        gb = ttk.Frame(pc, style="Flat.TFrame")
        gb.pack(fill="x", pady=(0, 6))
        ttk.Label(gb, text="Pacientes de la hoja", style="H2.TLabel", background=theme.CARD).pack(side="left")
        ttk.Button(gb, text="+ Añadir fila", command=lambda: self._add_row()).pack(side="left", padx=10)
        ttk.Label(gb, text="Puede pegar (Ctrl+V) filas copiadas de Excel en cualquier celda.",
                  style="CardMuted.TLabel").pack(side="left")
        gh = ttk.Frame(pc, style="Flat.TFrame")
        gh.pack(fill="x")
        self.gcanvas = tk.Canvas(gh, highlightthickness=0, background=theme.CARD, height=200)
        ghs = ttk.Scrollbar(gh, orient="horizontal", command=self.gcanvas.xview)
        self.gcanvas.configure(xscrollcommand=ghs.set)
        ghs.pack(side="bottom", fill="x")
        self.gcanvas.pack(side="top", fill="x")
        self.grid_frame = ttk.Frame(self.gcanvas, style="Flat.TFrame")
        self.gcanvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", self._grid_resized)
        for c, (_, label, w) in enumerate(ata_svc.UI_COLUMNS):
            ttk.Label(self.grid_frame, text=label, style="CardMuted.TLabel", wraplength=max(w * 8, 60)
                      ).grid(row=0, column=c, sticky="w", padx=2)

    def _grid_resized(self, _event=None):
        """La tabla crece con sus filas: solo se desliza hacia los lados; hacia abajo se desliza toda la pantalla."""
        self.gcanvas.configure(scrollregion=self.gcanvas.bbox("all"), height=self.grid_frame.winfo_reqheight())

    # ------------------------------------------------------------------
    def on_show(self, **kw):
        self.refresh()
        if self.sheet_id is None and not self.cells:
            self.new(force=True)

    def refresh(self):
        sheets = ata_svc.list_sheets(self.db)
        self._sheets = {}
        labels = []
        for s in sheets:
            lab = f"{fmt_date(s['fecha']) or 'sin fecha'} · {s['establecimiento'] or 'sin establecimiento'} ({s['filas']} filas) #{s['id']}"
            self._sheets[lab] = s["id"]
            labels.append(lab)
        self.combo.set_values(labels)
        cur = next((k for k, v in self._sheets.items() if v == self.sheet_id), "")
        self.combo.set_value(cur)

    # -- estado ------------------------------------------------------------------
    def collect(self):
        return {"h": {k: v.get() for k, v in self.h.items()},
                "rows": [{k: v.get() for k, v in r.items()} for r in self.cells]}

    def _snap(self):
        data = self.collect()
        data["rows"] = [r for r in data["rows"] if any(r[k].strip() for k in ata_svc.KEYS)]
        return json.dumps(data, sort_keys=True)

    def _mark_clean(self):
        self._clean = self._snap()

    def is_dirty(self):
        return self._clean is not None and self._snap() != self._clean

    def can_leave(self):
        if not self.is_dirty():
            return True
        choice = dialogs.unsaved_changes(self, "Guardar hoja")
        if choice == "cancel":
            return False
        if choice == "save":
            return self.save()
        self._mark_clean()
        return True

    def on_save_shortcut(self):
        self.save()

    # -- tabla -------------------------------------------------------------------
    def _add_row(self, values=None):
        r = len(self.cells) + 1
        vars_ = {}
        for k, _lbl, _w in ata_svc.COLUMNS:          # lo que ya no se pide (HC, identidad, CIE…) se conserva sin mostrarse
            vars_[k] = tk.StringVar(value=(values or {}).get(k, "") or "")
        for c, (k, _, w) in enumerate(ata_svc.UI_COLUMNS):
            e = ttk.Entry(self.grid_frame, textvariable=vars_[k], width=w)
            e.grid(row=r, column=c, padx=1, pady=1)
            e.bind("<<Paste>>", lambda ev, row=len(self.cells), col=c: self._paste(row, col))
        if values is None:
            vars_["numero"].set(str(r))
        self.cells.append(vars_)

    def _clear_rows(self):
        for w in self.grid_frame.grid_slaves():
            if int(w.grid_info()["row"]) > 0:
                w.destroy()
        self.cells = []

    def _paste(self, row, col):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            return None
        if "\t" not in text and "\n" not in text.strip("\r\n"):
            return None  # pegado normal de una celda
        lines = [ln for ln in text.replace("\r", "").split("\n") if ln.strip() != ""]
        for i, ln in enumerate(lines):
            while row + i >= len(self.cells):
                self._add_row()
            for j, val in enumerate(ln.split("\t")):
                if col + j < len(ata_svc.UI_KEYS):
                    self.cells[row + i][ata_svc.UI_KEYS[col + j]].set(val.strip())
        return "break"

    # -- hojas -------------------------------------------------------------------
    def new(self, force=False):
        if not force and not self.can_leave():
            return
        self.sheet_id = None
        self.image_name = None
        for v in self.h.values():
            v.set("")
        self.h["fecha"].set(date.today().strftime("%d/%m/%Y"))
        self._clear_rows()
        for _ in range(START_ROWS):
            self._add_row()
        self.btn_delete.state(["disabled"])
        self.combo.set_value("")
        self._mark_clean()
        self.status.configure(text="")

    def _on_pick(self):
        sid = self._sheets.get(self.combo.get_value())
        if sid is None or sid == self.sheet_id:
            return
        if not self.can_leave():
            self.refresh()
            return
        self._open(sid)

    def _open(self, sid):
        sheet, rows = ata_svc.get_sheet(self.db, sid)
        if not sheet:
            return
        self.sheet_id = sid
        for k, _ in ata_svc.HEADER_FIELDS:
            v = sheet.get(k) or ""
            self.h[k].set(fmt_date(v) if k == "fecha" and v else v)
        self._clear_rows()
        for r in rows:
            vals = dict(r)
            if vals.get("fecha_nacimiento"):
                vals["fecha_nacimiento"] = fmt_date(vals["fecha_nacimiento"])
            self._add_row(vals)
        while len(self.cells) < START_ROWS:
            self._add_row()
        self.btn_delete.state(["!disabled"])
        self._mark_clean()
        self.status.configure(text="")

    def save(self):
        header, rows, errors = ata_svc.prepare_sheet(
            {k: v.get() for k, v in self.h.items()},
            [{k: v.get() for k, v in r.items()} for r in self.cells])
        if errors:
            dialogs.show_errors(self, errors)
            return False
        if not rows:
            dialogs.info(self, "La hoja no tiene ningún paciente escrito.")
            return False
        sid = ata_svc.save_sheet(self.db, header, rows, self.sheet_id, self.image_name, None)
        self.sheet_id = sid
        self._open(sid)
        self.refresh()
        self.status.configure(text=f"Guardada a las {common.now_hhmm()}: {len(rows)} pacientes en la base")
        self.hint.configure(text="Los pacientes ya están en la pestaña «Pacientes», con su botón «Añadir registro».")
        return True

    def delete(self):
        if self.sheet_id is None:
            return
        if not dialogs.confirm(self, "Eliminar hoja", "¿Eliminar esta hoja ATA y sus filas? "
                               "Las fichas de pacientes no se tocan.", yes="Eliminar", no="Cancelar",
                               danger=True):
            return
        ata_svc.delete_sheet(self.db, self.sheet_id)
        self.sheet_id = None
        self.new(force=True)
        self.refresh()

    def export(self):
        header, rows, errors = ata_svc.prepare_sheet(
            {k: v.get() for k, v in self.h.items()},
            [{k: v.get() for k, v in r.items()} for r in self.cells])
        if errors:
            dialogs.show_errors(self, errors)
            return
        if not rows:
            dialogs.info(self, "No hay pacientes para exportar.")
            return
        path = dialogs.ask_save_path(self, "Guardar ATA en Excel", initialfile=f"ATA_{date.today():%Y%m%d}.xlsx",
                                     ext=".xlsx", types=[("Excel", "*.xlsx")])
        if not path:
            return
        try:
            ata_svc.export_excel(path, header, rows)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo crear el archivo de Excel:\n{exc}")
            return
        if dialogs.confirm(self, "Excel generado", f"Se guardó:\n{path}", yes="Abrir", no="Cerrar"):
            widgets.open_path(path)

    # -- Excel -------------------------------------------------------------------
    def load_excel(self):
        if not self.can_leave():
            return
        path = dialogs.ask_open_path(self, "Elegir el ATA en Excel",
                                     [("Excel", "*.xlsx *.xlsm"), ("Todos", "*.*")])
        if not path:
            return
        try:
            header, rows, warns = ata_svc.import_excel(path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo leer el Excel:\n{exc}")
            return
        self.sheet_id = None
        self.image_name = None
        self.btn_delete.state(["disabled"])
        self.combo.set_value("")
        for k, v in self.h.items():
            v.set(header.get(k, ""))
        self._clear_rows()
        for r in rows:
            self._add_row(r)
        while len(self.cells) < START_ROWS:
            self._add_row()
        self._clean = ""  # sin guardar: pregunta antes de salir
        self.status.configure(text="")
        self.hint.configure(text=f"Se leyeron {len(rows)} filas del Excel. Revíselas y pulse "
                            "«Guardar en la base» para confirmarlas." + (" " + " ".join(warns) if warns else ""))
