"""Hojas ATA: foto de la hoja a la vista y tabla editable para confirmar lo que se registra."""
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
        self.btn_delete = ttk.Button(bar, text="Eliminar hoja", style="Danger.TButton", command=self.delete)
        self.btn_delete.pack(side="left", padx=8)
        self.status = ttk.Label(bar, text="", style="Saved.TLabel")
        self.status.pack(side="left", padx=10)
        # segunda fila: así ningún botón queda cortado en pantallas de 1366 px
        bar2 = ttk.Frame(self)
        bar2.pack(fill="x", pady=(6, 0))
        ttk.Button(bar2, text="Subir foto", command=self.load_image).pack(side="left")
        ttk.Button(bar2, text="Subir Excel", command=self.load_excel).pack(side="left", padx=8)
        ttk.Button(bar2, text="Guardar en la base", style="Accent.TButton", command=self.save).pack(side="left")
        ttk.Button(bar2, text="Exportar Excel", command=self.export).pack(side="left", padx=8)
        self.hint = ttk.Label(self, text="", style="Hint.TLabel")
        self.hint.pack(anchor="w", pady=(4, 0))

        # Todo lo de abajo se desliza junto, como una sola pantalla (no hay barras internas verticales)
        self.scroller = widgets.ScrollFrame(self)
        self.scroller.pack(fill="both", expand=True, pady=(8, 0))
        body = self.scroller.body

        # --- foto ---
        card = ttk.Frame(body, style="Card.TFrame", padding=(14, 10, 14, 12))
        card.pack(fill="x", padx=(0, 6), pady=(0, 12))
        zb = ttk.Frame(card, style="Flat.TFrame")
        zb.pack(fill="x")
        ttk.Label(zb, text="Foto de la hoja", style="H2.TLabel", background=theme.CARD).pack(side="left")
        ttk.Button(zb, text="Acercar +", command=lambda: self._set_zoom(self._zoom * 1.25)).pack(side="right")
        ttk.Button(zb, text="Alejar –", command=lambda: self._set_zoom(self._zoom / 1.25)).pack(side="right", padx=6)
        ttk.Button(zb, text="Ajustar al ancho", command=self._fit).pack(side="right")
        self.photo_hint = ttk.Label(zb, text="Ctrl + rueda: acercar o alejar · arrastre para mover",
                                    style="CardMuted.TLabel")
        self.photo_hint.pack(side="right", padx=12)
        self.photo_hint.pack_forget()
        holder = ttk.Frame(card, style="Flat.TFrame")
        holder.pack(fill="x", pady=(8, 0))
        self.canvas = tk.Canvas(holder, background="#EEF3F4", highlightthickness=1, highlightbackground=theme.BORDER,
                                height=340, cursor="arrow")
        self.vs = ttk.Scrollbar(holder, orient="vertical", command=self.canvas.yview)
        self.hs = ttk.Scrollbar(holder, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vs.set, xscrollcommand=self.hs.set)
        self.canvas.pack(side="left", fill="x", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw_empty())
        self.canvas.bind("<Button-1>", self._canvas_click)
        self.canvas.bind("<B1-Motion>", self._canvas_drag)
        self.canvas.bind("<ButtonPress-1>", lambda e: (self.canvas.scan_mark(e.x, e.y), self._canvas_click(e)))
        self.canvas.bind("<Control-MouseWheel>", self._canvas_zoom)
        self._draw_empty()

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
        for c, (_, label, w) in enumerate(ata_svc.COLUMNS):
            ttk.Label(self.grid_frame, text=label, style="CardMuted.TLabel", wraplength=max(w * 8, 60)
                      ).grid(row=0, column=c, sticky="w", padx=2)

    def _grid_resized(self, _event=None):
        """La tabla crece con sus filas: solo se desliza hacia los lados; hacia abajo se desliza toda la pantalla."""
        self.gcanvas.configure(scrollregion=self.gcanvas.bbox("all"), height=self.grid_frame.winfo_reqheight())

    # -- zona de la foto ---------------------------------------------------------
    def _draw_empty(self):
        self.canvas.delete("hint")
        if self._pil is not None:
            return
        w = max(self.canvas.winfo_width(), 400)
        h = int(self.canvas["height"])
        self.canvas.create_rectangle(24, 24, w - 24, h - 24, outline="#9DB7BD", dash=(6, 5), width=2, tags="hint")
        self.canvas.create_text(w / 2, h / 2 - 34, text="\U0001F4F7", font=(theme.FAMILY, 34), fill="#7FA3AB", tags="hint")
        self.canvas.create_text(w / 2, h / 2 + 18, text="Haga clic aquí para subir la foto de la hoja",
                                font=theme.FONT_B, fill=theme.PRIMARY_DARK, tags="hint")
        self.canvas.create_text(w / 2, h / 2 + 44, text="JPG o PNG", font=theme.FONT_SMALL, fill=theme.MUTED, tags="hint")

    def _canvas_click(self, event):
        if self._pil is None:
            self.load_image()

    def _canvas_drag(self, event):
        if self._pil is not None:
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _canvas_zoom(self, event):
        if self._pil is not None:
            self._set_zoom(self._zoom * (1.15 if event.delta > 0 else 1 / 1.15))
        return "break"

    def _toggle_photo_bars(self, on):
        if on:
            self.vs.pack(side="right", fill="y", before=self.canvas)
            self.hs.pack(side="bottom", fill="x", before=self.canvas)
            self.canvas.configure(cursor="fleur")
            self.photo_hint.pack(side="right", padx=12)
        else:
            self.vs.pack_forget()
            self.hs.pack_forget()
            self.canvas.configure(cursor="arrow")
            self.photo_hint.pack_forget()

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
        self._show_image(None)
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
            self._toggle_photo_bars(False)
            self.canvas.configure(scrollregion=(0, 0, 0, 0))
            self._draw_empty()
            return
        try:
            from PIL import Image
            img = Image.open(path)
            img.load()
        except Exception:  # noqa: BLE001
            self._draw_empty()
            return
        if img.width > 3200:
            img = img.resize((3200, int(img.height * 3200 / img.width)))
        self._pil = img.convert("RGB")
        self.canvas.delete("hint")
        self._toggle_photo_bars(True)
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
