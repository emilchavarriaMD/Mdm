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
    ("telefono", "Teléfono", 13), ("obst", "Gestas, partos, cesáreas, abortos, HV, HM", 34),
]
KEYS = [c[0] for c in COLUMNS]
# Lo que se ve en la pantalla «Cargar ATA»: las columnas de la plantilla ATA-2023, en su orden
# (HC, identidad, códigos CIE y referencias se conservan en la base, pero ya no se piden)
UI_KEYS = ["numero", "nombre", "telefono", "sexo", "fecha_nacimiento", "edad_anios", "edad_meses", "edad_dias",
           "dep", "mun", "loc", "dx1", "dx2", "dx3", "obst"]
_CMAP = {c[0]: c for c in COLUMNS}
UI_COLUMNS = [_CMAP[k] for k in UI_KEYS]
UI_COLUMNS = [(k, {"obst": "G, P, C, A, HV, HM", "dx1": "Diagnóstico 1", "telefono": "Teléfono"}.get(k, l), w)
              for k, l, w in UI_COLUMNS]
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
    filas = [{k: (r.get(k) or "").strip() for k in KEYS} for r in expand_ditto(rows)]
    normalizar_sexos(filas)                       # masculino/femenino, F, palabras… -> H o M
    for i, r in enumerate(filas, 1):
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
                    (x["ai_estado"], x["ai_fecha"], x.get("ai_datos"))
                    for x in db.query("SELECT * FROM ata_rows WHERE sheet_id=? AND borrado_en IS NULL", (sheet_id,))}
            db.execute("DELETE FROM ata_rows WHERE sheet_id=? AND borrado_en IS NULL", (sheet_id,))
            db.audit("ata", sheet_id, "modificación", f"Hoja ATA {header['fecha']}")
        for n, r in enumerate(rows):
            est = prev.get((r["nombre"].lower(), r["fecha_nacimiento"] or "", r["numero"] or ""),
                           ("Pendiente", None, None))
            db.execute(
                f"INSERT INTO ata_rows (sheet_id, orden, {', '.join(KEYS)}, ai_estado, ai_fecha, ai_datos) "
                f"VALUES (?, ?, {', '.join('?' * len(KEYS))}, ?, ?, ?)",
                (sheet_id, n, *[r[k] for k in KEYS], est[0], est[1], est[2]))
    return sheet_id


def list_records(db, texto="", estado="Todos"):
    """Un renglón por paciente/atención, con los datos de su hoja."""
    where, params = ["r.borrado_en IS NULL"], []
    for tok in texto.lower().split():
        where.append("(LOWER(r.nombre) LIKE ? OR LOWER(r.hc) LIKE ? OR r.identidad LIKE ? OR LOWER(r.dx1) LIKE ? "
                     "OR LOWER(r.dx2) LIKE ? OR LOWER(r.dx3) LIKE ?)")
        params += [f"%{tok}%"] * 6
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


def save_datos(db, rid, datos: dict):
    """Guarda lo que se revisó en la ventana «Añadir registro» para poder volver a verlo después."""
    import json
    with db.transaction():
        db.execute("UPDATE ata_rows SET ai_datos=? WHERE id=?", (json.dumps(datos, ensure_ascii=False), rid))


