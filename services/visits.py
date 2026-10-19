"""Atenciones clínicas: APS (Atención Primaria en Salud) y SSR (Salud Sexual y Reproductiva).

Cada atención es un evento independiente vinculado al paciente por patient_id.
Nada se completa automáticamente: los campos vacíos se guardan vacíos (NULL).
"""
import json
import re

from database import now_iso
from services.validators import (ValidationError, check_vitals, normalize, parse_date,
                                 parse_number)

KINDS = ("aps", "ssr")
KIND_NAMES = {"aps": "Atención Primaria en Salud (APS)",
              "ssr": "Salud Sexual y Reproductiva (SSR)"}
KIND_SHORT = {"aps": "APS", "ssr": "SSR"}

ESTADO_BORRADOR, ESTADO_FINAL = "borrador", "finalizada"

# ---------------------------------------------------------------------------
# Examen físico
# ---------------------------------------------------------------------------
EXAM_PENDIENTE = "Pendiente de completar"
EXAM_NORMAL = "Sin hallazgos patológicos identificados"
EXAM_ANORMAL = "Hallazgos anormales"
EXAM_NO_EVALUADO = "No evaluado"
EXAM_LIMITADO = "Evaluación limitada"
EXAM_ESTADOS = [EXAM_PENDIENTE, EXAM_NORMAL, EXAM_ANORMAL, EXAM_NO_EVALUADO, EXAM_LIMITADO]

ABDOMEN_LIMITADO = ("Exploración abdominal limitada por ausencia de espacio físico adecuado y de "
                    "condiciones apropiadas para la evaluación. No se realiza palpación abdominal.")

ABDOMEN_SUB = [("abdomen_inspeccion", "Inspección"),
               ("abdomen_auscultacion", "Auscultación"),
               ("abdomen_otros", "Otros componentes efectivamente evaluados (percusión, palpación)")]

APS_REGIONS = [
    ("general", "1. Estado general y apariencia"),
    ("cabeza", "2. Cabeza"),
    ("ojos", "3. Ojos"),
    ("oidos", "4. Oídos"),
    ("nariz", "5. Nariz y senos paranasales"),
    ("orofaringe", "6. Cavidad oral y orofaringe"),
    ("cuello", "7. Cuello"),
    ("torax", "8. Tórax y aparato respiratorio"),
    ("cardiovascular", "9. Aparato cardiovascular"),
    ("abdomen", "10. Abdomen"),
    ("genitourinario", "11. Aparato genitourinario (solo si está indicado y se evaluó)"),
    ("extremidades", "12. Extremidades superiores e inferiores"),
    ("musculoesqueletico", "13. Sistema musculoesquelético"),
    ("piel", "14. Piel y anexos"),
    ("neurologico", "15. Sistema neurológico"),
    ("otros", "16. Otros hallazgos relevantes según la HEA"),
]

SSR_REGIONS = [
    ("general", "Estado general y apariencia"),
    ("cardiopulmonar", "Tórax / cardiopulmonar"),
    ("abdomen", "Abdomen"),
    ("mamas", "Mamas"),
    ("genital_externo", "Genitales externos (inspección)"),
    ("especuloscopia", "Examen con espéculo (si no se realizó, indique el motivo)"),
    ("tacto_vaginal", "Tacto vaginal (si no se realizó, indique el motivo)"),
    ("otros", "Otros hallazgos"),
]

REGIONS = {"aps": APS_REGIONS, "ssr": SSR_REGIONS}
REGION_LABELS = {k: dict(v) for k, v in REGIONS.items()}
for _k in REGION_LABELS:
    REGION_LABELS[_k].update({"abdomen_inspeccion": "Abdomen – inspección",
                              "abdomen_auscultacion": "Abdomen – auscultación",
                              "abdomen_otros": "Abdomen – otros componentes"})

