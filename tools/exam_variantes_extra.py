"""Genera services/examen_variantes_extra.py: redacciones adicionales de cada hallazgo del examen físico.

Parte de las redacciones que ya tiene services/examen_variantes.py y les agrega fórmulas de introducción
(«a la exploración se observa…», «durante la valoración, …») concordando el verbo en singular o plural. La positividad
del hallazgo no cambia. Los hallazgos que empiezan con «sin / no / simétrico…» (no admiten fórmula de introducción)
llevan sus redacciones escritas a mano en tools/exam_variantes_manual.py.
Uso:  python3 tools/exam_variantes_extra.py
"""
import pathlib
import pprint
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from services.examen_variantes import VARIANTES  # noqa: E402

NUEVAS = 12   # redacciones nuevas por hallazgo

VERBOS = [("a la exploración se observa", "a la exploración se observan"), ("se observa", "se observan"),
          ("se aprecia", "se aprecian"), ("se evidencia", "se evidencian"), ("al examen se encuentra", "al examen se encuentran"),
          ("se constata", "se constatan"), ("durante el examen se evidencia", "durante el examen se evidencian"),
          ("se identifica", "se identifican"), ("en la exploración se aprecia", "en la exploración se aprecian"),
          ("se detecta", "se detectan"), ("al examen físico se observa", "al examen físico se observan"),
          ("se documenta", "se documentan")]
LEADS = ["a la exploración, ", "durante la valoración, ", "al examen físico, ", "en la valoración clínica, ",
         "al momento del examen, ", "durante el examen físico, ", "a la valoración, ", "en el examen, ",
         "en la exploración física, ", "al evaluar, ", "en la consulta, ", "durante la exploración, "]
SING_S = {"tos", "crisis", "pelvis", "diabetes", "dermatitis", "cuadris"}
# primeras palabras que no admiten «se observa …» delante (adjetivos, negaciones, preposiciones, verbos…)
NO_VERBO = re.compile(r"^(sin|no|se|en|con|de|del|al|a|la|el|los|las|un|una|simétric|móvil|movil|normo|libre|blando|"
                      r"sano|buena|bueno|ambos|ambas|todo|toda|según|por|para|hasta)\b", re.I)


def _palabra1(t):
    m = re.match(r"[\wáéíóúüñ/]+", t.lower())
    return m.group(0) if m else ""


def _plural(t):
    w = _palabra1(t)
    return w.endswith("s") and w not in SING_S


def clase(k):
    p = _palabra1(k)
    if p in ("paciente", "recién") or k.startswith(("recién nacido", "paciente")):
        return "A"
    if NO_VERBO.match(k):
        return "C"
    return "B"


def _cand(k, bases):
    c = clase(k)
    out = []
    if c == "A":
        for li, lead in enumerate(LEADS):
            for bi, b in enumerate(bases):
                out.append((li, bi, lead + b))
    elif c == "B":
        for vi, (sg, pl) in enumerate(VERBOS):
            for bi, b in enumerate(bases):
                if NO_VERBO.match(b):
                    continue
                out.append((vi, bi, (pl if _plural(b) else sg) + " " + b))
    return out


def generar():
    try:
        from exam_variantes_manual import MANUAL
    except ImportError:
        MANUAL = {}
    res = {}
    for k, bases in VARIANTES.items():
        rng = random.Random(hash_estable(k))
        ya = set(bases)
        nuevas = []
        for v in MANUAL.get(k, []):
            if v not in ya:
                ya.add(v)
                nuevas.append(v)
        cands = _cand(k, bases)
        rng.shuffle(cands)
        usados_pref, usados_base = {}, {}
        # primero las combinaciones que repiten menos prefijo y menos redacción base
        cands.sort(key=lambda c: (usados_pref.get(c[0], 0), usados_base.get(c[1], 0)))
        for _ in range(len(cands)):
            if len(nuevas) >= NUEVAS:
                break
            cands.sort(key=lambda c: (usados_pref.get(c[0], 0) + usados_base.get(c[1], 0), rng.random()))
            for pi, bi, txt in cands:
                if txt not in ya:
                    ya.add(txt)
                    nuevas.append(txt)
                    usados_pref[pi] = usados_pref.get(pi, 0) + 1
                    usados_base[bi] = usados_base.get(bi, 0) + 1
                    break
            else:
                break
        res[k] = nuevas
    return res


def hash_estable(s):
    h = 0
    for ch in s:
        h = (h * 131 + ord(ch)) % 1000003
    return h


if __name__ == "__main__":
    r = generar()
    corto = {k: len(v) for k, v in r.items() if len(v) < NUEVAS}
    path = ROOT / "services" / "examen_variantes_extra.py"
    path.write_text('"""Redacciones adicionales de los hallazgos del examen físico (generado por tools/exam_variantes_extra.py)."""\n'
                    "EXTRA = " + pprint.pformat(r, width=140, sort_dicts=False) + "\n", encoding="utf-8")
    print(path, len(r), "hallazgos;", sum(len(v) for v in r.values()), "redacciones nuevas")
    print("con menos de", NUEVAS, ":", len(corto))
    for k, n in sorted(corto.items(), key=lambda x: x[1])[:80]:
        print(n, "|", clase(k), "|", k[:100])