def load_datos(db, rid):
    """Lo guardado con save_datos (dict) o None si todavía no hay registro."""
    import json
    rows = db.query("SELECT ai_datos FROM ata_rows WHERE id=?", (rid,))
    try:
        return json.loads(rows[0]["ai_datos"]) if rows and rows[0]["ai_datos"] else None
    except ValueError:
        return None


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
    "fecha_nacimiento": ["fecha de nacimiento", "fecha nacimiento", "fecha de nacimiento dd/mm/aa",
                         "fecha de nacimiento (dd/mm/aa)"],
    "edad_anios": ["edad anos", "edad años", "anos", "años"], "edad_meses": ["edad meses", "meses"],
    "edad_dias": ["edad dias", "edad días", "dias", "días"],
    "dep": ["departamento"], "mun": ["municipio"], "loc": ["localidad"],
    "dx1": ["diagnostico 1", "diagnóstico 1", "dx 1", "dx1"], "cie1": ["cie 1", "cie1"],
    "dx2": ["diagnostico 2", "diagnóstico 2", "dx 2", "dx2"], "cie2": ["cie 2", "cie2"],
    "dx3": ["diagnostico 3", "diagnóstico 3", "dx 3", "dx3"], "cie3": ["cie 3", "cie3"],
    "ref_enviada": ["referencia enviada", "enviada a", "enviada"],
    "ref_recibida": ["referencia recibida", "recibida de", "recibida"],
    "telefono": ["telefono", "numero de telefono", "n de telefono", "n° de telefono", "celular", "numero de celular"],
    "obst": ["gestas partos cesareas abortos hv hm", "gestas, partos, cesareas, abortos, hv, hm", "historia ginecoobstetrica",
             "gestas partos cesareas abortos hijos vivos hijos muertos", "gpcahvhm", "g p c a hv hm"],
}
# encabezados de dos y tres filas (plantilla ATA-2023): se juntan el texto de arriba y el de abajo
_SYN_JUNTOS = {
    "edad_anios": ["edad anos"], "edad_meses": ["edad meses"], "edad_dias": ["edad dias"],
    "dep": ["procedencia departamento"], "mun": ["procedencia municipio"], "loc": ["procedencia localidad"],
    "dx1": ["diagnostico / actividad 1", "diagnostico actividad 1"], "dx2": ["diagnostico / actividad 2", "diagnostico actividad 2"],
    "dx3": ["diagnostico / actividad 3", "diagnostico actividad 3"],
}
_SUBENCABEZADOS = {"1", "2", "3", "anos", "meses", "dias", "departamento", "municipio", "localidad"}
_ETIQUETAS_ENCABEZADO = [("establecimiento", "establecimiento"), ("codigo", "codigo"),
                         ("tipo de establecimiento", "tipo_establecimiento"), ("departamento", "departamento"),
                         ("municipio", "municipio"), ("fecha", "fecha"), ("nombre", "profesional")]


def _anio2(texto, nacimiento=False):
    """«15/10/26» -> «15/10/2026» (para nacimientos, el año de dos cifras es del 1900 si pasaría de hoy)."""
    import re as _re
    from datetime import date as _d
    m = _re.fullmatch(r"\s*(\d{1,2})[/-](\d{1,2})[/-](\d{2})\s*", str(texto or ""))
    if not m:
        return texto
    yy = int(m.group(3))
    hoy = _d.today().year % 100
    anio = (2000 + yy) if (not nacimiento or yy <= hoy) else (1900 + yy)
    return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}/{anio}"


_SEXO_PALABRAS = {"HOMBRE": "H", "MASCULINO": "H", "MASC": "H", "VARON": "H", "VARÓN": "H", "MALE": "H", "H": "H",
                  "MUJER": "M", "FEMENINO": "M", "FEM": "M", "FEMENINA": "M", "FEMALE": "M", "F": "M"}


def normalizar_sexos(rows):
    """Deja el sexo de cada fila como H (hombre) o M (mujer). Acepta H/M, M/F (masculino/femenino) y palabras
    (hombre, mujer, masculino, femenino…). Una «M» sola es mujer, salvo en una hoja que usa «F» (no menos que «M») y no usa
    «H» (M/F): ahí M = masculino. Devuelve cuántos valores se cambiaron de significado (M masculino -> H, F -> M)."""
    vals = [str(r.get("sexo") or "").strip().upper() for r in rows]
    # M/F de verdad (M = masculino) solo si hay «F», no hay «H» y las «F» no son menos que las «M» (en una hoja de H/M con una
    # «F» de error, la «M» sigue siendo mujer)
    mf = "F" in vals and "H" not in vals and vals.count("F") >= vals.count("M")
    cambios = 0
    for r, v in zip(rows, vals):
        if not v:
            continue
        if v == "M":
            nuevo = "H" if mf else "M"
        else:
            nuevo = _SEXO_PALABRAS.get(v) or _SEXO_PALABRAS.get(v.rstrip(".")) or v
        if nuevo != v:
            cambios += 1
        r["sexo"] = nuevo
    return cambios


def parse_obst(texto):
    """«G=2 P=1 C=1 A=0 HV=3 HM=0» -> {'G': 2, 'P': 1, 'C': 1, 'A': 0, 'HV': 3, 'HM': 0} (solo lo que trae número)."""
    import re as _re
    out = {}
    for k, v in _re.findall(r"\b(HV|HM|G|P|C|A)\s*[=:]\s*(\d+)", str(texto or "").upper()):
        out[k] = int(v)
    return out


