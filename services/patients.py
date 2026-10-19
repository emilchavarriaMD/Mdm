"""Gestión de pacientes (Ficha Integral): alta, edición, duplicados y búsqueda."""
import difflib
from datetime import date, datetime

from database import now_iso
from services.validators import (ValidationError, digits, fmt_date, normalize, parse_date,
                                 parse_number)

SEXOS = ["Femenino", "Masculino", "Otro"]
UNIDADES_EDAD = ["años", "meses", "días"]

PATIENT_FIELDS = ["historia_clinica", "nombres", "apellidos", "fecha_nacimiento", "edad_valor",
                  "edad_unidad", "sexo", "telefono", "estado_migratorio", "departamento",
                  "municipio", "localidad", "fecha_creacion", "brigade_id", "observaciones"]


# -- edad ---------------------------------------------------------------------

def calc_age(fecha_nacimiento_iso, ref_iso=None):
    """Devuelve (valor, unidad) calculado desde la fecha de nacimiento, o None."""
    if not fecha_nacimiento_iso:
        return None
    try:
        born = datetime.strptime(fecha_nacimiento_iso[:10], "%Y-%m-%d").date()
        ref = datetime.strptime(ref_iso[:10], "%Y-%m-%d").date() if ref_iso else date.today()
    except ValueError:
        return None
    if born > ref:
        return None
    years = ref.year - born.year - ((ref.month, ref.day) < (born.month, born.day))
    if years >= 1:
        return years, "años"
    months = (ref.year - born.year) * 12 + ref.month - born.month - (ref.day < born.day)
    if months >= 1:
        return months, "meses"
    return (ref - born).days, "días"


def age_text(patient, ref_iso=None) -> str:
    """Texto de edad: calculada de la fecha de nacimiento si existe; si no, la registrada."""
    computed = calc_age(patient.get("fecha_nacimiento"), ref_iso)
    if computed:
        return f"{computed[0]} {computed[1]}"
    if patient.get("edad_valor") is not None:
        return f"{patient['edad_valor']} {patient.get('edad_unidad') or 'años'}"
    return ""


def display_name(p) -> str:
    return f"{p['nombres']} {p['apellidos']}".strip()


def procedencia(p) -> str:
    parts = [p.get("localidad"), p.get("municipio"), p.get("departamento")]
    return ", ".join(x for x in parts if x)


# -- validación y conversión -----------------------------------------------------

def prepare_patient(raw: dict):
    """Convierte lo ingresado en el formulario a valores de BD. Devuelve (datos, errores)."""
    errors, data = [], {}
    data["historia_clinica"] = (raw.get("historia_clinica") or "").strip()
    data["nombres"] = (raw.get("nombres") or "").strip()
    data["apellidos"] = (raw.get("apellidos") or "").strip()
    if not data["nombres"]:
        errors.append("Nombres: campo obligatorio.")
    if not data["apellidos"]:
        errors.append("Apellidos: campo obligatorio.")

    try:
        data["fecha_nacimiento"] = parse_date(raw.get("fecha_nacimiento"),
                                              "Fecha de nacimiento", allow_future=False)
    except ValidationError as exc:
        errors.append(str(exc))
        data["fecha_nacimiento"] = None
    try:
        data["fecha_creacion"] = parse_date(raw.get("fecha_creacion"), "Fecha de creación",
                                            allow_future=False)
        if not data["fecha_creacion"]:
            errors.append("Fecha de creación: campo obligatorio.")
    except ValidationError as exc:
        errors.append(str(exc))
        data["fecha_creacion"] = None

    if data["fecha_nacimiento"]:
        ref = data.get("fecha_creacion") or None
        computed = calc_age(data["fecha_nacimiento"], ref)
        if computed is None:
            errors.append("Fecha de nacimiento: es posterior a la fecha de creación de la ficha.")
            data["edad_valor"], data["edad_unidad"] = None, "años"
        else:
            data["edad_valor"], data["edad_unidad"] = computed
    else:
        unidad = raw.get("edad_unidad") or "años"
        maximos = {"años": 120, "meses": 36, "días": 365}
        try:
            val = parse_number(raw.get("edad_valor"), "Edad", minimum=0,
                               maximum=maximos.get(unidad, 120))
            data["edad_valor"] = int(val) if val is not None else None
            if val is not None and val != int(val):
                errors.append("Edad: debe ser un número entero.")
        except ValidationError as exc:
            errors.append(str(exc))
            data["edad_valor"] = None
        data["edad_unidad"] = unidad if unidad in UNIDADES_EDAD else "años"
        if data["edad_valor"] is None and not errors:
            pass  # edad desconocida: permitido, se advierte en la interfaz

    sexo = (raw.get("sexo") or "").strip()
    data["sexo"] = sexo if sexo in SEXOS else ""
    if not data["sexo"]:
        errors.append("Sexo: seleccione una opción.")

    tel = (raw.get("telefono") or "").strip()
    if tel and not (7 <= len(digits(tel)) <= 15):
        errors.append("Teléfono: debe tener entre 7 y 15 dígitos.")
    data["telefono"] = tel
    for key in ("estado_migratorio", "departamento", "municipio", "localidad", "observaciones"):
        data[key] = (raw.get(key) or "").strip()
    brigade = raw.get("brigade_id")
    data["brigade_id"] = int(brigade) if brigade not in (None, "") else None
    return data, errors


