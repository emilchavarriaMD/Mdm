"""Generación de las tres fichas en PDF (A4): Ficha Integral, APS y SSR.

El PDF refleja SOLO lo registrado: los campos vacíos se muestran como
"Pendiente / no registrado" y nunca se completan con datos ficticios.
"""
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from config import APP_NAME, DISCLAIMER
from services import patients as patient_svc
from services.clinical import APS_HEA_FIELDS, SSR_HEA_FIELDS
from services import visits as visit_svc
from services.validators import fmt_date, fmt_number

PRIMARY = colors.HexColor("#0F6E7C")
LIGHT = colors.HexColor("#E8F3F5")
GRID = colors.HexColor("#B8C7CC")
GREY = colors.HexColor("#5F6B70")
PENDING_COLOR = "#8A8F92"

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
PENDING = "— Pendiente / no registrado —"

S_LABEL = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=GREY)
S_VAL = ParagraphStyle("val", fontName="Helvetica", fontSize=9.2, leading=11.8)
S_CELL = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.4)
S_CELL_B = ParagraphStyle("cellb", parent=S_CELL, fontName="Helvetica-Bold")
S_HEAD = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white)
S_SECTION = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=colors.white)
S_NOTE = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=GREY)
S_WARN = ParagraphStyle("warn", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                        textColor=colors.HexColor("#8A4B00"))


def esc(text) -> str:
    return escape(str(text)).replace("\n", "<br/>")


def _blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def val_par(value, style=S_VAL):
    if _blank(value):
        return Paragraph(f'<font color="{PENDING_COLOR}"><i>{PENDING}</i></font>', style)
    return Paragraph(esc(value), style)


class _NumberedCanvas(canvas.Canvas):
    """Encabezado y pie con 'Página x de y'."""

    def __init__(self, *args, header=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._header = header or {}
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._decorate(total)
            super().showPage()
        super().save()

    def _decorate(self, total):
        h = self._header
        self.saveState()
        self.setFillColor(PRIMARY)
        self.rect(0, PAGE_H - 24 * mm, PAGE_W, 24 * mm, stroke=0, fill=1)
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 13)
        self.drawString(MARGIN, PAGE_H - 11 * mm, h.get("institucion", ""))
        self.setFont("Helvetica", 8.5)
        self.drawString(MARGIN, PAGE_H - 16 * mm, h.get("subtitulo", ""))
        self.setFont("Helvetica-Bold", 10.5)
        self.drawRightString(PAGE_W - MARGIN, PAGE_H - 11 * mm, h.get("titulo", ""))
        self.setFont("Helvetica", 8.5)
        self.drawRightString(PAGE_W - MARGIN, PAGE_H - 16 * mm, h.get("derecha", ""))
        self.setStrokeColor(GRID)
        self.line(MARGIN, 14 * mm, PAGE_W - MARGIN, 14 * mm)
        self.setFillColor(GREY)
        self.setFont("Helvetica-Oblique", 7)
        self.drawString(MARGIN, 10 * mm, DISCLAIMER)
        self.setFont("Helvetica", 8)
        self.drawRightString(PAGE_W - MARGIN, 10 * mm, f"Página {self._pageNumber} de {total}")
        self.restoreState()


def header_settings(db):
    return (db.get_setting("encabezado_institucion", "Brigada Médica"),
            db.get_setting("encabezado_subtitulo", ""))