def fmt_obst(d):
    return " ".join(f"{k}={d[k]}" for k in ("G", "P", "C", "A", "HV", "HM") if k in d)


def import_excel(path):
    """Lee un Excel con el formato del ATA (el de columnas simples o la plantilla ATA-2023 con encabezados de varias
    filas, teléfono y gestas/partos/cesáreas/abortos). Devuelve (encabezado, filas, avisos).

    No guarda nada: la pantalla muestra lo leído para que la persona lo revise y confirme."""
    from datetime import date, datetime

    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    grid = [[c for c in row] for row in ws.iter_rows(values_only=True)]
    # copia con las celdas combinadas repetidas en todo su rango (solo para leer encabezados)
    relleno = [list(r) for r in grid]
    for mr in ws.merged_cells.ranges:
        v = grid[mr.min_row - 1][mr.min_col - 1] if mr.min_row - 1 < len(grid) and mr.min_col - 1 < len(grid[0]) else None
        for rr in range(mr.min_row - 1, mr.max_row):
            for cc in range(mr.min_col - 1, mr.max_col):
                if rr < len(relleno) and cc < len(relleno[rr]):
                    relleno[rr][cc] = v
    syn = {_norm(x): k for k, xs in _SYN.items() for x in xs}
    juntos = {_norm(x): k for k, xs in _SYN_JUNTOS.items() for x in xs}
    hdr_row = None
    for i, row in enumerate(grid):
        m = {}
        for j, v in enumerate(row):
            k = syn.get(_norm(v))
            if k and k not in m.values():
                m[j] = k
        if "nombre" in m.values() and len(m) >= 3:
            hdr_row = i
            break
    if hdr_row is None:
        raise ValueError("No encontré la fila de encabezados (debe existir la columna «Nombre completo»).")
    # filas de subencabezado (edad: años/meses/días; procedencia: departamento…; diagnóstico 1/2/3)
    colmap0 = {j: syn[_norm(v)] for j, v in enumerate(grid[hdr_row]) if syn.get(_norm(v))}
    num_col = next((j for j, k in colmap0.items() if k == "numero"), None)
    nom_col = next(j for j, k in colmap0.items() if k == "nombre")
    data_start = hdr_row + 1
    for i in range(hdr_row + 1, min(hdr_row + 4, len(grid))):
        row = grid[i]
        celdas = [(j, v) for j, v in enumerate(row) if v is not None and str(v).strip()]
        if (celdas and (num_col is None or not str(row[num_col] if num_col < len(row) and row[num_col] is not None else "").strip())
                and not (nom_col < len(row) and row[nom_col])
                and all(_norm(v) in _SUBENCABEZADOS for _j, v in celdas)):
            data_start = i + 1
        else:
            break
    # texto de encabezado de cada columna = lo de arriba + lo de abajo (con celdas combinadas)
    colmap = {}
    for j in range(max(len(r) for r in grid)):
        partes = []
        for i in range(hdr_row, data_start):
            v = relleno[i][j] if j < len(relleno[i]) else None
            t = str(v).strip() if v is not None else ""
            if t and t not in partes:
                partes.append(t)
        k = juntos.get(_norm(" ".join(partes))) or syn.get(_norm(partes[0] if partes else "")) \
            or (syn.get(_norm(" ".join(partes))) if partes else None)
        if k and k not in colmap.values():
            colmap[j] = k
    sexo_mf = any("m/f" in str(grid[hdr_row][j] or "").lower().replace(" ", "")
                  for j, k in colmap.items() if k == "sexo")
    header = {k: "" for k, _ in HEADER_FIELDS}
    labels = {_norm(lbl): k for k, lbl in HEADER_FIELDS}
    for row in grid[:hdr_row]:                                  # formato simple: etiqueta en la columna A, valor en la B
        if row and row[0] is not None and _norm(row[0]) in labels and len(row) > 1 and row[1] is not None:
            v = row[1]
            header[labels[_norm(row[0])]] = v.strftime("%d/%m/%Y") if isinstance(v, (date, datetime)) else str(v)
    etiquetas = dict(_ETIQUETAS_ENCABEZADO)
    for row in grid[:hdr_row]:                                  # plantilla: «Etiqueta:» y su valor a la derecha o después de «:»
        for j, v in enumerate(row):
            if not isinstance(v, str) or ":" not in v:
                continue
            ant, _, desp = v.partition(":")
            nombre = _norm(ant)
            nombre = "fecha" if nombre.startswith("fecha") else nombre
            if nombre not in etiquetas:                          # (p. ej. «Profesional De Salud: MG» no es el nombre)
                continue
            k = etiquetas[nombre]
            val = desp.strip()
            if not val:
                for w in row[j + 1:]:
                    if w is None or (isinstance(w, str) and not w.strip()):
                        continue
                    if isinstance(w, str) and ":" in w and _norm(w.partition(":")[0]) in list(etiquetas) + ["fecha dd/mm/aa"]:
                        break
                    val = w.strftime("%d/%m/%Y") if isinstance(w, (date, datetime)) else str(w).strip()
                    break
            if val and not header[k]:
                header[k] = val
    header["fecha"] = _anio2(header["fecha"])
    rows, warnings = [], []
    for row in grid[data_start:]:
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
        r["fecha_nacimiento"] = _anio2(r["fecha_nacimiento"], nacimiento=True)
        if r["obst"]:
            r["obst"] = fmt_obst(parse_obst(r["obst"]))         # «G=    P=   …» sin números = vacío
        if not row_is_empty(r):
            rows.append(r)
    sx = {str(r.get("sexo") or "").strip().upper() for r in rows}
    cambios = normalizar_sexos(rows)
    if "F" in sx and "M" in sx and "H" not in sx:
        warnings.append("La hoja mezcla M y F sin H: revise el sexo de cada paciente (M puede ser mujer o masculino).")
    if cambios:
        warnings.append(f"Se corrigió el sexo de {cambios} fila(s) a H (hombre) o M (mujer) "
                        "(venía como masculino/femenino, F o palabras). Verifique el sexo.")
    if not rows:
        warnings.append("El archivo no tiene filas de pacientes.")
    return header, rows, warnings


