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

try:                                       # frases extra: se agregan al final de cada reserva (las primeras no cambian)
    from services.plan_extra_data import EXTRA
    for _n, _e in EXTRA.items():
        if _n in PLAN:
            PLAN[_n]["m"] = list(PLAN[_n]["m"]) + [x for x in _e["m"] if x not in PLAN[_n]["m"]]
            PLAN[_n]["a"] = list(PLAN[_n]["a"]) + [x for x in _e["a"] if x not in PLAN[_n]["a"]]
except ImportError:
    pass

try:                                       # plan propio de la ficha de SSR (otras frases que el de APS)
    from services.plan_ssr_data import PLAN_SSR
except ImportError:
    PLAN_SSR = {}
_NORM_SSR = {cat.plain(k): v for k, v in PLAN_SSR.items()}

_NORM = {cat.plain(k): v for k, v in PLAN.items()}

FRASES_M = ["Se recomienda {}.", "Se indica {}.", "Se aconseja {}.", "Se sugiere {}."]
FRASES_A = ["Vigilar signos de alarma como {}; en caso de presentarlos, acudir de inmediato a un centro de salud.",
            "Vigilar la aparición de signos de alarma como {} y, en caso de presentarlos, acudir sin demora al centro de salud.",
            "Estar atento a signos de alarma como {}; si se presentan, acudir de inmediato a un centro de salud.",
            "Vigilar por signos de alarma como {} y, de presentarlos, buscar atención médica de inmediato."]


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


def _registro(texto, ssr=False):
    """Reserva de frases para una descripción de ActivityInfo o un diagnóstico/abreviatura del ATA (None si no hay).
    Con ssr=True se usa primero el plan propio de SSR (si el diagnóstico lo tiene) y si no, el general."""
    k = cat.plain(texto or "")
    if not k:
        return None
    if ssr and k in _NORM_SSR:
        return _NORM_SSR[k]
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


def compose(descripciones, rng=None, ssr=False):
    """Texto del plan para los diagnósticos dados. Sin rng: siempre las primeras frases (estable para pruebas)."""
    det = rng is None
    rng = rng or _Primero()
    reg, usados = [], set()
    for d in descripciones:
        r = _registro(d, ssr)
        if r is not None and id(r) not in usados:       # dos diagnósticos que son el mismo no repiten su plan
            usados.add(id(r))
            reg.append(r)
    if not reg:
        return ""
    n = len(reg)
    # un párrafo corto: con varios diagnósticos solo lo de mayor peso de cada uno (las ideas repetidas se descartan)
    m = _repartir([r["m"] for r in reg], 3 if n == 1 else 4, rng, must=1, top=24)
    a = _repartir([r["a"] for r in reg], 3 if n == 1 else 4, rng, must=1, top=12)
    partes = []
    if m:
        t = _lista(m)
        partes.append(t[0].upper() + t[1:] + ".")
    if a:
        partes.append(rng.choice(FRASES_A).format(_lista(a)))
    return " ".join(partes)