# ---------------------------------------------------------------------------
# SSR: intervenciones y opciones
# ---------------------------------------------------------------------------
INTERVENCION_ESTADOS = ["Pendiente", "Realizada", "No realizada"]
SSR_INTERVENCIONES = [
    "Administración de método anticonceptivo",
    "Entrega de medicamentos",
    "Entrega de preservativos",
    "Consejería: uso correcto del método",
    "Consejería: prevención de ITS",
    "Consejería: uso de preservativos",
    "Consejería: efectos adversos",
    "Consejería: signos de alarma",
]
PRUEBA_ESTADOS = ["Realizada", "No realizada", "Pendiente"]
CONSEJERIA_ESTADOS = ["Pendiente", "Realizada", "No realizada"]
SAME_DAY_APS = ["Sí", "No", "No se registró atención APS"]

# ---------------------------------------------------------------------------
# Especificación de campos (columna -> tipo)
# ---------------------------------------------------------------------------
_VITAL_SPEC = {"pas": "num", "pad": "num", "fc": "num", "fr": "num", "temperatura": "num",
               "peso": "num", "vitales_nota": "text"}

APS_SPEC = {
    "fecha_atencion": "date", "personal": "text", "brigade_id": "int", "lugar": "text",
    "historia_clinica": "text", "mismo_dia_ficha": "text", "mismo_dia_manual": "bool",
    "observaciones": "text",
    "hea_motivo": "text", "hea_inicio": "text", "hea_sintomas": "text", "hea_evolucion": "text",
    "hea_asociados": "text", "hea_factores": "text", "hea_antecedentes": "text",
    "hea_negativos": "text", "hea_otros": "text", "hea_texto": "text", "hea_origen": "text",
    "hea_revisada": "bool",
    **_VITAL_SPEC,
    "consejeria_alarma": "text", "consejeria_estado": "text", "recomendaciones": "text",
    "medidas_no_farm": "text", "seguimiento": "text", "fecha_control": "date",
    "referencia": "text", "estado": "text",
}

SSR_SPEC = {
    "fecha_atencion": "date", "personal": "text", "brigade_id": "int", "lugar": "text",
    "motivo": "text", "categoria": "text", "mismo_dia_aps": "text", "mismo_dia_manual": "bool",
    "observaciones": "text",
    "hea_inicio": "text", "hea_urinarios": "text", "hea_flujo": "text", "hea_olor_prurito": "text",
    "hea_dolor": "text", "fum": "date_past", "hea_ciclo": "text", "hea_antec_go": "text",
    "hea_anticonceptivo_actual": "text", "hea_fecha_ultima_dosis": "date_past",
    "hea_riesgo_embarazo": "text", "hea_antec_its": "text", "hea_otros": "text",
    "hea_texto": "text", "hea_origen": "text", "hea_revisada": "bool",
    **_VITAL_SPEC,
    "metodo_entregado": "text", "metodo_presentacion": "text", "metodo_cantidad": "num",
    "metodo_unidad": "text", "fecha_administracion": "date_past", "fecha_proxima_dosis": "date",
    "signos_alarma": "text", "recomendaciones": "text", "seguimiento": "text",
    "fecha_control": "date", "referencia": "text", "estado": "text",
}
SPECS = {"aps": APS_SPEC, "ssr": SSR_SPEC}

DATE_LABELS = {
    "fecha_atencion": "Fecha de atención", "fecha_control": "Fecha sugerida de control",
    "fum": "Fecha de última menstruación (FUM)",
    "hea_fecha_ultima_dosis": "Fecha de última dosis anticonceptiva",
    "fecha_administracion": "Fecha de administración",
    "fecha_proxima_dosis": "Fecha prevista de la próxima dosis",
}

MED_FIELDS = ["generico", "presentacion", "dosis", "via", "frecuencia", "horario", "duracion",
              "cant_prescrita", "cant_entregada", "unidad", "indicaciones"]

CIE11_RE = re.compile(r"^[0-9A-Z]{2,4}(\.[0-9A-Z]{1,3})?(/[0-9A-Z]{2,4}(\.[0-9A-Z]{1,3})?)?$")


# ---------------------------------------------------------------------------
# Preparación / validación
# ---------------------------------------------------------------------------