def _section(title):
    t = Table([[Paragraph(esc(title.upper()), S_SECTION)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
    return [Spacer(1, 4 * mm), t, Spacer(1, 1.5 * mm)]


def _kv_grid(pairs, ncols=2):
    lw = 32 * mm if ncols == 2 else 26 * mm
    vw = (CONTENT_W / ncols) - lw
    rows, row = [], []
    for label, value in pairs:
        if not label:  # celda de relleno para completar la fila
            row += ["", ""]
        else:
            row += [Paragraph(esc(label), S_LABEL), val_par(value)]
        if len(row) == ncols * 2:
            rows.append(row)
            row = []
    if row:
        row += [""] * (ncols * 2 - len(row))
        rows.append(row)
    t = Table(rows, colWidths=[lw, vw] * ncols)
    style = [("GRID", (0, 0), (-1, -1), 0.4, GRID), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    for c in range(0, ncols * 2, 2):
        style.append(("BACKGROUND", (c, 0), (c, -1), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def _text_block(label, text, note=None):
    cells = [[Paragraph(esc(label), S_LABEL)], [val_par(text)]]
    if note:
        cells.insert(1, [Paragraph(esc(note), S_WARN)])
    t = Table(cells, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.4, GRID),
                           ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def _table(headers, rows, widths):
    data = [[Paragraph(esc(h), S_HEAD) for h in headers]]
    for r in rows:
        data.append([c if not isinstance(c, str) else val_par(c, S_CELL) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREY), ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFB")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def _plain(text, style=S_CELL):
    return Paragraph(esc(text), style)


def _signature(responsable):
    t = Table([[_plain(" "), _plain(" ")],
               [Paragraph(esc("Profesional responsable: " + (responsable or "______________________")), S_CELL),
                Paragraph("Firma y sello", S_CELL)]],
              colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.38], rowHeights=[16 * mm, None])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (0, -1), 12)]))
    return KeepTogether([Spacer(1, 6 * mm), t])


def _build(path, header, story):
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=30 * mm, bottomMargin=20 * mm, title=header.get("titulo", ""),
                            author=APP_NAME)
    doc.build(story, canvasmaker=lambda *a, **k: _NumberedCanvas(*a, header=header, **k))
    return path


def _patient_block(p, ref_iso=None):
    return [
        ("Código de expediente", p["codigo"]),
        ("Historia clínica", p.get("historia_clinica")),
        ("Paciente", patient_svc.display_name(p)),
        ("Edad", patient_svc.age_text(p, ref_iso)),
        ("Sexo", p.get("sexo")),
        ("Procedencia", patient_svc.procedencia(p)),
    ]


def _vitals_table(main):
    items = [("PAS", "mmHg", "pas"), ("PAD", "mmHg", "pad"), ("FC", "lpm", "fc"),
             ("FR", "rpm", "fr"), ("Temperatura", "°C", "temperatura"), ("Peso", "kg", "peso")]
    head = [Paragraph(f"{esc(n)} ({esc(u)})", S_HEAD) for n, u, _ in items]
    vals = []
    for _, _, k in items:
        v = main.get(k)
        vals.append(Paragraph(esc(fmt_number(v)), S_CELL_B) if v is not None else
                    Paragraph(f'<font color="{PENDING_COLOR}"><i>No registrado</i></font>', S_CELL))
    t = Table([head, vals], colWidths=[CONTENT_W / 6] * 6)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREY), ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                           ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    out = [t]
    if main.get("vitales_nota"):
        out += [Spacer(1, 1.5 * mm), _text_block("Observaciones / justificación de valores", main["vitales_nota"])]
    return out


def _exam_table(kind, exam):
    labels = visit_svc.REGION_LABELS[kind]
    rows = []

    def add(region, indent=False):
        e = exam.get(region)
        label = labels.get(region, region)
        if indent:
            label = "    - " + label.replace("Abdomen – ", "")
        if e is None:
            estado, texto = visit_svc.EXAM_PENDIENTE, ""
        else:
            estado, texto = e["estado"], e["hallazgos"]
        if indent and e is None:
            return
        if indent and not texto and estado == visit_svc.EXAM_PENDIENTE:
            return
        estado_par = (Paragraph(f'<font color="{PENDING_COLOR}"><i>{esc(estado)}</i></font>', S_CELL)
                      if estado == visit_svc.EXAM_PENDIENTE else _plain(estado))
        rows.append([_plain(label, S_CELL_B if not indent else S_CELL), estado_par,
                     val_par(texto, S_CELL) if (texto or estado in (visit_svc.EXAM_ANORMAL,)) else
                     _plain("—" if estado != visit_svc.EXAM_PENDIENTE else "")])

    for region, _ in visit_svc.REGIONS[kind]:
        add(region)
        if region == "abdomen":
            for sub, _ in visit_svc.ABDOMEN_SUB:
                add(sub, indent=True)
    return _table(["Región / sistema", "Estado", "Hallazgos"], rows,
                  [52 * mm, 36 * mm, CONTENT_W - 88 * mm])


def _dx_table(dx):
    if not dx:
        return val_par("")
    rows = []
    for d in dx:
        cie = d["cie11"] or ""
        if cie:
            cie += "" if d["cie11_verificado"] else " (sin verificar)"
        rows.append([_plain("Principal" if d["tipo"] == "principal" else "Secundario", S_CELL_B),
                     _plain(d["descripcion"]), _plain(cie or "—"), _plain(d["observaciones"] or "—")])
    return _table(["Tipo", "Descripción", "CIE-11", "Observaciones"], rows,
                  [24 * mm, 70 * mm, 32 * mm, CONTENT_W - 126 * mm])