def list_sheets(db):
    return db.query("""SELECT s.*, (SELECT COUNT(*) FROM ata_rows WHERE sheet_id=s.id AND borrado_en IS NULL) AS filas
                       FROM ata_sheets s ORDER BY COALESCE(s.fecha,'') DESC, s.id DESC""")


def get_sheet(db, sheet_id):
    s = db.one("SELECT * FROM ata_sheets WHERE id=?", (sheet_id,))
    if not s:
        return None, []
    rows = db.query("SELECT * FROM ata_rows WHERE sheet_id=? AND borrado_en IS NULL ORDER BY orden", (sheet_id,))
    return s, rows


def delete_sheet(db, sheet_id):
    with db.transaction():
        db.execute("DELETE FROM ata_sheets WHERE id=?", (sheet_id,))
        db.audit("ata", sheet_id, "eliminación", "Hoja ATA eliminada")


def delete_records(db, ids):
    """Manda pacientes (filas) de los ATA cargados a la papelera (se pueden recuperar). Devuelve cuántos."""
    ids = [int(i) for i in ids]
    with db.transaction():
        for i in ids:
            db.execute("UPDATE ata_rows SET borrado_en=? WHERE id=?", (now_iso(), i))
        if ids:
            db.audit("ata", ids[0], "eliminación", f"{len(ids)} paciente(s) del ATA enviados a la papelera")
    return len(ids)


def list_papelera(db):
    return db.query("SELECT r.*, s.fecha FROM ata_rows r JOIN ata_sheets s ON s.id = r.sheet_id "
                    "WHERE r.borrado_en IS NOT NULL ORDER BY r.borrado_en DESC, r.id")