def _convert_main(kind, raw_main, errors):
    spec = SPECS[kind]
    out = {}
    for col, typ in spec.items():
        value = raw_main.get(col)
        if typ == "text":
            out[col] = (value or "").strip() if isinstance(value, str) or value is None else str(value)
        elif typ == "bool":
            out[col] = 1 if value in (1, True, "1", "Sí", "si") else 0
        elif typ == "int":
            out[col] = int(value) if value not in (None, "") else None
        elif typ in ("date", "date_past"):
            label = DATE_LABELS.get(col, col)
            try:
                out[col] = parse_date(value, label,
                                      allow_future=(typ == "date" and col != "fecha_atencion"))
            except ValidationError as exc:
                errors.append(str(exc))
                out[col] = None
        elif typ == "num":
            if col in _VITAL_SPEC:
                continue
            try:
                out[col] = parse_number(value, "Cantidad del método", minimum=0)
            except ValidationError as exc:
                errors.append(str(exc))
                out[col] = None
    values, v_errors, v_warnings = check_vitals(raw_main)
    errors.extend(v_errors)
    out.update(values)
    return out, v_warnings


def prepare_visit(kind, raw, finalizing=False):
    """Convierte y valida. Devuelve (data, errores, advertencias).

    - errores: impiden guardar (datos mal formados o faltantes esenciales).
    - advertencias: se muestran para que el usuario confirme, pero no impiden guardar.
    - Al finalizar se exigen los datos administrativos esenciales; los datos clínicos
      pueden quedar pendientes (se avisa cuántos).
    """
    errors, warnings = [], []
    main, w = _convert_main(kind, raw.get("main", {}), errors)
    warnings.extend(w)
    # valores de listas cerradas: nunca se guardan vacíos ni inventados
    if kind == "aps":
        if main.get("mismo_dia_ficha") not in ("Sí", "No"):
            main["mismo_dia_ficha"] = "No"
        if main.get("consejeria_estado") not in CONSEJERIA_ESTADOS:
            main["consejeria_estado"] = "Pendiente"
    elif main.get("mismo_dia_aps") not in SAME_DAY_APS:
        main["mismo_dia_aps"] = "No se registró atención APS"
    if main.get("hea_origen") not in ("manual", "plantilla"):
        main["hea_origen"] = "manual"
    if not main.get("fecha_atencion") and not any("Fecha de atención" in e for e in errors):
        errors.append("Fecha de atención: campo obligatorio.")

    # examen físico
    exam = {}
    for region, entry in (raw.get("exam") or {}).items():
        estado = entry.get("estado") or EXAM_PENDIENTE
        if estado not in EXAM_ESTADOS:
            estado = EXAM_PENDIENTE
        texto = (entry.get("hallazgos") or "").strip()
        exam[region] = {"estado": estado, "hallazgos": texto}
        if estado == EXAM_ANORMAL and not texto:
            warnings.append(f"{REGION_LABELS[kind].get(region, region)}: marcado como "
                            "'Hallazgos anormales' pero sin describir los hallazgos.")

    # diagnósticos
    dx = []
    for i, row in enumerate(raw.get("dx") or []):
        desc = (row.get("descripcion") or "").strip()
        cie = (row.get("cie11") or "").strip().upper()
        obs = (row.get("observaciones") or "").strip()
        tipo = row.get("tipo", "secundario")
        if not (desc or cie or obs):
            continue
        if not desc:
            errors.append("Diagnóstico: hay un código u observación sin descripción.")
            continue
        if cie and not CIE11_RE.match(cie):
            warnings.append(f"Código CIE-11 '{cie}' no tiene el formato esperado (ej. CA40.0). "
                            "Verifique el código.")
        dx.append({"tipo": tipo, "descripcion": desc, "cie11": cie,
                   "cie11_verificado": 1 if row.get("cie11_verificado") and cie else 0,
                   "observaciones": obs, "orden": i})

    # medicamentos
    meds = []
    for i, row in enumerate(raw.get("meds") or []):
        row = {k: (row.get(k) or "").strip() if isinstance(row.get(k), str) or row.get(k) is None
               else row.get(k) for k in MED_FIELDS}
        name = row["generico"]
        if not any(str(v).strip() for v in row.values()):
            continue
        if not name:
            errors.append(f"Medicamento (fila {i + 1}): falta el nombre genérico.")
            continue
        try:
            presc = parse_number(row["cant_prescrita"], f"{name}: cantidad prescrita", minimum=0)
            entr = parse_number(row["cant_entregada"], f"{name}: cantidad entregada", minimum=0)
        except ValidationError as exc:
            errors.append(str(exc))
            continue
        if presc is not None and entr is not None and entr > presc:
            warnings.append(f"{name}: la cantidad entregada ({entr:g}) es mayor que la prescrita ({presc:g}).")
        meds.append({**row, "cant_prescrita": presc, "cant_entregada": entr, "orden": i})

    data = {"main": main, "exam": exam, "dx": dx, "meds": meds}

    if kind == "ssr":
        tests = []
        for i, row in enumerate(raw.get("tests") or []):
            name = (row.get("prueba") or "").strip()
            result = (row.get("resultado") or "").strip()
            motivo = (row.get("motivo") or "").strip()
            if not (name or result or motivo):
                continue
            if not name:
                errors.append(f"Prueba (fila {i + 1}): falta el nombre de la prueba.")
                continue
            estado = row.get("estado") if row.get("estado") in PRUEBA_ESTADOS else "Realizada"
            if estado == "Realizada" and not result:
                warnings.append(f"Prueba '{name}' marcada como realizada pero sin resultado.")
            tests.append({"prueba": name, "estado": estado, "resultado": result,
                          "motivo": motivo, "orden": i})
        data["tests"] = tests
        inter = {}
        for tipo in SSR_INTERVENCIONES:
            e = (raw.get("interventions") or {}).get(tipo, {})
            estado = e.get("estado") if e.get("estado") in INTERVENCION_ESTADOS else "Pendiente"
            inter[tipo] = {"estado": estado, "nota": (e.get("nota") or "").strip()}
        data["interventions"] = inter
        if main.get("metodo_entregado") and inter[SSR_INTERVENCIONES[0]]["estado"] == "Pendiente" \
                and main.get("fecha_administracion"):
            warnings.append("Hay fecha de administración, pero la administración del método "
                            "anticonceptivo sigue como 'Pendiente'.")

    # fechas de seguimiento
    if main.get("fecha_control") and main.get("fecha_atencion") \
            and main["fecha_control"] < main["fecha_atencion"]:
        warnings.append("La fecha sugerida de control es anterior a la fecha de atención.")

    # coherencia de HEA generada por plantilla
    if main.get("hea_origen") == "plantilla" and not main.get("hea_revisada") and finalizing:
        errors.append("La HEA es un borrador generado por plantilla: debe ser revisada por el "
                      "personal médico (marque 'HEA revisada') antes de finalizar.")

    if finalizing:
        if not main.get("personal"):
            errors.append("Personal médico que brinda la atención: obligatorio para finalizar.")
        principal = [d for d in dx if d["tipo"] == "principal"]
        if not principal:
            errors.append("Diagnóstico principal: obligatorio para finalizar.")
        if kind == "ssr":
            if not main.get("motivo"):
                errors.append("Motivo de consulta: obligatorio para finalizar.")
            if not main.get("categoria"):
                errors.append("Categoría de atención: obligatoria para finalizar.")
        pendientes = [REGION_LABELS[kind].get(r, r) for r, e in exam.items()
                      if e["estado"] == EXAM_PENDIENTE and not r.startswith("abdomen_")]
        faltan = [r for r, _ in REGIONS[kind] if r not in exam]
        n_pend = len(pendientes) + len(faltan)
        if n_pend:
            warnings.append(f"{n_pend} región(es) del examen físico siguen 'Pendiente de completar'. "
                            "Se guardarán como pendientes (no se marcan como normales).")
        if all(main.get(k) is None for k in ("pas", "pad", "fc", "fr", "temperatura", "peso")):
            warnings.append("No se registró ningún signo vital.")
        if kind == "aps" and not (main.get("hea_texto") or main.get("hea_motivo")):
            warnings.append("La Historia de la Enfermedad Actual está vacía (quedará pendiente).")
    data["main"]["estado"] = ESTADO_FINAL if finalizing else ESTADO_BORRADOR
    return data, errors, warnings