def _meds_table(meds):
    if not meds:
        return Paragraph(f'<font color="{PENDING_COLOR}"><i>Sin medicamentos registrados.</i></font>', S_VAL)
    rows = []
    for m in meds:
        unidad = f" {m['unidad']}" if m["unidad"] else ""
        presc = f"{fmt_number(m['cant_prescrita'])}{unidad}" if m["cant_prescrita"] is not None else "No registrada"
        entr = f"{fmt_number(m['cant_entregada'])}{unidad}" if m["cant_entregada"] is not None else "No registrada"
        name = f"<b>{esc(m['generico'])}</b>" + (f"<br/>{esc(m['presentacion'])}" if m["presentacion"] else "")
        freq = " / ".join(x for x in (m["frecuencia"], m["horario"]) if x)
        rows.append([Paragraph(name, S_CELL), _plain(m["dosis"] or "—"), _plain(m["via"] or "—"),
                     _plain(freq or "—"), _plain(m["duracion"] or "—"), _plain(presc), _plain(entr),
                     _plain(m["indicaciones"] or "—")])
    return _table(["Medicamento / presentación", "Dosis", "Vía", "Frecuencia / horario", "Duración",
                   "Cant. prescrita", "Cant. entregada", "Indicaciones"], rows,
                  [38 * mm, 18 * mm, 16 * mm, 24 * mm, 17 * mm, 20 * mm, 20 * mm,
                   CONTENT_W - 153 * mm])


def _estado_label(main):
    return "FICHA FINALIZADA" if main["estado"] == visit_svc.ESTADO_FINAL else \
        "BORRADOR – FICHA INCOMPLETA"


# ---------------------------------------------------------------------------
# Ficha Integral
# ---------------------------------------------------------------------------

