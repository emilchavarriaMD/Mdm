"""Registro de brigadas médicas."""
from database import now_iso
from services.patients import age_text
from services.validators import ValidationError, fmt_date, parse_date


def prepare_brigade(raw):
    errors, data = [], {}
    for key in ("codigo", "nombre", "departamento", "municipio", "localidad", "lugar",
                "personal", "observaciones"):
        data[key] = (raw.get(key) or "").strip()
    if not data["codigo"]:
        errors.append("Código de la brigada: obligatorio.")
    if not data["nombre"]:
        errors.append("Nombre de la brigada: obligatorio.")
    try:
        data["fecha"] = parse_date(raw.get("fecha"), "Fecha de la brigada")
        if not data["fecha"]:
            errors.append("Fecha de la brigada: obligatoria.")
    except ValidationError as exc:
        errors.append(str(exc))
        data["fecha"] = None
    return data, errors


def list_brigades(db):
    return db.query("SELECT * FROM brigades ORDER BY fecha DESC, id DESC")


def get_brigade(db, bid):
    return db.one("SELECT * FROM brigades WHERE id=?", (bid,))


def label(b) -> str:
    return f"{b['codigo']} – {b['nombre']} ({fmt_date(b['fecha'])})"


def save_brigade(db, data, bid=None):
    ts = now_iso()
    dup = db.one("SELECT id FROM brigades WHERE LOWER(codigo)=LOWER(?)", (data["codigo"],))
    if dup and dup["id"] != bid:
        raise ValueError(f"Ya existe una brigada con el código '{data['codigo']}'.")
    with db.transaction():
        if bid is None:
            cur = db.execute(
                """INSERT INTO brigades(codigo, nombre, fecha, departamento, municipio, localidad,
                       lugar, personal, observaciones, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (data["codigo"], data["nombre"], data["fecha"], data["departamento"],
                 data["municipio"], data["localidad"], data["lugar"], data["personal"],
                 data["observaciones"], ts, ts))
            bid = cur.lastrowid
            db.audit("brigada", bid, "creación", data["codigo"])
        else:
            db.execute(
                """UPDATE brigades SET codigo=?, nombre=?, fecha=?, departamento=?, municipio=?,
                       localidad=?, lugar=?, personal=?, observaciones=?, updated_at=? WHERE id=?""",
                (data["codigo"], data["nombre"], data["fecha"], data["departamento"],
                 data["municipio"], data["localidad"], data["lugar"], data["personal"],
                 data["observaciones"], ts, bid))
            db.audit("brigada", bid, "modificación", data["codigo"])
    return bid


def delete_brigade(db, bid):
    used = db.scalar("SELECT (SELECT COUNT(*) FROM patients WHERE brigade_id=?) + "
                     "(SELECT COUNT(*) FROM aps_visits WHERE brigade_id=?) + "
                     "(SELECT COUNT(*) FROM ssr_visits WHERE brigade_id=?)", (bid, bid, bid))
    if used:
        raise ValueError("No se puede eliminar: la brigada tiene pacientes o atenciones asociadas.")
    with db.transaction():
        db.execute("DELETE FROM brigades WHERE id=?", (bid,))
        db.audit("brigada", bid, "eliminación", "")


def brigade_patients(db, bid):
    """Pacientes de la brigada (registrados o atendidos en ella) con sus diagnósticos."""
    rows = db.query(
        """SELECT p.* FROM patients p
           WHERE p.brigade_id=:b
              OR EXISTS (SELECT 1 FROM aps_visits WHERE patient_id=p.id AND brigade_id=:b)
              OR EXISTS (SELECT 1 FROM ssr_visits WHERE patient_id=p.id AND brigade_id=:b)
           ORDER BY p.apellidos, p.nombres""", {"b": bid})
    out = []
    for p in rows:
        aps = db.query("SELECT id FROM aps_visits WHERE patient_id=? AND brigade_id=?", (p["id"], bid))
        ssr = db.query("SELECT id FROM ssr_visits WHERE patient_id=? AND brigade_id=?", (p["id"], bid))
        dx = []
        for kind, visits in (("aps", aps), ("ssr", ssr)):
            for v in visits:
                for d in db.query(f"SELECT descripcion, cie11 FROM {kind}_dx WHERE visit_id=? "
                                  "ORDER BY tipo, orden", (v["id"],)):
                    text = d["descripcion"] + (f" ({d['cie11']})" if d["cie11"] else "")
                    if text not in dx:
                        dx.append(text)
        out.append({**p, "edad": age_text(p), "aps_n": len(aps), "ssr_n": len(ssr),
                    "diagnosticos": "; ".join(dx)})
    return out


def brigade_summary(db, bid):
    pacientes_atendidos = db.scalar(
        """SELECT COUNT(DISTINCT pid) FROM (
               SELECT patient_id AS pid FROM aps_visits WHERE brigade_id=?
               UNION SELECT patient_id FROM ssr_visits WHERE brigade_id=?)""", (bid, bid))
    return {
        "registrados": db.scalar("SELECT COUNT(*) FROM patients WHERE brigade_id=?", (bid,)),
        "atendidos": pacientes_atendidos,
        "aps": db.scalar("SELECT COUNT(*) FROM aps_visits WHERE brigade_id=?", (bid,)),
        "ssr": db.scalar("SELECT COUNT(*) FROM ssr_visits WHERE brigade_id=?", (bid,)),
    }
