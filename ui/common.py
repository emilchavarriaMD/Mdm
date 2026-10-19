"""Funciones auxiliares compartidas por varias pantallas."""
from datetime import datetime

from services import brigades as brigade_svc

NO_BRIGADE = "(Sin brigada)"


def brigade_options(db, with_none=True, none_label=NO_BRIGADE):
    """Devuelve (lista de etiquetas, {etiqueta: id}, {id: etiqueta})."""
    labels, by_label, by_id = [], {}, {}
    if with_none:
        labels.append(none_label)
        by_label[none_label] = None
    for b in brigade_svc.list_brigades(db):
        text = brigade_svc.label(b)
        labels.append(text)
        by_label[text] = b["id"]
        by_id[b["id"]] = text
    return labels, by_label, by_id


def known_values(db, table, column):
    return db.distinct_values(table, column)


def known_meds(db):
    rows = db.query("SELECT generico FROM aps_meds UNION SELECT generico FROM ssr_meds "
                    "ORDER BY generico COLLATE NOCASE")
    return [r["generico"] for r in rows]


def now_hhmm():
    return datetime.now().strftime("%H:%M")