def ficha_integral_pdf(db, patient_id, path):
    p = patient_svc.get_patient(db, patient_id)
    if not p:
        raise ValueError("Paciente no encontrado")
    inst, sub = header_settings(db)
    header = {"institucion": inst, "subtitulo": sub, "titulo": "FICHA INTEGRAL",
              "derecha": f"Expediente {p['codigo']}"}
    story = []
    story += _section("Identificación del paciente")
    story.append(_kv_grid([
        ("Código de expediente", p["codigo"]), ("Historia clínica", p.get("historia_clinica")),
        ("Nombres", p["nombres"]), ("Apellidos", p["apellidos"]),
        ("Edad", patient_svc.age_text(p)), ("Fecha de nacimiento", fmt_date(p.get("fecha_nacimiento"))),
        ("Sexo", p.get("sexo")), ("Teléfono", p.get("telefono")),
        ("Estado migratorio", p.get("estado_migratorio")), ("", ""),
    ]))
    story += _section("Procedencia")
    story.append(_kv_grid([("Departamento", p.get("departamento")), ("Municipio", p.get("municipio")),
                           ("Localidad / comunidad", p.get("localidad")), ("", "")]))
    story += _section("Datos administrativos")
    brig = f"{p['brigada_codigo']} – {p['brigada_nombre']}" if p.get("brigada_codigo") else None
    story.append(_kv_grid([("Fecha de creación", fmt_date(p["fecha_creacion"])), ("Brigada médica", brig)]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(_text_block("Observaciones administrativas", p.get("observaciones")))

    story += _section("Atenciones registradas")
    visits = visit_svc.list_all_visits(db, patient_id=patient_id)
    if visits:
        rows = [[_plain(fmt_date(v["fecha_atencion"])), _plain(v["kind"].upper(), S_CELL_B),
                 _plain(v["dx"] or "Sin diagnóstico registrado"), _plain(v["personal"] or "—"),
                 _plain("Finalizada" if v["estado"] == "finalizada" else "Borrador")] for v in visits]
        story.append(_table(["Fecha", "Tipo", "Diagnóstico principal", "Personal médico", "Estado"], rows,
                            [24 * mm, 14 * mm, 70 * mm, 46 * mm, CONTENT_W - 154 * mm]))
    else:
        story.append(Paragraph(f'<font color="{PENDING_COLOR}"><i>Aún no hay atenciones registradas.</i></font>', S_VAL))
    story.append(_signature(None))
    return _build(path, header, story)


# ---------------------------------------------------------------------------
# APS
# ---------------------------------------------------------------------------

def _hea_aps_story(m):
    story = []
    note = None
    if m["hea_origen"] == "plantilla" and not m["hea_revisada"]:
        note = "HEA generada con plantilla y SIN revisión médica confirmada."
    text = m.get("hea_texto")
    if text:
        story.append(_text_block("Historia de la Enfermedad Actual", text, note))
        return story
    fields = [(lbl, m.get(k)) for k, lbl, _ in APS_HEA_FIELDS]
    present = [(l, v) for l, v in fields if not _blank(v)]
    if present:
        story.append(_kv_grid(present, ncols=1))
    else:
        story.append(_text_block("Historia de la Enfermedad Actual", None))
    return story


def aps_pdf(db, visit_id, path):
    v = visit_svc.get_visit(db, "aps", visit_id)
    if not v:
        raise ValueError("Atención APS no encontrada")
    m = v["main"]
    p = patient_svc.get_patient(db, m["patient_id"])
    brig = db.one("SELECT codigo, nombre FROM brigades WHERE id=?", (m["brigade_id"],)) if m["brigade_id"] else None
    inst, sub = header_settings(db)
    header = {"institucion": inst, "subtitulo": sub,
              "titulo": "FICHA DE ATENCIÓN PRIMARIA EN SALUD (APS)",
              "derecha": f"Expediente {p['codigo']} · {fmt_date(m['fecha_atencion'])}"}
    story = []
    story.append(Paragraph(_estado_label(m), S_WARN if m["estado"] != "finalizada" else
                           ParagraphStyle("ok", parent=S_WARN, textColor=PRIMARY)))
    story += _section("Identificación del paciente")
    story.append(_kv_grid(_patient_block(p, m["fecha_atencion"])))
    story += _section("Datos de la atención")
    mismo = m["mismo_dia_ficha"] + (" (corregido manualmente)" if m["mismo_dia_manual"] else "")
    story.append(_kv_grid([
        ("Fecha de atención", fmt_date(m["fecha_atencion"])), ("Personal médico", m.get("personal")),
        ("Brigada", f"{brig['codigo']} – {brig['nombre']}" if brig else None), ("Lugar de atención", m.get("lugar")),
        ("Historia clínica", m.get("historia_clinica") or p.get("historia_clinica")),
        ("Fecha de creación de la Ficha Integral", fmt_date(p["fecha_creacion"])),
        ("¿APS el mismo día de creación de la Ficha Integral?", mismo), ("", ""),
    ]))
    if m.get("observaciones"):
        story += [Spacer(1, 1.5 * mm), _text_block("Observaciones clínicas", m["observaciones"])]

    story += _section("Historia de la enfermedad actual (HEA)")
    story += _hea_aps_story(m)
    story += _section("Signos vitales")
    story += _vitals_table(m)
    story += _section("Examen físico (orden cefalocaudal)")
    story.append(_exam_table("aps", v["exam"]))
    story += _section("Diagnósticos")
    story.append(_dx_table(v["dx"]))
    story += _section("Plan terapéutico")
    story.append(_meds_table(v["meds"]))
    story.append(Spacer(1, 2 * mm))
    cons = m["consejeria_estado"]
    cons_note = {"Realizada": "Consejería brindada (confirmada por el personal médico).",
                 "No realizada": "Consejería NO realizada.",
                 "Pendiente": "Consejería pendiente de confirmar: el texto siguiente es solo una sugerencia no confirmada."}[cons]
    story.append(_text_block("Consejería: signos de alarma", m.get("consejeria_alarma"), cons_note))
    for label, key in (("Recomendaciones generales", "recomendaciones"),
                       ("Medidas no farmacológicas", "medidas_no_farm"), ("Seguimiento", "seguimiento")):
        story += [Spacer(1, 1.5 * mm), _text_block(label, m.get(key))]
    story += [Spacer(1, 1.5 * mm), _kv_grid([("Fecha sugerida de control", fmt_date(m.get("fecha_control"))),
                                             ("Referencia a otro establecimiento", m.get("referencia"))])]
    story.append(_signature(m.get("personal")))
    return _build(path, header, story)


# ---------------------------------------------------------------------------
# SSR
# ---------------------------------------------------------------------------

def aps_same_day_text(m):
    return m["mismo_dia_aps"] + (" (corregido manualmente)" if m["mismo_dia_manual"] else "")


def ssr_pdf(db, visit_id, path):
    v = visit_svc.get_visit(db, "ssr", visit_id)
    if not v:
        raise ValueError("Atención SSR no encontrada")
    m = v["main"]
    p = patient_svc.get_patient(db, m["patient_id"])
    brig = db.one("SELECT codigo, nombre FROM brigades WHERE id=?", (m["brigade_id"],)) if m["brigade_id"] else None
    inst, sub = header_settings(db)
    header = {"institucion": inst, "subtitulo": sub,
              "titulo": "FICHA DE SALUD SEXUAL Y REPRODUCTIVA (SSR)",
              "derecha": f"Expediente {p['codigo']} · {fmt_date(m['fecha_atencion'])}"}
    story = [Paragraph(_estado_label(m), S_WARN if m["estado"] != "finalizada" else
                       ParagraphStyle("ok", parent=S_WARN, textColor=PRIMARY))]
    story += _section("Identificación del paciente")
    story.append(_kv_grid(_patient_block(p, m["fecha_atencion"])))
    story += _section("Datos de la atención")
    story.append(_kv_grid([
        ("Fecha de atención", fmt_date(m["fecha_atencion"])), ("Personal médico", m.get("personal")),
        ("Brigada", f"{brig['codigo']} – {brig['nombre']}" if brig else None), ("Lugar de atención", m.get("lugar")),
        ("Categoría de atención", m.get("categoria")), ("¿SSR el mismo día que APS?", aps_same_day_text(m)),
    ]))
    story += [Spacer(1, 1.5 * mm), _text_block("Motivo de consulta", m.get("motivo"))]
    if m.get("observaciones"):
        story += [Spacer(1, 1.5 * mm), _text_block("Observaciones", m["observaciones"])]

    story += _section("Historia de la enfermedad actual (HEA) – SSR")
    note = None
    if m["hea_origen"] == "plantilla" and not m["hea_revisada"]:
        note = "HEA generada con plantilla y SIN revisión médica confirmada."
    if m.get("hea_texto"):
        story.append(_text_block("HEA", m["hea_texto"], note))
    else:
        pairs = []
        for key, label in SSR_HEA_FIELDS:
            value = m.get(key)
            if key in ("fum", "hea_fecha_ultima_dosis"):
                value = fmt_date(value)
            if not _blank(value):
                pairs.append((label, value))
        story.append(_kv_grid(pairs, ncols=1) if pairs else _text_block("HEA", None))

    story += _section("Signos vitales")
    story += _vitals_table(m)
    story += _section("Examen físico y evaluación clínica")
    story.append(_exam_table("ssr", v["exam"]))
    story += _section("Pruebas realizadas")
    if v["tests"]:
        rows = [[_plain(t["prueba"], S_CELL_B), _plain(t["estado"]), _plain(t["resultado"] or "—"),
                 _plain(t["motivo"] or "—")] for t in v["tests"]]
        story.append(_table(["Prueba", "Estado", "Resultado", "Motivo si no se realizó"], rows,
                            [42 * mm, 26 * mm, 52 * mm, CONTENT_W - 120 * mm]))
    else:
        story.append(Paragraph(f'<font color="{PENDING_COLOR}"><i>Sin pruebas registradas '
                               '(no se asume que se hayan realizado).</i></font>', S_VAL))
    story += _section("Diagnósticos")
    story.append(_dx_table(v["dx"]))
    story += _section("Plan terapéutico")
    story.append(_meds_table(v["meds"]))
    story.append(Spacer(1, 2 * mm))
    unidad = f" {m['metodo_unidad']}" if m.get("metodo_unidad") else ""
    cant = (fmt_number(m["metodo_cantidad"]) + unidad) if m.get("metodo_cantidad") is not None else None
    story.append(_kv_grid([
        ("Método anticonceptivo entregado / administrado", m.get("metodo_entregado")),
        ("Presentación", m.get("metodo_presentacion")),
        ("Cantidad", cant), ("Fecha de administración", fmt_date(m.get("fecha_administracion"))),
        ("Próxima dosis prevista", fmt_date(m.get("fecha_proxima_dosis"))), ("", ""),
    ]))
    story += _section("Intervenciones y consejería")
    rows = []
    for tipo in visit_svc.SSR_INTERVENCIONES:
        e = v["interventions"].get(tipo, {"estado": "Pendiente", "nota": ""})
        rows.append([_plain(tipo, S_CELL_B), _plain(e["estado"]), _plain(e["nota"] or "—")])
    story.append(_table(["Intervención", "Estado", "Nota"], rows, [76 * mm, 28 * mm, CONTENT_W - 104 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(_text_block("Signos de alarma", m.get("signos_alarma"),
                             None if v["interventions"].get("Consejería: signos de alarma", {}).get("estado") == "Realizada"
                             else "Consejería sobre signos de alarma no confirmada como realizada."))
    for label, key in (("Recomendaciones", "recomendaciones"), ("Seguimiento", "seguimiento")):
        story += [Spacer(1, 1.5 * mm), _text_block(label, m.get(key))]
    story += [Spacer(1, 1.5 * mm), _kv_grid([("Fecha sugerida de control", fmt_date(m.get("fecha_control"))),
                                             ("Referencia", m.get("referencia"))])]
    story.append(_signature(m.get("personal")))
    return _build(path, header, story)