# ---------------------------------------------------------------------------
# Lógica "mismo día"
# ---------------------------------------------------------------------------

def suggest_same_day(db, kind, pid, fecha_iso, patient=None):
    """APS: ¿misma fecha que la creación de la Ficha Integral? ('Sí'/'No').
    SSR: ¿misma fecha que una atención APS del paciente? (Sí/No/No se registró atención APS)."""
    if kind == "aps":
        if patient is None:
            patient = db.one("SELECT fecha_creacion FROM patients WHERE id=?", (pid,))
        return "Sí" if patient and fecha_iso and patient["fecha_creacion"] == fecha_iso else "No"
    if db.scalar("SELECT COUNT(*) FROM aps_visits WHERE patient_id=?", (pid,)) == 0:
        return "No se registró atención APS"
    if fecha_iso and db.scalar(
            "SELECT COUNT(*) FROM aps_visits WHERE patient_id=? AND fecha_atencion=?",
            (pid, fecha_iso)):
        return "Sí"
    return "No"


# ---------------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------------

def _insert_children(db, kind, vid, data):
    for region, e in data["exam"].items():
        db.execute(f"INSERT INTO {kind}_exam(visit_id, region, estado, hallazgos) VALUES (?,?,?,?)",
                   (vid, region, e["estado"], e["hallazgos"]))
    for d in data["dx"]:
        db.execute(
            f"INSERT INTO {kind}_dx(visit_id, tipo, descripcion, descripcion_norm, cie11, "
            "cie11_verificado, observaciones, orden) VALUES (?,?,?,?,?,?,?,?)",
            (vid, d["tipo"], d["descripcion"], normalize(d["descripcion"]), d["cie11"],
             d["cie11_verificado"], d["observaciones"], d["orden"]))
    for m in data["meds"]:
        db.execute(
            f"INSERT INTO {kind}_meds(visit_id, generico, presentacion, dosis, via, frecuencia, "
            "horario, duracion, cant_prescrita, cant_entregada, unidad, indicaciones, orden) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (vid, m["generico"], m["presentacion"], m["dosis"], m["via"], m["frecuencia"],
             m["horario"], m["duracion"], m["cant_prescrita"], m["cant_entregada"], m["unidad"],
             m["indicaciones"], m["orden"]))
    if kind == "ssr":
        for t in data["tests"]:
            db.execute("INSERT INTO ssr_tests(visit_id, prueba, estado, resultado, motivo, orden) "
                       "VALUES (?,?,?,?,?,?)",
                       (vid, t["prueba"], t["estado"], t["resultado"], t["motivo"], t["orden"]))
        for tipo, e in data["interventions"].items():
            db.execute("INSERT INTO ssr_interventions(visit_id, tipo, estado, nota) VALUES (?,?,?,?)",
                       (vid, tipo, e["estado"], e["nota"]))


