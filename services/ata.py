"""Hojas ATA (Atenciones Ambulatorias): captura de lo escrito en la hoja física y exportación a Excel.

No se inventa nada: solo se guarda lo que la persona escribe o pega y confirma. Las comillas de
repetición (") de la hoja se expanden con el valor de la fila anterior, solo en las columnas de
procedencia, para que el Excel salga completo.
"""
import shutil
from pathlib import Path

import config
from database import now_iso
from services.validators import ValidationError, fmt_date, parse_date

# (clave, encabezado, ancho en caracteres)
COLUMNS = [
    ("numero", "No.", 5), ("hc", "HC", 9), ("nombre", "Nombre completo", 28),
    ("identidad", "N.° de identidad", 16), ("sexo", "Sexo (H/M)", 7),
    ("fecha_nacimiento", "Fecha de nacimiento", 12),
    ("edad_anios", "Edad años", 6), ("edad_meses", "Edad meses", 6), ("edad_dias", "Edad días", 6),
    ("dep", "Departamento", 14), ("mun", "Municipio", 14), ("loc", "Localidad", 14),
    ("dx1", "Diagnóstico 1", 22), ("cie1", "CIE 1", 7),
    ("dx2", "Diagnóstico 2", 22), ("cie2", "CIE 2", 7),
    ("dx3", "Diagnóstico 3", 22), ("cie3", "CIE 3", 7),
    ("ref_enviada", "Referencia enviada", 14), ("ref_recibida", "Referencia recibida", 14),
]
KEYS = [c[0] for c in COLUMNS]
HEADER_FIELDS = [
    ("establecimiento", "Establecimiento"), ("profesional", "Profesional"),
    ("codigo", "Código"), ("tipo_establecimiento", "Tipo de establecimiento"),
    ("departamento", "Departamento"), ("municipio", "Municipio"), ("fecha", "Fecha"),
]
DITTO_KEYS = ("dep", "mun", "loc")
DITTOS = {'"', "''", "“", "”", "〃", "11", ",,"}   # «11» es como se ve la comilla de «ídem» escrita a mano
MAX_ROWS = 40


def is_ditto(value) -> bool:
    v = (value or "").strip()
    return v in DITTOS or (v and set(v) <= set('"“”\'〃') and len(v) <= 2)


def expand_ditto(rows):
    """Reemplaza las comillas de repetición por el valor de la fila anterior (solo procedencia)."""
    last = {}
    out = []
    for r in rows:
        r = dict(r)
        for k in DITTO_KEYS:
            if is_ditto(r.get(k)):
                r[k] = last.get(k, "")
            if (r.get(k) or "").strip():
                last[k] = r[k].strip()
        out.append(r)
    return out


def row_is_empty(r) -> bool:
    return not any((r.get(k) or "").strip() for k in KEYS if k != "numero")


def prepare_sheet(header: dict, rows: list):
    """Valida y normaliza. Devuelve (header, rows, errores). Las filas vacías se descartan."""
    errors = []
    h = {k: (header.get(k) or "").strip() for k, _ in HEADER_FIELDS}
    try:
        h["fecha"] = parse_date(h["fecha"], "Fecha de la hoja") or ""
    except ValidationError as exc:
        errors.append(str(exc))
    clean = []
    for i, r in enumerate(expand_ditto(rows), 1):
        r = {k: (r.get(k) or "").strip() for k in KEYS}
        if row_is_empty(r):
            continue
        tag = f"Fila {r['numero'] or i}"
        sx = r["sexo"].upper()
        if sx and sx not in ("H", "M"):
            errors.append(f"{tag}: sexo debe ser H o M.")
        r["sexo"] = sx
        if r["fecha_nacimiento"]:
            try:
                r["fecha_nacimiento"] = parse_date(r["fecha_nacimiento"], f"{tag}: fecha de nacimiento",
                                                  allow_future=False) or ""
            except ValidationError as exc:
                errors.append(str(exc))
        for k in ("edad_anios", "edad_meses", "edad_dias"):
            if r[k] and not r[k].isdigit():
                errors.append(f"{tag}: {dict((c[0], c[1]) for c in COLUMNS)[k].lower()} debe ser un número entero.")
        if not r["nombre"]:
            errors.append(f"{tag}: falta el nombre.")
        clean.append(r)
    return h, clean, errors


