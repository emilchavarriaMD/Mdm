"""Generador del banco de HEA (services/hea_data_gen.py) a partir de fichas clínicas compactas (tools/hea_specs_*.py).

Cada ficha:  F(id, nombre, k, s, t, main=…, asoc=…, ctx=…, tx=…, neg=…, dur=…, u='años')
  k  C crónico · S síntoma · X contexto/motivo     s  A ambos · F mujer · M hombre
  t  síntoma corto que se usa al combinar diagnósticos (C: nombre para «antecedente de …»)
  main  motivos/cuadros principales (frases nominales en minúscula: «flujo vaginal blanquecino y grumoso»), «|» separa
  asoc  síntomas acompañantes (frases nominales)         ctx  oraciones de contexto/factores (con mayúscula y punto)
  tx    oraciones de tratamiento previo                   neg  ítems negados («fiebre», «dolor pélvico»…)
  dur   duraciones posibles (por defecto según el preset: A agudo, B subagudo, L crónico-síntoma, H horas, Y años)
Las versiones salen de mezclar plantillas distintas con esos ingredientes (sin repetirse) y siempre empiezan como
frase nominal, porque van después de «…de edad, que presenta ».  Uso:  python3 tools/hea_gen.py
"""
import difflib
import importlib
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PRESET = {
    "A": "1 día|2 días|3 días|4 días|5 días|6 días|1 semana",
    "B": "1 semana|10 días|2 semanas|3 semanas|1 mes",
    "L": "1 mes|2 meses|3 meses|4 meses|6 meses|1 año",
    "H": "6 horas|12 horas|24 horas|2 días|3 días",
    "Y": "2 años|3 años|5 años|8 años|10 años|15 años",
    "D": "1 día|2 días|3 días|4 días|5 días",
    "S": "6 semanas|8 semanas|10 semanas|12 semanas|16 semanas|20 semanas|24 semanas|28 semanas|32 semanas|36 semanas",
}
INICIO = ["de inicio insidioso", "de inicio súbito", "de inicio gradual", "de inicio progresivo", "de instalación brusca"]
CURSO = ["de curso progresivo", "de curso persistente", "de curso intermitente", "con tendencia a empeorar",
         "con mejoría parcial", "sin cambios desde su inicio", "que va en aumento", "de predominio vespertino",
         "de predominio nocturno", "de predominio matutino"]
INTENS = ["leve", "moderada", "de intensidad moderada", "intensa", "de intensidad leve a moderada", "marcada"]

SPECS = []
BASE = 14        # versiones que ya existían (no cambian); N_VERSIONES = cuántas se generan ahora
N_VERSIONES = 26
ALIAS_EXTRA = [("Tumor o masa en el seno femenino (nódulo mamario)", 83)]


def F(id, n, k, s, t, main, asoc="", ctx="", tx="", neg="", dur=None, u="años", al=""):
    sp = lambda x: [i.strip() for i in x.split("|") if i.strip()] if isinstance(x, str) else list(x)
    if dur is None:
        dur = {"C": "Y", "X": "A"}.get(k, "A")
    d = sp(PRESET.get(dur, dur))
    SPECS.append(dict(id=id, n=n, k=k, s=s, t=t, u=u, main=sp(main), asoc=sp(asoc), ctx=sp(ctx), tx=sp(tx),
                      neg=sp(neg), dur=d, al=sp(al)))


def G(id, main, asoc="", ctx="", tx="", neg="", dur=None, al="", **meta):
    """Como F, pero n/k/s/t/u se toman del banco anterior (services/hea_data.py) para no cambiar los metadatos."""
    from services import hea_data as old
    b = old.BANK[id]
    F(id, meta.get("n", b["n"]), meta.get("k", b["k"]), meta.get("s", b["s"]), meta.get("t", b["t"]), main, asoc, ctx, tx,
      neg, dur, meta.get("u", b["u"]), al)


