"""Ficha Integral: registro, consulta y edición de los datos generales del paciente."""
import json
import tkinter as tk
from datetime import date
from tkinter import ttk

import config
import security
from reports import pdf
from services import patients as patient_svc
from services import visits as visit_svc
from services.validators import ValidationError, fmt_date, parse_date
from ui import common, dialogs, widgets
from ui.page import Page
from ui.picker import PatientPicker


class PatientPage(Page):
    nav_key = "patient"

    def __init__(self, app):
        super().__init__(app)
        self.pid = None
        self.locked = False
        self._clean = None
        self.w = {}

        head = ttk.Frame(self)
        head.pack(fill="x", pady=(0, 6))
        self.title = ttk.Label(head, text="Ficha Integral", style="H1.TLabel")
        self.title.pack(side="left")
        self.badge = ttk.Label(head, text="", style="Draft.TLabel")
        self.badge.pack(side="left", padx=14)
        self.dirty_lbl = ttk.Label(head, text="", style="Dirty.TLabel")
        self.dirty_lbl.pack(side="left")

        self.picker_box = ttk.Frame(self)
        self.picker = PatientPicker(self.picker_box, app, on_pick=app.open_patient,
                                    title="¿De qué paciente es la Ficha Integral?")
        self.picker.pack(fill="both", expand=True, pady=(12, 0))

        self.form_box = ttk.Frame(self)
        self._build_bar()
        self.scroll = widgets.ScrollFrame(self.form_box)
        self.scroll.pack(fill="both", expand=True)
        self._build_form(self.scroll.body)

    # ------------------------------------------------------------------ construcción
    def _add(self, grid, key, label, widget, **kw):
        self.w[key] = widget
        return grid.add(label, widget, **kw)

    def _build_form(self, body):
        s1 = widgets.section(body, "Identificación del paciente")
        g = widgets.FormGrid(s1, 3)
        codigo = widgets.EntryField(s1)
        codigo.state(["readonly"])
        widgets.keep_enabled(codigo)
        self._add(g, "codigo", "Código del paciente (automático)", codigo)
        self._add(g, "historia_clinica", "Número de historia clínica (si existe)",
                  widgets.EntryField(s1))
        self._add(g, "identidad", "Número de identidad (opcional)", widgets.EntryField(s1))
        g.newline()
        self._add(g, "nombres", "Nombres", widgets.EntryField(s1), required=True)
        self._add(g, "apellidos", "Apellidos", widgets.EntryField(s1), required=True)
        self._add(g, "sexo", "Sexo", widgets.ComboField(s1, patient_svc.SEXOS), required=True)
        self._add(g, "fecha_nacimiento", "Fecha de nacimiento (si se conoce)",
                  widgets.DateEntry(s1, on_change=self._recalc_age))
        age_box = ttk.Frame(s1)
        self.w["edad_valor"] = widgets.EntryField(age_box, width=7)
        self.w["edad_valor"].pack(side="left")
        self.w["edad_unidad"] = widgets.ComboField(age_box, patient_svc.UNIDADES_EDAD, width=8)
        self.w["edad_unidad"].pack(side="left", padx=(8, 0))
        self.age_hint = ttk.Label(age_box, text="", style="Hint.TLabel")
        self.age_hint.pack(side="left", padx=8)
        g.add("Edad", age_box)
        self._add(g, "telefono", "Teléfono", widgets.EntryField(s1))

        s2 = widgets.section(body, "Procedencia y estado migratorio")
        g2 = widgets.FormGrid(s2, 3)
        self._add(g2, "estado_migratorio", "Estado migratorio",
                  widgets.ComboField(s2, [], readonly=False), span=1,
                  hint="Escriba uno nuevo si no está en la lista; se guardará para la próxima vez.")
        self._add(g2, "departamento", "Departamento de procedencia",
                  widgets.ComboField(s2, [], readonly=True))
        g2.newline()
        self._add(g2, "municipio", "Municipio de procedencia",
                  widgets.ComboField(s2, [], readonly=False))
        self._add(g2, "localidad", "Localidad o comunidad", widgets.ComboField(s2, [], readonly=False))

        s3 = widgets.section(body, "Registro")
        g3 = widgets.FormGrid(s3, 3)
        date_box = ttk.Frame(s3)
        self.w["fecha_creacion"] = widgets.DateEntry(date_box, on_change=self._recalc_age)
        self.w["fecha_creacion"].pack(side="top", anchor="w")
        self.fix_date = widgets.CheckField(date_box, text="Corregir fecha de creación")
        self.fix_date.configure(command=self._toggle_fix_date)
        self.fix_date.pack(side="top", anchor="w", pady=(4, 0))
        g3.add("Fecha de creación de la Ficha Integral", date_box)
        self._add(g3, "brigade", "Brigada médica", widgets.ComboField(s3, [], width=40), span=2)
        g3.newline()
        self._add(g3, "observaciones", "Observaciones administrativas",
                  widgets.TextBox(s3, height=2), span=3)

        self.visits_box = widgets.section(body, "Atenciones de este paciente")
        top = ttk.Frame(self.visits_box)
        top.pack(fill="x")
        widgets.keep_enabled(ttk.Button(
            top, text="Nueva atención APS", style="Accent.TButton",
            command=lambda: self._new_visit("aps"))).pack(side="left")
        widgets.keep_enabled(ttk.Button(
            top, text="Nueva atención SSR", style="Accent.TButton",
            command=lambda: self._new_visit("ssr"))).pack(side="left", padx=8)
        ttk.Label(top, text="Doble clic en una fila para abrirla.", style="Hint.TLabel").pack(
            side="left", padx=8)
        frame, self.vtree = widgets.make_tree(self.visits_box, [
            ("t", "Ficha", 60), ("f", "Fecha", 100), ("e", "Estado", 100),
            ("d", "Diagnóstico principal", 330), ("p", "Personal", 200), ("b", "Brigada", 100)],
            height=5)
        frame.pack(fill="x", pady=(8, 0))
        self.vtree.bind("<Double-1>", lambda e: self._open_visit())
        self.form = body

    def _build_bar(self):
        bar = ttk.Frame(self.form_box)
        bar.pack(side="bottom", fill="x", pady=(10, 0))
        ttk.Separator(bar).pack(fill="x", pady=(0, 10))
        ttk.Button(bar, text="← Regresar", command=self.app.back).pack(side="left")
        self.btn_cancel = ttk.Button(bar, text="Cancelar cambios", command=self.cancel)
        self.btn_cancel.pack(side="left", padx=8)
        self.status = ttk.Label(bar, text="", style="Saved.TLabel")
        self.status.pack(side="left", padx=10)
        self.btn_save = ttk.Button(bar, text="Guardar", style="Accent.TButton", command=self.save)
        self.btn_save.pack(side="right")
        self.btn_edit = ttk.Button(bar, text="Editar ficha", style="Accent.TButton",
                                   command=self.unlock)
        self.btn_edit.pack(side="right")
        self.btn_print = ttk.Button(bar, text="Imprimir", command=self.print_pdf)
        self.btn_print.pack(side="right", padx=8)
        self.btn_pdf = ttk.Button(bar, text="Exportar PDF", command=self.export_pdf)
        self.btn_pdf.pack(side="right")
        self.btn_log = ttk.Button(bar, text="Ver cambios", command=self.show_log)
        self.btn_log.pack(side="right", padx=8)
        for b in (self.btn_cancel, self.btn_save, self.btn_edit, self.btn_print, self.btn_pdf,
                  self.btn_log):
            widgets.keep_enabled(b)

    # ------------------------------------------------------------------ carga
    def on_show(self, patient_id=None, new=False, **kw):
        self._fill_lists()
        if new:
            self._load_new()
        else:
            pid = patient_id or self.app.active_pid
            if pid:
                self._load(pid)
            else:
                self._show_picker()
        self._poll()

    def refresh(self):
        self._fill_lists()

    def _show_picker(self):
        self.pid = None
        self.form_box.pack_forget()
        self.picker_box.pack(fill="both", expand=True)
        self.title.configure(text="Ficha Integral")
        self.badge.configure(text="", style="Draft.TLabel")
        self.picker.start()
        self._clean = None
        self.dirty_lbl.configure(text="")

    def _show_form(self):
        self.picker_box.pack_forget()
        self.form_box.pack(fill="both", expand=True)
        self.scroll.scroll_top()

    def _fill_lists(self):
        db = self.db
        self.w["estado_migratorio"].set_values(db.catalog("estado_migratorio"))
        self.w["departamento"].set_values([""] + db.catalog("departamento"))
        self.w["municipio"].set_values(common.known_values(db, "patients", "municipio"))
        self.w["localidad"].set_values(common.known_values(db, "patients", "localidad"))
        labels, self.by_label, self.by_id = common.brigade_options(db)
        self.w["brigade"].set_values(labels)

    def _load_new(self):
        self.pid = None
        self._show_form()
        self.title.configure(text="Registrar paciente")
        self.badge.configure(text="NUEVO – sin guardar", style="Draft.TLabel")
        for k, w in self.w.items():
            w.set_value("")
        self.w["codigo"].set_value("Se genera al guardar")
        self.w["edad_unidad"].set_value("años")
        self.w["fecha_creacion"].set_value(date.today().isoformat())
        self.fix_date.set_value(False)
        bid = self.app.current_brigade_id()
        self.w["brigade"].set_value(self.by_id.get(bid, common.NO_BRIGADE))
        if bid:
            from services import brigades as brigade_svc
            b = brigade_svc.get_brigade(self.db, bid)
            for k in ("departamento", "municipio", "localidad"):
                self.w[k].set_value(b.get(k) or "")
        self.w["estado_migratorio"].set_value("")
        self._set_locked(False)
        self._recalc_age()
        self._fill_visits()
        self.status.configure(text="")
        self._mark_clean()
        self.w["nombres"].focus_field()

    def _load(self, pid):
        p = patient_svc.get_patient(self.db, pid)
        if not p:
            self._show_picker()
            return
        self.pid = pid
        self.app.set_active(pid)
        self._show_form()
        self.title.configure(text="Ficha Integral")
        self.badge.configure(text=f"Expediente {p['codigo']}", style="Final.TLabel")
        self.w["codigo"].set_value(p["codigo"])
        for k in ("historia_clinica", "identidad", "nombres", "apellidos", "sexo", "telefono",
                  "estado_migratorio", "departamento", "municipio", "localidad", "observaciones"):
            self.w[k].set_value(p.get(k) or "")
        self.w["fecha_nacimiento"].set_value(p.get("fecha_nacimiento") or "")
        self.w["edad_valor"].set_value("" if p.get("edad_valor") is None else p["edad_valor"])
        self.w["edad_unidad"].set_value(p.get("edad_unidad") or "años")
        self.w["fecha_creacion"].set_value(p["fecha_creacion"])
        self.fix_date.set_value(False)
        self.w["brigade"].set_value(self.by_id.get(p["brigade_id"], common.NO_BRIGADE))
        self._fill_visits()
        self.status.configure(text="")
        self._set_locked(True)
        self._mark_clean()

    def _fill_visits(self):
        rows = visit_svc.list_all_visits(self.db, patient_id=self.pid) if self.pid else []
        widgets.fill_tree(self.vtree, [(
            f"{v['kind']}:{v['id']}",
            (visit_svc.KIND_SHORT[v["kind"]], fmt_date(v["fecha_atencion"]),
             "Borrador" if v["estado"] == "borrador" else "Finalizada", v["dx"] or "",
             v["personal"] or "", v["brigada"] or ""),
            ["draft"] if v["estado"] == "borrador" else []) for v in rows])

    # ------------------------------------------------------------------ edad y fechas
    def _recalc_age(self):
        if self.locked:
            return
        raw = self.w["fecha_nacimiento"].get_value()
        iso = ref = None
        try:
            iso = parse_date(raw, allow_future=False)
            ref = parse_date(self.w["fecha_creacion"].get_value())
        except ValidationError:
            pass
        comp = patient_svc.calc_age(iso, ref) if iso else None
        if comp is None and iso:
            comp = patient_svc.calc_age(iso)
        ev, eu = self.w["edad_valor"], self.w["edad_unidad"]
        if comp:
            ev.set_value(comp[0])
            eu.set_value(comp[1])
            ev.state(["disabled"])
            eu.state(["disabled"])
            self.age_hint.configure(text="(calculada)")
        else:
            ev.state(["!disabled"])
            eu.state(["!disabled"])
            self.age_hint.configure(text="")

    def _toggle_fix_date(self):
        if self.fix_date.get_value():
            ok = dialogs.confirm(
                self, "Corregir fecha de creación",
                "La fecha de creación se genera automáticamente. Cámbiela solo para corregir un "
                "error de registro; el cambio quedará anotado en el historial de modificaciones.",
                yes="Permitir corrección")
            stored = self.db.get_setting("password_hash", "")
            if ok and stored:
                pw = dialogs.ask_password(self, "Autorización",
                                          "Escriba la contraseña del programa para autorizar:")
                ok = pw is not None and security.verify_password(pw, stored)
                if pw is not None and not ok:
                    dialogs.error(self, "Contraseña incorrecta.", title="Autorización")
            if not ok:
                self.fix_date.set_value(False)
        self._apply_date_lock()

    def _apply_date_lock(self):
        editable = (not self.locked) and self.fix_date.get_value()
        self.w["fecha_creacion"].entry.state(["!disabled" if editable else "disabled"])

    # ------------------------------------------------------------------ bloqueo
    def _set_locked(self, locked):
        self.locked = locked
        widgets.set_locked(self.form, locked)
        if not locked:
            self._recalc_age()
        self._apply_date_lock()
        self._buttons()

    def _buttons(self):
        existing = self.pid is not None
        self.btn_edit.pack_forget()
        self.btn_save.pack_forget()
        if self.locked:
            self.btn_edit.pack(side="right", before=self.btn_print)
            self.btn_cancel.state(["disabled"])
        else:
            self.btn_save.configure(text="Guardar cambios" if existing else "Guardar paciente")
            self.btn_save.pack(side="right", before=self.btn_print)
            self.btn_cancel.state(["!disabled"])
        if existing:
            self.visits_box.pack(fill="x", pady=(0, 12))
        else:
            self.visits_box.pack_forget()
        st = ["!disabled"] if existing else ["disabled"]
        for b in (self.btn_pdf, self.btn_print, self.btn_log):
            b.state(st)

    def unlock(self):
        self._set_locked(False)
        self.status.configure(text="")
        self.w["nombres"].focus_field()

    # ------------------------------------------------------------------ recolección
    def collect(self):
        raw = {k: w.get_value() for k, w in self.w.items() if k not in ("codigo", "brigade")}
        raw["brigade_id"] = self.by_label.get(self.w["brigade"].get_value())
        return raw

    def _mark_clean(self):
        self._clean = json.dumps(self.collect(), sort_keys=True, default=str)
        self.dirty_lbl.configure(text="")

    def is_dirty(self):
        if self._clean is None or not self.form_box.winfo_ismapped():
            return False
        return json.dumps(self.collect(), sort_keys=True, default=str) != self._clean

    def _poll(self):
        if not self.winfo_exists() or not self.winfo_ismapped():
            return
        if self.form_box.winfo_ismapped() and not self.locked:
            self.dirty_lbl.configure(text="●  Cambios sin guardar" if self.is_dirty() else "")
        self.after(600, self._poll)

    def can_leave(self):
        if self.locked or not self.is_dirty():
            return True
        choice = dialogs.unsaved_changes(self, "Guardar")
        if choice == "cancel":
            return False
        if choice == "save":
            return self.save(stay=True)
        self._mark_clean()
        return True

    def on_save_shortcut(self):
        if self.form_box.winfo_ismapped() and not self.locked:
            self.save()

    # ------------------------------------------------------------------ acciones
    def cancel(self):
        if self.locked:
            return
        if self.is_dirty() and not dialogs.confirm(
                self, "Cancelar cambios", "Se perderán los datos escritos que no haya guardado.",
                yes="Descartar cambios", no="Seguir editando", danger=True):
            return
        self._mark_clean()
        if self.pid:
            self._load(self.pid)
        else:
            self._load_new()

    def save(self, stay=False):
        raw = self.collect()
        data, errors = patient_svc.prepare_patient(raw)
        if errors:
            dialogs.show_errors(self, errors)
            return False
        warnings = []
        if data["fecha_nacimiento"] is None and data["edad_valor"] is None:
            warnings.append("No se registró la edad ni la fecha de nacimiento.")
        if warnings and not dialogs.confirm_warnings(self, warnings, "Guardar así"):
            return False
        creating = self.pid is None
        if creating:
            dups = patient_svc.find_duplicates(self.db, data)
            if dups:
                details = [f"{p['codigo']} – {patient_svc.display_name(p)} · "
                           f"{patient_svc.age_text(p) or 'edad ?'} · "
                           f"{patient_svc.procedencia(p) or 'sin procedencia'}  ({reason})"
                           for p, reason in dups]
                choice = dialogs.choose(
                    self, "Posible paciente duplicado",
                    "Ya existe un expediente parecido. Evite duplicar pacientes: si es la misma "
                    "persona, abra el expediente existente y registre ahí la nueva atención.",
                    [("cancel", "Revisar datos", "normal"), ("open", "Abrir el existente", "normal"),
                     ("create", "Es otra persona: crear", "accent")],
                    default="open", cancel="cancel", details=details)
                if choice == "cancel":
                    return False
                if choice == "open":
                    self._mark_clean()
                    if not stay:
                        self.app.open_patient(dups[0][0]["id"])
                    return True
            pid = patient_svc.create_patient(self.db, data)
        else:
            pid = self.pid
            changes = patient_svc.update_patient(self.db, pid, data)
        if data.get("estado_migratorio"):
            self.db.add_catalog("estado_migratorio", data["estado_migratorio"])
        self.app.set_active(pid)
        self._fill_lists()
        self._load(pid)
        self.status.configure(text=f"Guardado a las {common.now_hhmm()}")
        if creating and not stay:
            self._after_create(pid)
        return True

    def _after_create(self, pid):
        choice = dialogs.choose(
            self, "Paciente registrado",
            "La Ficha Integral se guardó. ¿Qué desea registrar ahora?",
            [("stay", "Ver la ficha", "normal"), ("new", "Registrar otro paciente", "normal"),
             ("ssr", "Registrar SSR", "normal"), ("aps", "Registrar APS", "accent")],
            default="aps", cancel="stay")
        if choice == "aps":
            self.app.new_visit("aps", pid)
        elif choice == "ssr":
            self.app.new_visit("ssr", pid)
        elif choice == "new":
            self.app.show("patient", new=True)

    def _new_visit(self, kind):
        if self.pid:
            self.app.new_visit(kind, self.pid)

    def _open_visit(self):
        iid = widgets.selected_iid(self.vtree)
        if iid:
            kind, vid = iid.split(":")
            self.app.open_visit(kind, int(vid))

    def show_log(self):
        if self.pid:
            dialogs.audit_log(self, "Historial de modificaciones de la Ficha Integral",
                              visit_svc.patient_audit(self.db, self.pid))

    # ------------------------------------------------------------------ PDF
    def _ensure_saved(self):
        if self.pid is None:
            dialogs.info(self, "Guarde primero la Ficha Integral para poder exportarla.")
            return False
        if not self.locked and self.is_dirty():
            choice = dialogs.choose(self, "Cambios sin guardar",
                                    "El PDF refleja lo guardado. ¿Guardar los cambios antes?",
                                    [("cancel", "Cancelar", "normal"), ("save", "Guardar y continuar", "accent")],
                                    default="save", cancel="cancel")
            if choice != "save" or not self.save(stay=True):
                return False
        return True

    def export_pdf(self):
        if not self._ensure_saved():
            return
        p = patient_svc.get_patient(self.db, self.pid)
        path = dialogs.ask_save_path(self, "Guardar Ficha Integral en PDF",
                                     initialfile=f"FichaIntegral_{p['codigo']}.pdf")
        if not path:
            return
        try:
            pdf.ficha_integral_pdf(self.db, self.pid, path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo generar el PDF:\n{exc}")
            return
        if dialogs.confirm(self, "PDF generado", f"Se guardó:\n{path}", yes="Abrir PDF", no="Cerrar"):
            widgets.open_path(path)

    def print_pdf(self):
        if not self._ensure_saved():
            return
        p = patient_svc.get_patient(self.db, self.pid)
        path = config.exports_dir() / f"imprimir_FichaIntegral_{p['codigo']}.pdf"
        try:
            pdf.ficha_integral_pdf(self.db, self.pid, path)
            widgets.open_path(path)
        except Exception as exc:  # noqa: BLE001
            dialogs.error(self, f"No se pudo preparar la impresión:\n{exc}")