def _delete_children(db, kind, vid):
    tables = [f"{kind}_exam", f"{kind}_dx", f"{kind}_meds"]
    if kind == "ssr":
        tables += ["ssr_tests", "ssr_interventions"]
    for t in tables:
        db.execute(f"DELETE FROM {t} WHERE visit_id=?", (vid,))


def get_visit(db, kind, vid):
    main = db.one(f"SELECT * FROM {kind}_visits WHERE id=?", (vid,))
    if not main:
        return None
    exam = {r["region"]: {"estado": r["estado"], "hallazgos": r["hallazgos"] or ""}
            for r in db.query(f"SELECT * FROM {kind}_exam WHERE visit_id=?", (vid,))}
    dx = db.query(f"SELECT * FROM {kind}_dx WHERE visit_id=? ORDER BY tipo, orden, id", (vid,))
    dx.sort(key=lambda d: (0 if d["tipo"] == "principal" else 1, d["orden"], d["id"]))
    meds = db.query(f"SELECT * FROM {kind}_meds WHERE visit_id=? ORDER BY orden, id", (vid,))
    result = {"main": main, "exam": exam, "dx": dx, "meds": meds}
    if kind == "ssr":
        result["tests"] = db.query("SELECT * FROM ssr_tests WHERE visit_id=? ORDER BY orden, id", (vid,))
        result["interventions"] = {r["tipo"]: {"estado": r["estado"], "nota": r["nota"] or ""}
                                   for r in db.query("SELECT * FROM ssr_interventions WHERE visit_id=?", (vid,))}
    return result