def restore_records(db, ids):
    ids = [int(i) for i in ids]
    with db.transaction():
        for i in ids:
            db.execute("UPDATE ata_rows SET borrado_en=NULL WHERE id=?", (i,))
        if ids:
            db.audit("ata", ids[0], "restauración", f"{len(ids)} paciente(s) recuperados de la papelera")
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
    """Excel con la distribución de la plantilla ATA-2023 (la misma que se sube con «Subir Excel»)."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, Side
    wb = Workbook()
    ws = wb.active
    ws.title = "ATA-2023"
    fino = Side(style="thin")
    borde = Border(left=fino, right=fino, top=fino, bottom=fino)
    centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws["A1"], ws["F1"], ws["O1"], ws["P1"], ws["Q1"] = ("SECRETARIA DE SALUD", "ATENCIONES AMBULATORIAS",
                                                         "SERVICIO DE\nATENCIÓN:", "Consulta Externa ☐", "Emergencia ☐")
    ws["A2"], ws["P2"], ws["Q2"] = "DEPARTAMENTO DE ESTADÍSTICA", "Filtro ☐", "Especialidad: Med General"
    ws["A3"] = "HONDURAS C. A."
    ws["A5"], ws["D5"], ws["J5"], ws["M5"], ws["O5"] = ("Establecimiento:", "Código:", "Tipo De Establecimiento:",
                                                       "Departamento:", "Municipio:")
    ws["A6"], ws["M6"] = "Profesional De Salud: MG", "Fecha (dd/mm/aa):"
    ws["C6"] = "Nombre: " + (header.get("profesional") or "")
    ws["C5"], ws["F5"], ws["L5"] = header.get("establecimiento") or "", header.get("codigo") or "", header.get("tipo_establecimiento") or ""
    ws["N5"], ws["P5"] = header.get("departamento") or "", header.get("municipio") or ""
    f = header.get("fecha") or ""
    ws["N6"] = fmt_date(f) if f else ""
    ws["A7"], ws["B7"], ws["C7"], ws["D7"] = "N°", "NOMBRES Y APELLIDOS", "NÚMERO DE TELEFONO", "SEXO (M/F)"
    ws["E7"], ws["F7"], ws["I7"], ws["J7"] = "FECHA DE NACIMIENTO (dd/mm/aa)", "EDAD", "PACIENTE", "PROCEDENCIA"
    ws["M7"], ws["P7"] = "DIAGNÓSTICO / ACTIVIDAD", "Gestas, partos, cesareas, abortos, HV, HM"
    ws["M8"], ws["N8"], ws["O8"] = "1", "2", "3"
    ws["F9"], ws["G9"], ws["H9"], ws["J9"], ws["K9"], ws["L9"] = "AÑOS", "MESES", "DÍAS", "DEPARTAMENTO", "MUNICIPIO", "LOCALIDAD"
    n = max(20, len(rows))
    for rng in ("A1:C1", "A2:C2", "A3:C3", "F1:N3", "O1:O3", "A5:B5", "D5:E5", "J5:K5", "P5:Q5", "A6:B6", "C6:L6",
                "A7:A9", "B7:B9", "C7:C9", "D7:D9", "E7:E9", "F7:H8", "I7:I9", "J7:L8", "M7:O7", "M8:M9", "N8:N9",
                "O8:O9", "P7:Q9") + tuple(f"P{10 + i}:Q{10 + i}" for i in range(n)):
        ws.merge_cells(rng)
    for r in range(7, 10):
        for c in range(1, 18):
            ws.cell(r, c).alignment = centro
            ws.cell(r, c).font = Font(bold=True, size=9)
    cols = {"numero": "A", "nombre": "B", "telefono": "C", "sexo": "D", "fecha_nacimiento": "E", "edad_anios": "F",
            "edad_meses": "G", "edad_dias": "H", "dep": "J", "mun": "K", "loc": "L", "dx1": "M", "dx2": "N", "dx3": "O",
            "obst": "P"}
    for i in range(n):
        r = 10 + i
        datos = rows[i] if i < len(rows) else {}
        for k, col in cols.items():
            v = datos.get(k) or ""
            if k == "numero":
                v = v or i + 1
            elif k == "fecha_nacimiento" and v:
                v = fmt_date(v)
            elif k == "obst" and not v:
                v = "G=    P=    C=    A=    HV=    HM=   "
            ws[f"{col}{r}"] = v
        for c in range(1, 18):
            ws.cell(r, c).border = borde
    for col, w in {"A": 4, "B": 34, "C": 15, "D": 7, "E": 14, "F": 6, "G": 7, "H": 6, "I": 9, "J": 13, "K": 13, "L": 16,
                   "M": 22, "N": 22, "O": 22, "P": 22, "Q": 16}.items():
        ws.column_dimensions[col].width = w
    wb.save(path)
