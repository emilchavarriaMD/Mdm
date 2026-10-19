"""Estadísticas del panel y reportes. Distinguen pacientes únicos de número de consultas."""
from services.patients import age_text
from services.validators import fmt_date, today_iso
from services import visits as visit_svc

_VISITS = ("SELECT 'aps' AS kind, id, patient_id, fecha_atencion, personal, brigade_id, estado "
           "FROM aps_visits UNION ALL "
           "SELECT 'ssr', id, patient_id, fecha_atencion, personal, brigade_id, estado FROM ssr_visits")


def dashboard_stats(db, brigade_id=None):
    today = today_iso()
    stats = {
        "pacientes": db.scalar("SELECT COUNT(*) FROM patients"),
        "aps_hoy": db.scalar("SELECT COUNT(*) FROM aps_visits WHERE fecha_atencion=?", (today,)),
        "ssr_hoy": db.scalar("SELECT COUNT(*) FROM ssr_visits WHERE fecha_atencion=?", (today,)),
        "brigada_atendidos": 0, "brigada_consultas": 0, "brigada_registrados": 0,
        "borradores": db.scalar(
            "SELECT (SELECT COUNT(*) FROM aps_visits WHERE estado='borrador') + "
            "(SELECT COUNT(*) FROM ssr_visits WHERE estado='borrador')"),
    }
    if brigade_id:
        stats["brigada_atendidos"] = db.scalar(
            "SELECT COUNT(DISTINCT patient_id) FROM (" + _VISITS + ") WHERE brigade_id=?",
            (brigade_id,))
        stats["brigada_consultas"] = db.scalar(
            "SELECT COUNT(*) FROM (" + _VISITS + ") WHERE brigade_id=?", (brigade_id,))
        stats["brigada_registrados"] = db.scalar(
            "SELECT COUNT(*) FROM patients WHERE brigade_id=?", (brigade_id,))
    return stats


def _vwhere(desde, hasta, brigade_id, solo_final, prefix=""):
    where, params = [], []
    if desde:
        where.append(f"{prefix}fecha_atencion >= ?"); params.append(desde)
    if hasta:
        where.append(f"{prefix}fecha_atencion <= ?"); params.append(hasta)
    if brigade_id:
        where.append(f"{prefix}brigade_id = ?"); params.append(brigade_id)
    if solo_final:
        where.append(f"{prefix}estado = 'finalizada'")
    return (" WHERE " + " AND ".join(where)) if where else "", params


def _filter_note(desde, hasta, brigada_txt, solo_final):
    parts = []
    if desde or hasta:
        parts.append(f"Periodo: {fmt_date(desde) or 'inicio'} a {fmt_date(hasta) or 'hoy'}")
    parts.append(f"Brigada: {brigada_txt or 'todas'}")
    if solo_final:
        parts.append("Solo fichas finalizadas")
    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Reportes: cada uno devuelve dict(title, headers, rows, notes)
# ---------------------------------------------------------------------------

