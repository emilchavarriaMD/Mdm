"""Validación y conversión de datos (fechas, números) y rangos plausibles."""
import re
import unicodedata
from datetime import date, datetime


class ValidationError(ValueError):
    pass


def normalize(text) -> str:
    """Minúsculas, sin tildes y sin espacios repetidos (para búsquedas y duplicados)."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text.lower()).strip()


def digits(text) -> str:
    return re.sub(r"\D", "", text or "")


# -- fechas -----------------------------------------------------------------

def parse_date(text, label="Fecha", allow_future=True):
    """DD/MM/AAAA (o AAAA-MM-DD) -> 'AAAA-MM-DD'. Vacío -> None. Inválido -> ValidationError."""
    text = (text or "").strip()
    if not text:
        return None
    parsed = None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            parsed = datetime.strptime(text, fmt).date()
            break
        except ValueError:
            continue
    if parsed is None:
        raise ValidationError(f"{label}: formato inválido (use DD/MM/AAAA).")
    if parsed.year < 1900:
        raise ValidationError(f"{label}: el año {parsed.year} no es válido.")
    if not allow_future and parsed > date.today():
        raise ValidationError(f"{label}: no puede ser una fecha futura.")
    return parsed.isoformat()


def fmt_date(iso) -> str:
    """'AAAA-MM-DD' (o con hora) -> 'DD/MM/AAAA'. Vacío -> ''."""
    if not iso:
        return ""
    try:
        return datetime.strptime(str(iso)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return str(iso)


def today_iso() -> str:
    return date.today().isoformat()


# -- números ----------------------------------------------------------------

def parse_number(text, label="Valor", minimum=None, maximum=None):
    """Acepta coma o punto decimal. Vacío -> None (no se rellena nada)."""
    if text is None:
        return None
    text = str(text).strip().replace(",", ".")
    if text == "":
        return None
    try:
        value = float(text)
    except ValueError:
        raise ValidationError(f"{label}: debe ser un número.")
    if value != value or value in (float("inf"), float("-inf")):
        raise ValidationError(f"{label}: número inválido.")
    if minimum is not None and value < minimum:
        raise ValidationError(f"{label}: no puede ser menor que {minimum:g}.")
    if maximum is not None and value > maximum:
        raise ValidationError(f"{label}: no puede ser mayor que {maximum:g}.")
    return value


def fmt_number(value) -> str:
    if value is None or value == "":
        return ""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{v:g}"


# -- signos vitales -----------------------------------------------------------
# (etiqueta, unidad, mínimo imposible, máximo imposible, rango plausible)
# Fuera del rango imposible se rechaza; fuera del plausible solo se advierte
# (el médico puede confirmar y justificar valores clínicos extremos).
VITALS = {
    "pas":         ("Presión sistólica (PAS)", "mmHg", 1, 400, (60, 250)),
    "pad":         ("Presión diastólica (PAD)", "mmHg", 1, 300, (30, 150)),
    "fc":          ("Frecuencia cardíaca (FC)", "lpm", 1, 400, (30, 220)),
    "fr":          ("Frecuencia respiratoria (FR)", "rpm", 1, 150, (6, 60)),
    "temperatura": ("Temperatura", "°C", 20, 50, (34, 42)),
    "peso":        ("Peso", "kg", 0.1, 500, (2, 250)),
}


def check_vitals(raw: dict):
    """raw: {clave: texto}. Devuelve (valores, errores, advertencias)."""
    values, errors, warnings = {}, [], []
    for key, (label, unit, lo, hi, (plo, phi)) in VITALS.items():
        try:
            value = parse_number(raw.get(key), f"{label} ({unit})", minimum=lo, maximum=hi)
        except ValidationError as exc:
            errors.append(str(exc))
            value = None
        values[key] = value
        if value is not None and not (plo <= value <= phi):
            warnings.append(f"{label}: {value:g} {unit} está fuera del rango habitual "
                            f"({plo:g}–{phi:g}). Verifique que sea correcto.")
    pas, pad = values.get("pas"), values.get("pad")
    if pas is not None and pad is not None and pad > pas:
        warnings.append("La presión diastólica es mayor que la sistólica. Verifique los valores.")
    return values, errors, warnings