def _snapshot(visit):
    """Representación comparable de una atención para el registro de cambios."""
    if not visit:
        return {}
    snap = {k: v for k, v in visit["main"].items()
            if k not in ("id", "created_at", "updated_at", "finalizada_at")}
    snap["__exam"] = json.dumps(visit["exam"], sort_keys=True, ensure_ascii=False)
    snap["__dx"] = json.dumps([(d["tipo"], d["descripcion"], d["cie11"], d["observaciones"])
                               for d in visit["dx"]], ensure_ascii=False)
    snap["__meds"] = json.dumps([[m.get(f) for f in MED_FIELDS] for m in visit["meds"]],
                                ensure_ascii=False)
    if "tests" in visit:
        snap["__pruebas"] = json.dumps([(t["prueba"], t["estado"], t["resultado"], t["motivo"])
                                        for t in visit["tests"]], ensure_ascii=False)
        snap["__intervenciones"] = json.dumps(visit["interventions"], sort_keys=True,
                                              ensure_ascii=False)
    return snap


_CHILD_NAMES = {"__exam": "examen físico", "__dx": "diagnósticos", "__meds": "medicamentos",
                "__pruebas": "pruebas", "__intervenciones": "intervenciones"}


def save_visit(db, kind, patient_id, data, visit_id=None) -> int:
    """Crea o actualiza una atención (borrador o finalizada). No modifica otras atenciones."""
    main = data["main"]
    cols = list(SPECS[kind].keys())
    with db.transaction():
        if visit_id is None:
            ts = now_iso()
            names = ["patient_id"] + cols + ["created_at", "updated_at", "finalizada_at"]
            values = ([patient_id] + [main.get(c) for c in cols]
                      + [ts, ts, ts if main["estado"] == ESTADO_FINAL else None])
            cur = db.execute(
                f"INSERT INTO {kind}_visits ({', '.join(names)}) "
                f"VALUES ({', '.join('?' * len(names))})", values)
            visit_id = cur.lastrowid
            _insert_children(db, kind, visit_id, data)
            db.audit(f"{kind}_visit", visit_id,
                     "creación" if main["estado"] == ESTADO_BORRADOR else "creación y finalización",
                     f"Atención {KIND_SHORT[kind]} del {main['fecha_atencion']}",
                     patient_id=patient_id)
            return visit_id

        before = get_visit(db, kind, visit_id)
        if not before or before["main"]["patient_id"] != patient_id:
            raise ValueError("La atención no pertenece a este paciente.")
        finalizada_at = before["main"]["finalizada_at"]
        if main["estado"] == ESTADO_FINAL and not finalizada_at:
            finalizada_at = now_iso()
        sets = ", ".join(f"{c}=?" for c in cols) + ", updated_at=?, finalizada_at=?"
        db.execute(f"UPDATE {kind}_visits SET {sets} WHERE id=?",
                   [main.get(c) for c in cols] + [now_iso(), finalizada_at, visit_id])
        _delete_children(db, kind, visit_id)
        _insert_children(db, kind, visit_id, data)
        after = get_visit(db, kind, visit_id)
        old_s, new_s = _snapshot(before), _snapshot(after)
        changes = []
        for key in new_s:
            if old_s.get(key) != new_s[key]:
                if key.startswith("__"):
                    changes.append(f"{_CHILD_NAMES[key]} modificado(s)")
                elif key == "estado":
                    changes.append(f"estado: {old_s.get(key)} → {new_s[key]}")
                else:
                    changes.append(f"{key}: '{old_s.get(key) if old_s.get(key) is not None else ''}' → "
                                   f"'{new_s[key] if new_s[key] is not None else ''}'")
        if changes:
            db.audit(f"{kind}_visit", visit_id, "modificación", "; ".join(changes),
                     patient_id=patient_id)
    return visit_id