def _lista(items, nexo="y"):
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    ult = items[-1]
    w = re.sub(r"[^a-záéíóúñ]", "", ult.lower().split()[0]) if ult.split() else ""
    if nexo == "y" and (w.startswith("i") or (w.startswith("hi") and not w.startswith(("hie", "hia")))):
        nexo = "e"
    if nexo == "o" and w.startswith(("o", "ho")):
        nexo = "u"
    return ", ".join(items[:-1]) + f" {nexo} " + ult


def _fix(v):
    v = re.sub(r"\by (?=(?:i|hi)[^aeiouáéíóú\W])", "e ", v)
    v = re.sub(r"\bo (?=(?:o|ho)[a-záéíóú])", "u ", v)
    return v


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def _raices(t):
    return {w[:5] for w in re.findall(r"[a-záéíóúñ]{5,}", t.lower())}


def _neg(rng, sp, used=""):
    pool = [i for i in sp["neg"] if not (_raices(i) & _raices(used))]
    if not pool:
        return ""
    k = min(len(pool), rng.choice([2, 3, 3, 4]))
    items = rng.sample(pool, k)
    return "Niega " + _lista(items, "o") + "."


def _oracion(rng, lst):
    return rng.choice(lst) if lst else ""


def _asoc(rng, sp, lo=1, hi=3, main=""):
    if not sp["asoc"]:
        return ""
    pool = sp["asoc"]
    if main:
        mw = {w[:5] for w in re.findall(r"[a-záéíóúñ]{5,}", main.lower())}
        pool = [a for a in pool if not ({w[:5] for w in re.findall(r"[a-záéíóúñ]{5,}", a.lower())} & mw)] or pool
    k = min(len(pool), rng.randint(lo, hi))
    return _lista(rng.sample(pool, k))


def _unir(*partes):
    out = []
    for p in partes:
        p = (p or "").strip()
        if p:
            out.append(p)
    return " ".join(out)


def _fin(s):
    s = s.strip()
    return s if s.endswith((".", "!", "?")) else s + "."


