"""Hojas ATA: foto de la hoja a la vista y tabla editable para confirmar lo que se registra."""
import json
import tkinter as tk
from datetime import date
from tkinter import ttk

from services import ata as ata_svc
from services.validators import fmt_date
from ui import common, dialogs, widgets
from ui.page import Page

START_ROWS = 20


class AtaPage(Page):
    nav_key = "ata"

    def __init__(self, app):
        super().__init__(app)
        self.sheet_id = None
        self.image_name = None
        self._pil = None
        self._photo = None
        self._zoom = 1.0
        self._clean = None
        self.cells = []          # filas: {clave: StringVar}
        self.h = {}              # encabezado: {clave: StringVar}
        self._sheets = {}

        ttk.Label(self, text="Hojas ATA (Atenciones Ambulatorias)", style="H1.TLabel").pack(anchor="w")
        ttk.Label(self, text="Cargue la foto de la hoja, escriba o pegue los datos en la tabla y "
                  "confírmelos. Nada se llena solo. Las comillas (\") en departamento, municipio y "
                  "localidad se repiten desde la fila anterior.", style="Muted.TLabel",
                  wraplength=1000, justify="left").pack(anchor="w", pady=(0, 6))

        bar = ttk.Frame(self)
        bar.pack(fill="x")
        ttk.Label(bar, text="Hoja:").pack(side="left")
        self.combo = widgets.ComboField(bar, [], readonly=True)
        self.combo.configure(width=26)
        self.combo.pack(side="left", padx=(6, 8))
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._on_pick())
        ttk.Button(bar, text="+ Nueva hoja", command=self.new).pack(side="left")
        ttk.Button(bar, text="Cargar foto", command=self.load_image).pack(side="left", padx=8)
        ttk.Button(bar, text="Guardar", style="Accent.TButton", command=self.save).pack(side="left")
        ttk.Button(bar, text="Exportar Excel", command=self.export).pack(side="left", padx=8)
        self.btn_delete = ttk.Button(bar, text="Eliminar", style="Danger.TButton", command=self.delete)
        self.btn_delete.pack(side="left")
        self.status = ttk.Label(bar, text="", style="Saved.TLabel")
        self.status.pack(side="left", padx=10)

        pane = ttk.PanedWindow(self, orient="vertical")
        pane.pack(fill="both", expand=True, pady=(8, 0))

        # --- foto ---
        top = ttk.Frame(pane)
        pane.add(top, weight=2)
        zb = ttk.Frame(top)
        zb.pack(fill="x")
        ttk.Label(zb, text="Foto de la hoja", style="H2.TLabel").pack(side="left")
        ttk.Button(zb, text="Acercar +", command=lambda: self._set_zoom(self._zoom * 1.25)).pack(
            side="right")
        ttk.Button(zb, text="Alejar –", command=lambda: self._set_zoom(self._zoom / 1.25)).pack(
            side="right", padx=6)
        ttk.Button(zb, text="Ajustar al ancho", command=self._fit).pack(side="right")
        holder = ttk.Frame(top)
        holder.pack(fill="both", expand=True, pady=(4, 0))
        self.canvas = tk.Canvas(holder, background="#2b2b2b", highlightthickness=0, height=260)
        vs = ttk.Scrollbar(holder, orient="vertical", command=self.canvas.yview)
        hs = ttk.Scrollbar(holder, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        vs.pack(side="right", fill="y")
        hs.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_text(20, 20, anchor="nw", fill="#bbbbbb", tags="hint",
                                text="Aún no hay foto. Use «Cargar foto…» (JPG o PNG).")

        # --- datos ---
        bottom = ttk.Frame(pane)
        pane.add(bottom, weight=3)
        hb = ttk.LabelFrame(bottom, text=" Encabezado de la hoja ", padding=(8, 2, 8, 6))
        hb.pack(fill="x")
        for i, (k, label) in enumerate(ata_svc.HEADER_FIELDS):
            self.h[k] = tk.StringVar()
            ttk.Label(hb, text=label, style="Muted.TLabel").grid(row=0, column=i, sticky="w", padx=3)
            ttk.Entry(hb, textvariable=self.h[k], width=18 if k != "fecha" else 14).grid(
                row=1, column=i, sticky="we", padx=3)
            hb.columnconfigure(i, weight=1)
        gb = ttk.Frame(bottom)
        gb.pack(fill="x", pady=(6, 2))
        ttk.Label(gb, text="Pacientes de la hoja", style="H2.TLabel").pack(side="left")
        ttk.Button(gb, text="+ Añadir fila", command=lambda: self._add_row()).pack(side="left", padx=10)
        ttk.Label(gb, text="Puede pegar (Ctrl+V) filas copiadas de Excel en cualquier celda.",
                  style="Hint.TLabel").pack(side="left")
        gh = ttk.Frame(bottom)
        gh.pack(fill="both", expand=True)
        self.gcanvas = tk.Canvas(gh, highlightthickness=0, background="#ffffff")
        gvs = ttk.Scrollbar(gh, orient="vertical", command=self.gcanvas.yview)
        ghs = ttk.Scrollbar(gh, orient="horizontal", command=self.gcanvas.xview)
        self.gcanvas.configure(yscrollcommand=gvs.set, xscrollcommand=ghs.set)
        gvs.pack(side="right", fill="y")
        ghs.pack(side="bottom", fill="x")
        self.gcanvas.pack(side="left", fill="both", expand=True)
        self.grid_frame = ttk.Frame(self.gcanvas)
        self.gcanvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e: self.gcanvas.configure(
            scrollregion=self.gcanvas.bbox("all")))
        for c, (_, label, w) in enumerate(ata_svc.COLUMNS):
            ttk.Label(self.grid_frame, text=label, style="Muted.TLabel", wraplength=max(w * 8, 60)
                      ).grid(row=0, column=c, sticky="w", padx=2)

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
        for c, (k, _, w) in enumerate(ata_svc.COLUMNS):
            var = tk.StringVar(value=(values or {}).get(k, "") or "")
            e = ttk.Entry(self.grid_frame, textvariable=var, width=w)
            e.grid(row=r, column=c, padx=1, pady=1)
            e.bind("<<Paste>>", lambda ev, row=len(self.cells), col=c: self._paste(row, col))
            vars_[k] = var
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
                if col + j < len(ata_svc.KEYS):
                    self.cells[row + i][ata_svc.KEYS[col + j]].set(val.strip())
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
        self._show_image(None)
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
        self.image_name = sheet.get("imagen")
        self._show_image(ata_svc.image_path(self.image_name))
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
        sid = ata_svc.save_sheet(self.db, header, rows, self.sheet_id, self.image_name,
                                 self.app.current_brigade_id())
        self.sheet_id = sid
        self._open(sid)
        self.refresh()
        self.status.configure(text=f"Hoja guardada a las {common.now_hhmm()} ({len(rows)} pacientes)")
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

    # -- foto --------------------------------------------------------------------
    def load_image(self):
        path = dialogs.ask_open_path(self, "Elegir foto de la hoja ATA",
                                     [("Imágenes", "*.jpg *.jpeg *.png *.bmp"), ("Todos", "*.*")])
        if not path:
            return
        try:
            self.image_name = ata_svc.store_image(path)
            self._show_image(ata_svc.image_path(self.image_name))
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo abrir la imagen:\n{exc}")

    def _show_image(self, path):
        self._pil = None
        self.canvas.delete("img")
        if not path:
            self.canvas.itemconfigure("hint", state="normal")
            self.canvas.configure(scrollregion=(0, 0, 0, 0))
            return
        try:
            from PIL import Image
            img = Image.open(path)
            img.load()
        except Exception:  # noqa: BLE001
            self.canvas.itemconfigure("hint", state="normal")
            return
        if img.width > 3200:
            img = img.resize((3200, int(img.height * 3200 / img.width)))
        self._pil = img.convert("RGB")
        self.canvas.itemconfigure("hint", state="hidden")
        self.after(150, self._fit)

    def _fit(self):
        if self._pil is None:
            return
        self.update_idletasks()
        w = self.canvas.winfo_width()
        if w < 100:  # aún sin dibujar: reintenta
            self.after(150, self._fit)
            return
        self._set_zoom((w - 4) / self._pil.width)

    def _set_zoom(self, z):
        if self._pil is None:
            return
        self._zoom = max(0.1, min(z, 4.0))
        from PIL import Image, ImageTk
        w, h = int(self._pil.width * self._zoom), int(self._pil.height * self._zoom)
        self._photo = ImageTk.PhotoImage(self._pil.resize((max(w, 1), max(h, 1)), Image.LANCZOS))
        self.canvas.delete("img")
        self.canvas.create_image(0, 0, anchor="nw", image=self._photo, tags="img")
        self.canvas.configure(scrollregion=(0, 0, w, h))