def report_por_brigada(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    where, params = _vwhere(desde, hasta, None, solo_final)
    brigades = db.query("SELECT * FROM brigades" +
                        (" WHERE id=?" if brigade_id else "") + " ORDER BY fecha DESC",
                        (brigade_id,) if brigade_id else ())
    rows = []
    for b in brigades:
        w, p = _vwhere(desde, hasta, b["id"], solo_final)
        reg_where, reg_p = ["brigade_id=?"], [b["id"]]
        if desde:
            reg_where.append("fecha_creacion >= ?"); reg_p.append(desde)
        if hasta:
            reg_where.append("fecha_creacion <= ?"); reg_p.append(hasta)
        registrados = db.scalar("SELECT COUNT(*) FROM patients WHERE " + " AND ".join(reg_where), reg_p)
        unicos = db.scalar("SELECT COUNT(DISTINCT patient_id) FROM (" + _VISITS + ")" + w, p)
        aps = db.scalar("SELECT COUNT(*) FROM (" + _VISITS + ")" + w +
                        (" AND" if w else " WHERE") + " kind='aps'", p)
        ssr = db.scalar("SELECT COUNT(*) FROM (" + _VISITS + ")" + w +
                        (" AND" if w else " WHERE") + " kind='ssr'", p)
        rows.append([b["codigo"], b["nombre"], fmt_date(b["fecha"]), registrados, unicos, aps, ssr,
                     aps + ssr])
    if not brigade_id:
        w, p = _vwhere(desde, hasta, None, solo_final)
        sin = (w + (" AND" if w else " WHERE") + " brigade_id IS NULL")
        n_unicos = db.scalar("SELECT COUNT(DISTINCT patient_id) FROM (" + _VISITS + ")" + sin, p)
        aps = db.scalar("SELECT COUNT(*) FROM (" + _VISITS + ")" + sin + " AND kind='aps'", p)
        ssr = db.scalar("SELECT COUNT(*) FROM (" + _VISITS + ")" + sin + " AND kind='ssr'", p)
        if aps + ssr:
            rows.append(["—", "(Sin brigada asignada)", "", db.scalar(
                "SELECT COUNT(*) FROM patients WHERE brigade_id IS NULL"), n_unicos, aps, ssr, aps + ssr])
    total_unicos = db.scalar("SELECT COUNT(DISTINCT patient_id) FROM (" + _VISITS + ")" + where, params)
    notes = [f"Pacientes únicos atendidos en el conjunto: {total_unicos}. "
             "Un paciente atendido en varias brigadas se cuenta una vez por brigada, "
             "por lo que la suma de la columna puede superar ese total.",
             "'Consultas' = atenciones APS + SSR (un paciente puede tener varias)."]
    return {"title": "Pacientes atendidos por brigada",
            "headers": ["Código", "Brigada", "Fecha", "Pacientes registrados", "Pacientes únicos atendidos",
                        "Atenciones APS", "Atenciones SSR", "Total consultas"],
            "rows": rows, "notes": notes}


def report_por_dia(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    w, p = _vwhere(desde, hasta, brigade_id, solo_final)
    data = db.query(
        "SELECT fecha_atencion, COUNT(DISTINCT patient_id) AS unicos, "
        "SUM(kind='aps') AS aps, SUM(kind='ssr') AS ssr, COUNT(*) AS total "
        "FROM (" + _VISITS + ")" + w + " GROUP BY fecha_atencion ORDER BY fecha_atencion", p)
    rows = [[fmt_date(r["fecha_atencion"]), r["unicos"], r["aps"], r["ssr"], r["total"]] for r in data]
    unicos = db.scalar("SELECT COUNT(DISTINCT patient_id) FROM (" + _VISITS + ")" + w, p)
    rows.append(["TOTAL", unicos, sum(r["aps"] for r in data), sum(r["ssr"] for r in data),
                 sum(r["total"] for r in data)])
    return {"title": "Pacientes atendidos por día",
            "headers": ["Fecha", "Pacientes únicos", "Atenciones APS", "Atenciones SSR", "Total consultas"],
            "rows": rows,
            "notes": ["En la fila TOTAL, 'Pacientes únicos' cuenta cada paciente una sola vez en todo "
                      "el periodo (no es la suma de los días)."]}


def report_diagnosticos(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    w, p = _vwhere(desde, hasta, brigade_id, solo_final)
    inner = ("SELECT 'aps' AS kind, d.visit_id, v.patient_id, d.tipo, d.descripcion, d.descripcion_norm, "
             "d.cie11, v.fecha_atencion, v.brigade_id, v.estado FROM aps_dx d JOIN aps_visits v ON v.id=d.visit_id "
             "UNION ALL SELECT 'ssr', d.visit_id, v.patient_id, d.tipo, d.descripcion, d.descripcion_norm, "
             "d.cie11, v.fecha_atencion, v.brigade_id, v.estado FROM ssr_dx d JOIN ssr_visits v ON v.id=d.visit_id")
    data = db.query(
        "SELECT MIN(descripcion) AS dx, GROUP_CONCAT(DISTINCT NULLIF(cie11,'')) AS cie, "
        "SUM(tipo='principal') AS principal, SUM(tipo='secundario') AS secundario, "
        "COUNT(DISTINCT kind || '-' || visit_id) AS consultas, COUNT(DISTINCT patient_id) AS pacientes "
        "FROM (" + inner + ")" + w + " GROUP BY descripcion_norm ORDER BY consultas DESC, dx", p)
    rows = [[r["dx"], r["cie"] or "", r["principal"], r["secundario"], r["consultas"], r["pacientes"]]
            for r in data]
    return {"title": "Diagnósticos registrados",
            "headers": ["Diagnóstico", "CIE-11 registrado", "Como principal", "Como secundario",
                        "Consultas", "Pacientes únicos"],
            "rows": rows,
            "notes": ["Los diagnósticos se agrupan por descripción (sin distinguir mayúsculas ni tildes). "
                      "El código CIE-11 se muestra solo si fue registrado."]}


def report_personal(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    w, p = _vwhere(desde, hasta, brigade_id, solo_final)
    data = db.query(
        "SELECT COALESCE(NULLIF(TRIM(personal),''), '(sin registrar)') AS personal, "
        "SUM(kind='aps') AS aps, SUM(kind='ssr') AS ssr, COUNT(*) AS total, "
        "COUNT(DISTINCT patient_id) AS unicos FROM (" + _VISITS + ")" + w +
        " GROUP BY 1 ORDER BY total DESC", p)
    rows = [[r["personal"], r["aps"], r["ssr"], r["total"], r["unicos"]] for r in data]
    return {"title": "Atenciones por personal médico",
            "headers": ["Personal médico", "Atenciones APS", "Atenciones SSR", "Total consultas",
                        "Pacientes únicos"],
            "rows": rows, "notes": []}


def report_medicamentos(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    w, p = _vwhere(desde, hasta, brigade_id, solo_final, prefix="v.")
    inner = ("SELECT 'aps' AS kind, m.*, v.patient_id, v.fecha_atencion, v.brigade_id, v.estado "
             "FROM aps_meds m JOIN aps_visits v ON v.id=m.visit_id "
             "UNION ALL SELECT 'ssr', m.*, v.patient_id, v.fecha_atencion, v.brigade_id, v.estado "
             "FROM ssr_meds m JOIN ssr_visits v ON v.id=m.visit_id")
    w2 = w.replace("v.", "")
    data = db.query(
        "SELECT MIN(generico) AS med, COALESCE(presentacion,'') AS pres, COALESCE(unidad,'') AS unidad, "
        "COUNT(*) AS n, SUM(cant_prescrita) AS presc, "
        "SUM(cant_entregada IS NOT NULL) AS con_entrega, SUM(cant_entregada) AS entr, "
        "COUNT(DISTINCT patient_id) AS pacientes "
        "FROM (" + inner + ")" + w2 +
        " GROUP BY LOWER(TRIM(generico)), LOWER(TRIM(COALESCE(presentacion,''))), COALESCE(unidad,'') "
        "ORDER BY n DESC, med", p)

    def f(x):
        return "" if x is None else f"{x:g}"
    rows = [[r["med"], r["pres"], r["unidad"], r["n"], f(r["presc"]), r["con_entrega"], f(r["entr"]),
             r["pacientes"]] for r in data]
    return {"title": "Medicamentos prescritos y entregados",
            "headers": ["Medicamento (genérico)", "Presentación", "Unidad", "Prescripciones",
                        "Total prescrito", "Registros con entrega documentada", "Total entregado",
                        "Pacientes únicos"],
            "rows": rows,
            "notes": ["'Total entregado' suma únicamente las cantidades entregadas que fueron "
                      "registradas; no se estima ni se completa lo no documentado."]}


def report_listado_pacientes(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    where, params = [], []
    if brigade_id:
        where.append("(p.brigade_id=? OR EXISTS (SELECT 1 FROM aps_visits WHERE patient_id=p.id AND brigade_id=?) "
                     "OR EXISTS (SELECT 1 FROM ssr_visits WHERE patient_id=p.id AND brigade_id=?))")
        params += [brigade_id] * 3
    if desde:
        where.append("p.fecha_creacion >= ?"); params.append(desde)
    if hasta:
        where.append("p.fecha_creacion <= ?"); params.append(hasta)
    clause = (" WHERE " + " AND ".join(where)) if where else ""
    pats = db.query("SELECT p.*, b.codigo AS bcod FROM patients p LEFT JOIN brigades b ON b.id=p.brigade_id"
                    + clause + " ORDER BY p.apellidos, p.nombres", params)
    rows = [[p["codigo"], p["historia_clinica"] or "", p["nombres"], p["apellidos"], age_text(p),
             p["sexo"], p["departamento"] or "", p["municipio"] or "", p["localidad"] or "",
             p["bcod"] or "", fmt_date(p["fecha_creacion"])] for p in pats]
    return {"title": "Listado administrativo de pacientes",
            "headers": ["Código", "Historia clínica", "Nombres", "Apellidos", "Edad", "Sexo",
                        "Departamento", "Municipio", "Localidad", "Brigada", "Fecha de creación"],
            "rows": rows,
            "notes": ["Listado administrativo: no incluye teléfono ni datos clínicos.",
                      "Filtro de fechas aplicado a la fecha de creación de la Ficha Integral."]}


def report_listado_atenciones(db, desde=None, hasta=None, brigade_id=None, solo_final=False, **_):
    data = visit_svc.list_all_visits(db, fecha_desde=desde, fecha_hasta=hasta, brigade_id=brigade_id,
                                     estado="finalizada" if solo_final else None, limit=100000)
    rows = [[fmt_date(r["fecha_atencion"]), r["codigo"], r["paciente"], r["kind"].upper(),
             r["dx"] or "", r["personal"] or "", r["brigada"] or "", r["estado"]] for r in data]
    return {"title": "Listado de atenciones",
            "headers": ["Fecha", "Código paciente", "Paciente", "Tipo", "Diagnóstico principal",
                        "Personal médico", "Brigada", "Estado"],
            "rows": rows, "notes": ["Listado administrativo: no incluye contenido clínico de las fichas."]}


REPORTS = {
    "Pacientes atendidos por brigada": report_por_brigada,
    "Pacientes atendidos por día": report_por_dia,
    "Diagnósticos registrados": report_diagnosticos,
    "Atenciones por personal médico": report_personal,
    "Medicamentos prescritos y entregados": report_medicamentos,
    "Listado de atenciones": report_listado_atenciones,
    "Listado administrativo de pacientes": report_listado_pacientes,
}


def run_report(db, name, desde=None, hasta=None, brigade_id=None, solo_final=False, brigada_txt=""):
    result = REPORTS[name](db, desde=desde, hasta=hasta, brigade_id=brigade_id, solo_final=solo_final)
    result["filters"] = _filter_note(desde, hasta, brigada_txt, solo_final)
    return result