# plantillas para cuadros agudos / síntomas / contexto: todas empiezan como frase nominal
def _plantillas_s():
    def t0(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, de {d} de evolución, acompañado de {a}" if a else f"{m}, de {d} de evolución"), c, x, ng)

    def t1(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"cuadro de {d} de evolución caracterizado por {m}" + (f", con {a}" if a else "")), x, c, ng)

    def t2(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, desde hace {d} y {r.choice(INICIO)}" + (f", asociado a {a}" if a else "")), c, ng, x)

    def t3(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, de {d} de evolución, {r.choice(CURSO)}" + (f"; además {a}" if a else "")), x, ng, c)

    def t4(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{d} de evolución con {m}" + (f" y {a}" if a else "")), c, ng, x)

    def t5(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"historia de {m}, que inició hace {d}" + (f", con {a}" if a else "")), x, ng, c)

    def t6(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, {r.choice(CURSO)}, desde hace {d}" + (f"; refiere además {a}" if a else "")), ng, c, x)

    def t7(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"cuadro clínico de {d} de evolución con {m}" + (f", {a}" if a else "")), c, x, ng)

    def t8(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, {r.choice(INICIO)} hace {d}" + (f", que se acompaña de {a}" if a else "")), c, ng, x)

    return [t0, t1, t2, t3, t4, t5, t6, t7, t8]


def _plantillas_extra():
    """Plantillas adicionales para las versiones 15 en adelante (también empiezan como frase nominal)."""
    def u0(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, que lleva {d} de evolución" + (f" y se acompaña de {a}" if a else "")), c, ng, x)

    def u1(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"cuadro de {d} de evolución que inicia con {m}" + (f", con posterior aparición de {a}" if a else "")), x, c, ng)

    def u2(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"desde hace {d}, {m}" + (f", {r.choice(INICIO)} y con {a}" if a else f", {r.choice(INICIO)}")), ng, x, c)

    def u3(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, referido por el paciente desde hace {d}" + (f", asociado a {a}" if a else "")), c, x, ng)

    def u4(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, {r.choice(INICIO)} y de {d} de evolución" + (f"; se acompaña de {a}" if a else "")), x, ng, c)

    def u5(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"molestias de {d} de evolución consistentes en {m}" + (f", junto con {a}" if a else "")), c, ng, x)

    def u6(r, sp, m, d, a, c, x, ng):
        return _unir(_fin(f"{m}, de {d} de evolución, {r.choice(CURSO)}" + (f", con {a}" if a else "")), ng, c, x)

    return [u0, u1, u2, u3, u4, u5, u6]


def generar(sp, n=26):
    rng = random.Random(sp["id"] * 7919 + 13)
    out = []
    if sp["k"] == "C":
        return _generar_c(sp, rng, n)
    if any("{w}" in m for m in sp["main"]):
        return _generar_emb(sp, rng, n)
    if sp["dur"] == ["-"]:
        return _generar_sin_dur(sp, rng, n)
    plant = _plantillas_s()
    extra = _plantillas_extra()
    mains = list(sp["main"]) or [sp["t"]]
    durs = list(sp["dur"])
    intentos = 0
    ti = 0
    mi = 0
    while len(out) < n and intentos < 400:
        intentos += 1
        m = mains[mi % len(mains)]
        mi += 1
        d = rng.choice(durs)
        a = _asoc(rng, sp, 1 if rng.random() < .7 else 0, 3, m)
        c = _oracion(rng, sp["ctx"]) if rng.random() < .6 else ""
        x = _oracion(rng, sp["tx"]) if rng.random() < .55 else ""
        ng = _neg(rng, sp, m + " " + a)
        if len(out) < BASE:          # las primeras versiones salen igual que siempre; después entran las plantillas nuevas
            v = plant[ti % len(plant)](rng, sp, m, d, a, c, x, ng)
        else:
            v = (plant + extra)[ti % (len(plant) + len(extra))](rng, sp, m, d, a, c, x, ng)
        ti += 1
        v = re.sub(r"\s{2,}", " ", v).replace(" ,", ",").strip()
        if any(difflib.SequenceMatcher(None, v, o, autojunk=False).ratio() > .78 for o in out):
            continue
        out.append(_fix(v))
    return out


def _generar_sin_dur(sp, rng, n):
    """Motivos de contacto/controles: sin tiempo de evolución."""
    out = []
    mains = list(sp["main"])
    intentos = 0
    while len(out) < n and intentos < 400:
        intentos += 1
        m = mains[intentos % len(mains)]
        a = _asoc(rng, sp, 0, 2, m)
        c = _oracion(rng, sp["ctx"]) if rng.random() < .75 else ""
        x = _oracion(rng, sp["tx"]) if rng.random() < .5 else ""
        f = intentos % 4
        if f == 0:
            v = _unir(_fin(m + (f", con {a}" if a else "")), c, x, _neg(rng, sp, m + " " + a))
        elif f == 1:
            v = _unir(_fin(m), c, _fin("Refiere " + a) if a else "", _neg(rng, sp, m + " " + a + " " + c), x)
        elif f == 2:
            v = _unir(_fin(m + (f"; se acompaña de {a}" if a else "")), x, _neg(rng, sp), c)
        else:
            v = _unir(_fin(m), x, c, _neg(rng, sp, m + " " + a))
        v = re.sub(r"\s{2,}", " ", v).replace(" ,", ",")
        if any(difflib.SequenceMatcher(None, v, o, autojunk=False).ratio() > .8 for o in out):
            continue
        out.append(_fix(v))
    return out


def _generar_emb(sp, rng, n):
    out = []
    mains = list(sp["main"])
    intentos = 0
    while len(out) < n and intentos < 400:
        intentos += 1
        w = rng.choice(sp["dur"]).split()[0]
        m = mains[intentos % len(mains)].replace("{w}", w)
        a = _asoc(rng, sp, 0, 2, m)
        c = _oracion(rng, sp["ctx"]) if rng.random() < .7 else ""
        x = _oracion(rng, sp["tx"]) if rng.random() < .5 else ""
        f = intentos % 3
        if f == 0:
            v = _unir(_fin(m + (f"; refiere {a}" if a else "")), c, x, _neg(rng, sp, m + " " + a))
        elif f == 1:
            v = _unir(_fin(m + (f", con {a}" if a else "")), x, c, _neg(rng, sp, m + " " + a))
        else:
            v = _unir(_fin(m), _fin("Se acompaña de " + a) if a else "", c, _neg(rng, sp, m + " " + a + " " + c), x)
        v = re.sub(r"\s{2,}", " ", v).replace(" ,", ",")
        if any(difflib.SequenceMatcher(None, v, o, autojunk=False).ratio() > .8 for o in out):
            continue
        out.append(_fix(v))
    return out


def _generar_c(sp, rng, n):
    out = []
    durs = sp["dur"]
    intentos = 0
    while len(out) < n and intentos < 400:
        intentos += 1
        d = rng.choice(durs)
        tx = rng.choice(sp["tx"]) if sp["tx"] else ""
        a = _asoc(rng, sp, 0, 2, "")
        c = _oracion(rng, sp["ctx"]) if rng.random() < .7 else ""
        main = rng.choice(sp["main"]) if sp["main"] else "acude a control de rutina"
        forma = intentos % 4
        ini = f"antecedente de {sp['t']} de {d} de diagnóstico"
        if forma == 0:
            v = f"{ini}, {tx}; {main}" if tx else f"{ini}; {main}"
        elif forma == 1:
            v = f"{ini}. {_cap(main)}" + (f", con {a}" if a else "") + (f". Se encuentra {tx}" if tx else "")
        elif forma == 2:
            v = f"antecedente de {sp['t']}" + (f", {tx}" if tx else "") + f"; {main}" + (f", con {a}" if a else "")
        else:
            v = f"{ini}" + (f", {tx}" if tx else "") + f". {_cap(main)}"
        v = _fin(v)
        v = _unir(v, c, _neg(rng, sp, main + " " + a))
        v = re.sub(r"\s{2,}", " ", v).replace(" ,", ",").replace(",.", ".").replace(";.", ".").replace("..", ".")
        if any(difflib.SequenceMatcher(None, v, o, autojunk=False).ratio() > .8 for o in out):
            continue
        out.append(_fix(v))
    return out


def construir(n=None):
    n = n or N_VERSIONES
    sys.path.insert(0, str(ROOT / "tools"))
    for f in sorted((ROOT / "tools").glob("hea_specs_*.py")):
        importlib.import_module(f.stem)
    bank = {}
    for sp in SPECS:
        vs = generar(sp, n)
        bank[sp["id"]] = dict(k=sp["k"], n=sp["n"], s=sp["s"], t=sp["t"], u=sp["u"], v=vs)
    return bank


def alias():
    return [(a, sp["id"]) for sp in SPECS for a in sp["al"]] + ALIAS_EXTRA


def escribir(bank, alias=None):
    path = ROOT / "services" / "hea_data_gen.py"
    lines = ['"""Banco de HEA generado por tools/hea_gen.py desde tools/hea_specs_*.py (no editar a mano)."""',
             "BANK_GEN = {"]
    for i in sorted(bank):
        e = bank[i]
        lines.append(f"    {i}: dict(k={e['k']!r}, n={e['n']!r}, s={e['s']!r}, t={e['t']!r}, u={e['u']!r}, v=[")
        for v in e["v"]:
            lines.append(f"        {v!r},")
        lines.append("    ]),")
    lines.append("}")
    lines.append("ALIAS_GEN = " + repr(alias or {}))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    import hea_gen as _g
    b = _g.construir()
    print(_g.escribir(b, _g.alias()), len(b), "diagnósticos,", sum(len(e["v"]) for e in b.values()), "versiones")