def save_sheet(db, header: dict, rows: list, sheet_id=None, imagen=None, brigade_id=None) -> int:
    ts = now_iso()
    prev = {}
    with db.transaction():
        if sheet_id is None:
            cur = db.execute(
                """INSERT INTO ata_sheets (fecha, establecimiento, profesional, codigo,
                       tipo_establecimiento, departamento, municipio, brigade_id, imagen,
                       created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (header["fecha"], header["establecimiento"], header["profesional"], header["codigo"],
                 header["tipo_establecimiento"], header["departamento"], header["municipio"],
                 brigade_id, imagen, ts, ts))
            sheet_id = cur.lastrowid
            db.audit("ata", sheet_id, "creación", f"Hoja ATA {header['fecha']}")
        else:
            db.execute(
                """UPDATE ata_sheets SET fecha=?, establecimiento=?, profesional=?, codigo=?,
                       tipo_establecimiento=?, departamento=?, municipio=?, brigade_id=?,
                       imagen=COALESCE(?, imagen), updated_at=? WHERE id=?""",
                (header["fecha"], header["establecimiento"], header["profesional"], header["codigo"],
                 header["tipo_establecimiento"], header["departamento"], header["municipio"],
                 brigade_id, imagen, ts, sheet_id))
            # se conserva el estado de ActivityInfo de lo ya registrado (se compara nombre + fecha nac.)
            prev = {(x["nombre"].lower(), x["fecha_nacimiento"] or "", x["numero"] or ""):
                    (x["ai_estado"], x["ai_fecha"])
                    for x in db.query("SELECT * FROM ata_rows WHERE sheet_id=?", (sheet_id,))}
            db.execute("DELETE FROM ata_rows WHERE sheet_id=?", (sheet_id,))
            db.audit("ata", sheet_id, "modificación", f"Hoja ATA {header['fecha']}")
        for n, r in enumerate(rows):
            est = prev.get((r["nombre"].lower(), r["fecha_nacimiento"] or "", r["numero"] or ""),
                           ("Pendiente", None))
            db.execute(
                f"INSERT INTO ata_rows (sheet_id, orden, {', '.join(KEYS)}, ai_estado, ai_fecha) "
                f"VALUES (?, ?, {', '.join('?' * len(KEYS))}, ?, ?)",
                (sheet_id, n, *[r[k] for k in KEYS], est[0], est[1]))
    return sheet_id


def list_records(db, texto="", estado="Todos"):
    """Un renglón por paciente/atención, con los datos de su hoja."""
    where, params = [], []
    for tok in texto.lower().split():
        where.append("(LOWER(r.nombre) LIKE ? OR LOWER(r.hc) LIKE ? OR r.identidad LIKE ?)")
        params += [f"%{tok}%"] * 3
    if estado in ("Pendiente", "Llenado", "Registrado"):
        where.append("r.ai_estado = ?")
        params.append(estado)
    sql = ("SELECT r.*, s.fecha, s.establecimiento, s.profesional, s.codigo AS cod_establecimiento, "
           "s.tipo_establecimiento, s.departamento AS dep_hoja, s.municipio AS mun_hoja "
           "FROM ata_rows r JOIN ata_sheets s ON s.id = r.sheet_id")
    if where:
        sql += " WHERE " + " AND ".join(where)
    return db.query(sql + " ORDER BY COALESCE(s.fecha,'') DESC, r.sheet_id DESC, r.orden", params)


def get_record(db, rid):
    rows = db.query("SELECT r.*, s.fecha, s.establecimiento, s.profesional, "
                    "s.codigo AS cod_establecimiento, s.tipo_establecimiento, "
                    "s.departamento AS dep_hoja, s.municipio AS mun_hoja "
                    "FROM ata_rows r JOIN ata_sheets s ON s.id = r.sheet_id WHERE r.id=?", (rid,))
    return rows[0] if rows else None


def set_llenado(db, rid):
    """El formulario ya se llenó en Chrome (falta crear la ficha a mano). No pisa un «Registrado»."""
    with db.transaction():
        db.execute("UPDATE ata_rows SET ai_estado='Llenado', ai_fecha=? WHERE id=? AND ai_estado<>'Registrado'",
                   (now_iso(), rid))
        db.audit("ata", rid, "ActivityInfo", "Formulario llenado")


def set_registered(db, rid, registered=True):
    with db.transaction():
        db.execute("UPDATE ata_rows SET ai_estado=?, ai_fecha=? WHERE id=?",
                   ("Registrado" if registered else "Pendiente", now_iso() if registered else None, rid))
        db.audit("ata", rid, "ActivityInfo", "Registrado" if registered else "Marcado pendiente")


def age_text(r) -> str:
    parts = []
    for k, u in (("edad_anios", "a"), ("edad_meses", "m"), ("edad_dias", "d")):
        if (r.get(k) or "").strip():
            parts.append(f"{r[k]} {u}")
    return " ".join(parts)


def _norm(t):
    from services.validators import normalize
    return normalize(str(t or "")).replace(".", "").strip()


_SYN = {
    "numero": ["no", "n", "numero"], "hc": ["hc", "no de historia clinica", "historia clinica", "no historia clinica"],
    "nombre": ["nombre completo", "nombres y apellidos", "nombre", "paciente"],
    "identidad": ["n de identidad", "n° de identidad", "numero de identidad", "identidad",
                  "numero de identidad del paciente", "n.° de identidad"],
    "sexo": ["sexo h/m", "sexo (h/m)", "sexo", "sexo (m/f)"],
    "fecha_nacimiento": ["fecha de nacimiento", "fecha nacimiento", "fecha de nacimiento dd/mm/aa"],
    "edad_anios": ["edad anos", "edad años", "anos", "años"], "edad_meses": ["edad meses", "meses"],
    "edad_dias": ["edad dias", "edad días", "dias", "días"],
    "dep": ["departamento"], "mun": ["municipio"], "loc": ["localidad"],
    "dx1": ["diagnostico 1", "diagnóstico 1", "dx 1", "dx1"], "cie1": ["cie 1", "cie1"],
    "dx2": ["diagnostico 2", "diagnóstico 2", "dx 2", "dx2"], "cie2": ["cie 2", "cie2"],
    "dx3": ["diagnostico 3", "diagnóstico 3", "dx 3", "dx3"], "cie3": ["cie 3", "cie3"],
    "ref_enviada": ["referencia enviada", "enviada a", "enviada"],
    "ref_recibida": ["referencia recibida", "recibida de", "recibida"],
}


def import_excel(path):
    """Lee un Excel con el formato del ATA. Devuelve (encabezado, filas, avisos).

    No guarda nada: la pantalla muestra lo leído para que la persona lo revise y confirme."""
    from datetime import date, datetime

    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    grid = [[c for c in row] for row in ws.iter_rows(values_only=True)]
    syn = {_norm(x): k for k, xs in _SYN.items() for x in xs}
    hdr_row, colmap = None, {}
    for i, row in enumerate(grid):
        m = {}
        for j, v in enumerate(row):
            k = syn.get(_norm(v))
            if k and k not in m.values():
                m[j] = k
        if "nombre" in m.values() and len(m) >= 3:
            hdr_row, colmap = i, m
            break
    if hdr_row is None:
        raise ValueError("No encontré la fila de encabezados (debe existir la columna «Nombre completo»).")
    header = {k: "" for k, _ in HEADER_FIELDS}
    labels = {_norm(lbl): k for k, lbl in HEADER_FIELDS}
    for row in grid[:hdr_row]:
        if row and row[0] is not None and _norm(row[0]) in labels and len(row) > 1 and row[1] is not None:
            v = row[1]
            header[labels[_norm(row[0])]] = v.strftime("%d/%m/%Y") if isinstance(v, (date, datetime)) else str(v)
    rows, warnings = [], []
    for row in grid[hdr_row + 1:]:
        r = {k: "" for k in KEYS}
        for j, k in colmap.items():
            v = row[j] if j < len(row) else None
            if v is None:
                continue
            if isinstance(v, (date, datetime)):
                v = v.strftime("%d/%m/%Y")
            elif isinstance(v, float) and v == int(v):
                v = int(v)
            r[k] = str(v).strip()
        if not row_is_empty(r):
            rows.append(r)
    if not rows:
        warnings.append("El archivo no tiene filas de pacientes.")
    return header, rows, warnings


def list_sheets(db):
    return db.query("""SELECT s.*, (SELECT COUNT(*) FROM ata_rows WHERE sheet_id=s.id) AS filas
                       FROM ata_sheets s ORDER BY COALESCE(s.fecha,'') DESC, s.id DESC""")


def get_sheet(db, sheet_id):
    s = db.one("SELECT * FROM ata_sheets WHERE id=?", (sheet_id,))
    if not s:
        return None, []
    rows = db.query("SELECT * FROM ata_rows WHERE sheet_id=? ORDER BY orden", (sheet_id,))
    return s, rows


def delete_sheet(db, sheet_id):
    with db.transaction():
        db.execute("DELETE FROM ata_sheets WHERE id=?", (sheet_id,))
        db.audit("ata", sheet_id, "eliminación", "Hoja ATA eliminada")


def delete_records(db, ids):
    """Quita pacientes (filas) de los ATA cargados. Devuelve cuántos se borraron."""
    ids = [int(i) for i in ids]
    with db.transaction():
        for i in ids:
            db.execute("DELETE FROM ata_rows WHERE id=?", (i,))
        if ids:
            db.audit("ata", ids[0], "eliminación", f"{len(ids)} paciente(s) del ATA eliminados")
    return len(ids)


def images_dir() -> Path:
    d = Path(config.data_dir()) / "ata_imagenes"
    d.mkdir(parents=True, exist_ok=True)
    return d


def store_image(src_path) -> str:
    """Copia la foto de la hoja a la carpeta de datos del programa y devuelve el nombre."""
    src = Path(src_path)
    dest = images_dir() / f"{now_iso().replace(':', '').replace(' ', '_').replace('-', '')}_{src.name}"
    shutil.copy2(src, dest)
    return dest.name


def image_path(name):
    return str(images_dir() / name) if name else None


def export_excel(path, header: dict, rows: list):
    """Excel con las columnas de la hoja ATA (una fila por paciente)."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active
    ws.title = "ATA"
    ws.append(["ATA – Atenciones Ambulatorias"])
    ws["A1"].font = Font(bold=True, size=14)
    for k, label in HEADER_FIELDS:
        v = header.get(k) or ""
        ws.append([label, fmt_date(v) if k == "fecha" and v else v])
        ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.append([])
    start = ws.max_row + 1
    ws.append([c[1] for c in COLUMNS])
    for i, (_, _, w) in enumerate(COLUMNS, 1):
        cell = ws.cell(start, i)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = max(w, len(COLUMNS[i - 1][1]) + 2)
    for r in rows:
        vals = []
        for k in KEYS:
            v = r.get(k) or ""
            if k == "fecha_nacimiento" and v:
                v = fmt_date(v)
            vals.append(v)
        ws.append(vals)
    ws.freeze_panes = ws.cell(start + 1, 4)
    wb.save(path)