def delete_draft(db, kind, visit_id):
    """Solo se pueden eliminar borradores; las fichas finalizadas se conservan siempre."""
    v = db.one(f"SELECT patient_id, estado, fecha_atencion FROM {kind}_visits WHERE id=?", (visit_id,))
    if not v:
        return False
    if v["estado"] != ESTADO_BORRADOR:
        raise ValueError("Solo se pueden eliminar borradores. Las fichas finalizadas se conservan.")
    with db.transaction():
        db.execute(f"DELETE FROM {kind}_visits WHERE id=?", (visit_id,))
        db.audit(f"{kind}_visit", visit_id, "eliminación de borrador",
                 f"Borrador {KIND_SHORT[kind]} del {v['fecha_atencion']}", patient_id=v["patient_id"])
    return True


# ---------------------------------------------------------------------------
# Listados
# ---------------------------------------------------------------------------

def list_all_visits(db, patient_id=None, texto="", fecha_desde=None, fecha_hasta=None,
                    brigade_id=None, kind=None, estado=None, diagnostico="", limit=1000):
    selects, params = [], []
    for k in KINDS:
        if kind and kind != k:
            continue
        where = ["1=1"]
        p = []
        if patient_id:
            where.append("v.patient_id=?"); p.append(patient_id)
        for token in normalize(texto).split():
            where.append("(pt.nombre_norm LIKE ? OR LOWER(pt.codigo) LIKE ?)")
            p += [f"%{token}%"] * 2
        if fecha_desde:
            where.append("v.fecha_atencion >= ?"); p.append(fecha_desde)
        if fecha_hasta:
            where.append("v.fecha_atencion <= ?"); p.append(fecha_hasta)
        if brigade_id:
            where.append("v.brigade_id = ?"); p.append(brigade_id)
        if estado:
            where.append("v.estado = ?"); p.append(estado)
        dx = normalize(diagnostico)
        if dx:
            where.append(f"EXISTS (SELECT 1 FROM {k}_dx d WHERE d.visit_id=v.id AND "
                         "(d.descripcion_norm LIKE ? OR LOWER(COALESCE(d.cie11,'')) LIKE ?))")
            p += [f"%{dx}%"] * 2
        selects.append(f"""
            SELECT '{k}' AS kind, v.id AS id, v.patient_id AS patient_id, v.fecha_atencion AS fecha_atencion,
                   v.personal AS personal, v.estado AS estado,
                   v.brigade_id AS brigade_id, v.updated_at AS updated_at, pt.codigo AS codigo, pt.nombres || ' ' || pt.apellidos AS paciente,
                   (SELECT descripcion FROM {k}_dx WHERE visit_id=v.id AND tipo='principal'
                        ORDER BY orden, id LIMIT 1) AS dx,
                   b.codigo AS brigada
            FROM {k}_visits v JOIN patients pt ON pt.id = v.patient_id
                 LEFT JOIN brigades b ON b.id = v.brigade_id
            WHERE {' AND '.join(where)}""")
        params += p
    if not selects:
        return []
    sql = " UNION ALL ".join(selects) + \
          f" ORDER BY fecha_atencion DESC, updated_at DESC LIMIT {int(limit)}"
    return db.query(sql, params)


def visit_audit(db, kind, visit_id):
    return db.query("SELECT * FROM audit_log WHERE entidad=? AND entidad_id=? ORDER BY id",
                    (f"{kind}_visit", visit_id))


def patient_audit(db, patient_id):
    return db.query("SELECT * FROM audit_log WHERE entidad='paciente' AND entidad_id=? ORDER BY id",
                    (patient_id,))