# -- CRUD ---------------------------------------------------------------------------

def _row_values(data):
    return {**data,
            "nombre_norm": normalize(f"{data['apellidos']} {data['nombres']}"),
            "telefono_norm": digits(data.get("telefono"))}


def create_patient(db, data: dict) -> int:
    values = _row_values(data)
    ts = now_iso()
    with db.transaction():
        cur = db.execute(
            """INSERT INTO patients (codigo, historia_clinica, nombres, apellidos, nombre_norm,
                   fecha_nacimiento, edad_valor, edad_unidad, sexo, telefono, telefono_norm,
                   estado_migratorio, departamento, municipio, localidad, fecha_creacion,
                   brigade_id, observaciones, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            ("TEMP", values["historia_clinica"], values["nombres"], values["apellidos"],
             values["nombre_norm"], values["fecha_nacimiento"], values["edad_valor"],
             values["edad_unidad"], values["sexo"], values["telefono"], values["telefono_norm"],
             values["estado_migratorio"], values["departamento"], values["municipio"],
             values["localidad"], values["fecha_creacion"], values["brigade_id"],
             values["observaciones"], ts, ts))
        pid = cur.lastrowid
        db.execute("UPDATE patients SET codigo=? WHERE id=?", (f"P{pid:06d}", pid))
        db.audit("paciente", pid, "creación",
                 f"{values['nombres']} {values['apellidos']}", patient_id=pid)
    return pid


def get_patient(db, pid):
    return db.one("""SELECT p.*, b.codigo AS brigada_codigo, b.nombre AS brigada_nombre
                     FROM patients p LEFT JOIN brigades b ON b.id = p.brigade_id
                     WHERE p.id=?""", (pid,))


_LABELS = {
    "historia_clinica": "Historia clínica", "nombres": "Nombres", "apellidos": "Apellidos",
    "fecha_nacimiento": "Fecha de nacimiento", "edad_valor": "Edad", "edad_unidad": "Unidad de edad",
    "sexo": "Sexo", "telefono": "Teléfono", "estado_migratorio": "Estado migratorio",
    "departamento": "Departamento", "municipio": "Municipio", "localidad": "Localidad",
    "fecha_creacion": "Fecha de creación", "brigade_id": "Brigada", "observaciones": "Observaciones",
}


def update_patient(db, pid: int, data: dict) -> list:
    """Actualiza la Ficha Integral sin tocar las atenciones. Devuelve la lista de cambios."""
    old = get_patient(db, pid)
    if not old:
        raise ValueError("Paciente no encontrado")
    values = _row_values(data)
    changes = []
    for key in PATIENT_FIELDS:
        a, b = old.get(key), values.get(key)
        if (a or "") != (b or "") and str(a) != str(b):
            changes.append(f"{_LABELS[key]}: '{a if a is not None else ''}' → '{b if b is not None else ''}'")
    with db.transaction():
        db.execute(
            """UPDATE patients SET historia_clinica=?, nombres=?, apellidos=?, nombre_norm=?,
                   fecha_nacimiento=?, edad_valor=?, edad_unidad=?, sexo=?, telefono=?,
                   telefono_norm=?, estado_migratorio=?, departamento=?, municipio=?, localidad=?,
                   fecha_creacion=?, brigade_id=?, observaciones=?, updated_at=? WHERE id=?""",
            (values["historia_clinica"], values["nombres"], values["apellidos"],
             values["nombre_norm"], values["fecha_nacimiento"], values["edad_valor"],
             values["edad_unidad"], values["sexo"], values["telefono"], values["telefono_norm"],
             values["estado_migratorio"], values["departamento"], values["municipio"],
             values["localidad"], values["fecha_creacion"], values["brigade_id"],
             values["observaciones"], now_iso(), pid))
        if changes:
            db.audit("paciente", pid, "modificación", "; ".join(changes), patient_id=pid)
    return changes


# -- duplicados ----------------------------------------------------------------------

def find_duplicates(db, data: dict, exclude_id=None):
    """Posibles duplicados: [(paciente, motivo)]. No bloquea; la interfaz pregunta."""
    found = {}
    name_norm = normalize(f"{data.get('apellidos', '')} {data.get('nombres', '')}")
    tel = digits(data.get("telefono"))
    hc = (data.get("historia_clinica") or "").strip()
    rows = db.query("SELECT * FROM patients")
    for p in rows:
        if exclude_id and p["id"] == exclude_id:
            continue
        reasons = []
        if hc and p["historia_clinica"] and hc.lower() == p["historia_clinica"].strip().lower():
            reasons.append("misma historia clínica")
        if tel and tel == p["telefono_norm"]:
            reasons.append("mismo teléfono")
        if name_norm:
            if name_norm == p["nombre_norm"]:
                reasons.append("mismo nombre y apellidos")
            else:
                ratio = difflib.SequenceMatcher(None, name_norm, p["nombre_norm"]).ratio()
                if ratio >= 0.88:
                    reasons.append("nombre muy parecido")
        if reasons:
            found[p["id"]] = (p, ", ".join(reasons))
    return list(found.values())


# -- búsqueda -----------------------------------------------------------------------

TIPOS_FICHA = ["Todos", "Solo Ficha Integral (sin atenciones)", "Con APS", "Con SSR",
               "Con APS y SSR"]


def search_patients(db, texto="", fecha_desde=None, fecha_hasta=None, brigade_id=None,
                    diagnostico="", tipo_ficha="Todos", limit=500):
    where, params = [], []
    for token in normalize(texto).split():
        like = f"%{token}%"
        where.append("(p.nombre_norm LIKE ? OR LOWER(p.codigo) LIKE ? "
                     "OR LOWER(COALESCE(p.historia_clinica,'')) LIKE ? "
                     "OR COALESCE(p.telefono_norm,'') LIKE ?)")
        params += [like, like, like, like]
    if fecha_desde or fecha_hasta:
        cond = []
        sub = []
        if fecha_desde:
            cond.append("fecha_atencion >= ?")
            sub.append(fecha_desde)
        if fecha_hasta:
            cond.append("fecha_atencion <= ?")
            sub.append(fecha_hasta)
        c = " AND ".join(cond)
        where.append(f"(EXISTS (SELECT 1 FROM aps_visits WHERE patient_id=p.id AND {c}) "
                     f"OR EXISTS (SELECT 1 FROM ssr_visits WHERE patient_id=p.id AND {c}))")
        params += sub + sub
    if brigade_id:
        where.append("(p.brigade_id = ? OR EXISTS (SELECT 1 FROM aps_visits WHERE patient_id=p.id AND brigade_id=?) "
                     "OR EXISTS (SELECT 1 FROM ssr_visits WHERE patient_id=p.id AND brigade_id=?))")
        params += [brigade_id] * 3
    dx = normalize(diagnostico)
    if dx:
        like = f"%{dx}%"
        where.append("(EXISTS (SELECT 1 FROM aps_dx d JOIN aps_visits v ON v.id=d.visit_id "
                     "WHERE v.patient_id=p.id AND (d.descripcion_norm LIKE ? OR LOWER(COALESCE(d.cie11,'')) LIKE ?)) "
                     "OR EXISTS (SELECT 1 FROM ssr_dx d JOIN ssr_visits v ON v.id=d.visit_id "
                     "WHERE v.patient_id=p.id AND (d.descripcion_norm LIKE ? OR LOWER(COALESCE(d.cie11,'')) LIKE ?)))")
        params += [like] * 4
    if tipo_ficha == "Solo Ficha Integral (sin atenciones)":
        where.append("aps_n = 0 AND ssr_n = 0")
    elif tipo_ficha == "Con APS":
        where.append("aps_n > 0")
    elif tipo_ficha == "Con SSR":
        where.append("ssr_n > 0")
    elif tipo_ficha == "Con APS y SSR":
        where.append("aps_n > 0 AND ssr_n > 0")
    clause = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
        SELECT * FROM (
            SELECT p.*, b.codigo AS brigada_codigo,
                   (SELECT COUNT(*) FROM aps_visits WHERE patient_id=p.id) AS aps_n,
                   (SELECT COUNT(*) FROM ssr_visits WHERE patient_id=p.id) AS ssr_n,
                   (SELECT MAX(f) FROM (SELECT MAX(fecha_atencion) AS f FROM aps_visits WHERE patient_id=p.id
                                        UNION ALL SELECT MAX(fecha_atencion) FROM ssr_visits WHERE patient_id=p.id)) AS ultima
            FROM patients p LEFT JOIN brigades b ON b.id = p.brigade_id
        ) p {clause} ORDER BY p.created_at DESC, p.id DESC LIMIT {int(limit)}"""
    return db.query(sql, params)


def patient_counts(db, pid):
    return (db.scalar("SELECT COUNT(*) FROM aps_visits WHERE patient_id=?", (pid,)),
            db.scalar("SELECT COUNT(*) FROM ssr_visits WHERE patient_id=?", (pid,)))


def count_patients(db) -> int:
    return db.scalar("SELECT COUNT(*) FROM patients")
