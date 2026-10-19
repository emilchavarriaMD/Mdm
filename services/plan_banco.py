"""Plan de manejo general (sin medicamentos) según los diagnósticos elegidos.

Por cada diagnóstico hay tres reservas de frases: medidas generales (m), signos de alarma (a) y seguimiento (s).
El texto elige algunas al azar y las junta en oraciones con distintos encabezados, así que sale distinto cada vez.
Con varios diagnósticos se reparten las frases entre ellos sin repetir. Los medicamentos los escribe la persona.
"""
import re

from services import cie11_catalog as cat

try:
    from services.plan_data import PLAN
except ImportError:  # sin banco: no se propone nada
    PLAN = {}

_NORM = {cat.plain(k): v for k, v in PLAN.items()}

FRASES_M = ["Se recomienda {}.", "Se indica {}.", "Se aconseja {}.", "Se sugiere {}."]
FRASES_A = ["Se explican los signos de alarma y se indica acudir de inmediato a un centro de salud si presenta {}.",
            "Se educa sobre signos de alarma: acudir sin demora si presenta {}.",
            "Se indica acudir a un centro de salud de inmediato si presenta {}.",
            "Se orienta sobre los signos de peligro: buscar atención médica urgente ante {}."]


class _Primero:
    @staticmethod
    def choice(op):
        return op[0]

    @staticmethod
    def sample(op, k):
        return list(op[:k])

    @staticmethod
    def shuffle(x):
        return None


def _lista(items):
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " y " + items[-1]


def _registro(texto):
    """Reserva de frases para una descripción de ActivityInfo o un diagnóstico/abreviatura del ATA (None si no hay)."""
    k = cat.plain(texto or "")
    if not k:
        return None
    if k in _NORM:
        return _NORM[k]
    from services import hea_banco            # «Hipertensión», «HTA»… → diagnóstico del banco
    n = hea_banco.bank_id(texto)
    nombre = hea_banco.BANK[n]["n"] if n in hea_banco.BANK else ""
    return _NORM.get(cat.plain(nombre))


def tiene_plan(descripcion):
    return _registro(descripcion) is not None


def _repartir(pools, total, rng, must=2, top=8):
    """Toma frases por turnos de cada diagnóstico, sin repetir ideas parecidas. Las listas vienen ordenadas de mayor a
    menor importancia: siempre entran las `must` primeras de cada una y el resto se elige al azar entre las `top` primeras."""
    armados = []
    for p in pools:
        p = list(p)[:top]
        resto = p[must:]
        rng.shuffle(resto)
        armados.append(p[:must] + resto)
    out, vistos, palabras = [], set(), []
    i = 0
    while len(out) < total and any(armados):
        p = armados[i % len(armados)]
        i += 1
        while p:
            x = p.pop(0)
            w = {t for t in re.findall(r"\w{4,}", x.lower())}
            parecido = x.lower() in vistos or any(w and q and len(w & q) / min(len(w), len(q)) >= 0.6 for q in palabras)
            if not parecido:
                vistos.add(x.lower())
                palabras.append(w)
                out.append(x)
                break
    return out


def compose(descripciones, rng=None):
    """Texto del plan para los diagnósticos dados. Sin rng: siempre las primeras frases (estable para pruebas)."""
    det = rng is None
    rng = rng or _Primero()
    reg, usados = [], set()
    for d in descripciones:
        r = _registro(d)
        if r is not None and id(r) not in usados:       # dos diagnósticos que son el mismo no repiten su plan
            usados.add(id(r))
            reg.append(r)
    if not reg:
        return ""
    n = len(reg)
    # un párrafo corto: con varios diagnósticos solo lo de mayor peso de cada uno (las ideas repetidas se descartan)
    m = _repartir([r["m"] for r in reg], 3 if n == 1 else 4, rng, must=1, top=6)
    a = _repartir([r["a"] for r in reg], 3 if n == 1 else 4, rng, must=1, top=5)
    partes = []
    if m:
        t = _lista(m)
        partes.append(t[0].upper() + t[1:] + ".")
    if a:
        partes.append(rng.choice(FRASES_A).format(_lista(a)))
    return " ".join(partes)
