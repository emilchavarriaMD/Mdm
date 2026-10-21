"""HEA de planificación familiar (PF) según el MÉTODO que dice el ATA.

El ATA trae «PF (ACOs)», «PF (Depo)», «PF implante», «PF DIU», «PF condón»… y la HEA tiene que hablar de ESE método
(antes toda la HEA de PF en SSR salía con la inyección trimestral). `metodo(texto)` detecta el método y
`VERSIONES[metodo]` trae las versiones de esa HEA: unas escritas a mano y otras armadas combinando piezas del mismo
método (así no se mezclan síntomas o tratamientos de otro método). Es determinista: siempre salen las mismas versiones.

Cada versión empieza con un verbo (acude / utiliza / solicita…) porque va después de «…de edad, que ».
"""
import difflib
import random
import re

# método → expresión (sobre texto sin tildes ni mayúsculas). Gana el método que se nombra primero.
_PATRONES = [
    ("oral", r"\bacos?\b|\bacho\b|\boral|pastilla|pildora"),
    ("depo", r"\bdepo|medroxi|\bdmpa\b|trimestral"),
    ("mensual", r"mensual|mesigyna|cyclofem|ciclofem"),
    ("inyectable", r"inyec|aplicacion"),
    ("implante", r"implante|jadelle|implanon|subdermic"),
    ("diu", r"\bdiu\b|dispositivo|t de cobre|intrauterin"),
    ("condon", r"condon|preservativo"),
]
_ORDEN = [m for m, _p in _PATRONES]


def _plano(texto):
    import unicodedata
    t = unicodedata.normalize("NFD", str(texto or "").lower())
    return re.sub(r"\s+", " ", re.sub(r"[̀-ͯ]", "", t).replace("(", " ").replace(")", " ")).strip()


def metodo(texto):
    """'oral', 'depo', 'mensual', 'inyectable', 'implante', 'diu', 'condon' o None (no dice el método)."""
    t = _plano(texto)
    mejor = None
    for m, patron in _PATRONES:
        hit = re.search(patron, t)
        if hit and (mejor is None or hit.start() < mejor[0]):
            mejor = (hit.start(), m)
    return mejor[1] if mejor else None


# frase corta del método (para cuando PF es un diagnóstico secundario: «Asimismo, utiliza …»)
SINTOMA = {
    "oral": "utiliza anticonceptivos orales como método de planificación familiar",
    "depo": "utiliza anticonceptivo inyectable trimestral",
    "mensual": "utiliza anticonceptivo inyectable mensual",
    "inyectable": "utiliza anticonceptivo inyectable como método de planificación familiar",
    "implante": "utiliza implante subdérmico como método de planificación familiar",
    "diu": "utiliza dispositivo intrauterino como método de planificación familiar",
    "condon": "utiliza condón como método de planificación familiar",
    "generico": "acude a control de planificación familiar",
}


def _o(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " o " + items[-1]


# ---------------------------------------------------------------------------------------------------------------
# piezas por método: aperturas (con {d} = tiempo de uso), síntomas (texto, frases de contexto compatibles),
# contexto sin síntomas, tratamientos, negativos.
_PIEZAS = {
    "oral": dict(
        d=["3 meses", "6 meses", "8 meses", "1 año", "2 años", "3 años"],
        ap=["acude a control de anticonceptivos orales",
            "utiliza anticonceptivos orales desde hace {d} y acude para entrega de su método",
            "acude para continuar sus anticonceptivos orales",
            "acude por un nuevo ciclo de pastillas anticonceptivas",
            "solicita continuar con su método de planificación familiar con pastillas",
            "utiliza anticonceptivos orales como método de planificación familiar y acude a control",
            "acude a control de su método de planificación familiar con pastillas anticonceptivas"],
        sx=[("náuseas leves después de la toma", ["Refiere que desea continuar con el método.", "Refiere que las náuseas mejoran al tomar la pastilla con comida."]),
            ("manchado intermenstrual leve", ["Refiere que desea continuar con el método.", "Refiere que toma su pastilla todos los días."]),
            ("mastalgia leve", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."]),
            ("cefalea leve ocasional", ["Refiere que desea continuar con el método.", "Refiere que toma su pastilla todos los días."]),
            ("aumento de peso", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."]),
            ("acné", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."]),
            ("olvidos ocasionales de pastillas", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."]),
            ("sangrado escaso entre periodos", ["Refiere que desea continuar con el método.", "Refiere que toma su pastilla todos los días."]),
            ("disminución del deseo sexual", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."]),
            ("sensación de hinchazón abdominal", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."])],
        ctx=["Refiere buena tolerancia al método.", "Refiere ciclos menstruales regulares con el método.",
             "Refiere que toma su pastilla todos los días a la misma hora.", "Refiere que desea continuar con el método.",
             "Refiere que no ha tenido molestias con el método."],
        tx=["Recibe anticonceptivos orales combinados.", "Recibe anticonceptivos orales de progestágeno.", "", ""],
        neg=["dolor en pantorrilla", "dolor torácico", "alteraciones visuales", "cefalea intensa", "retraso menstrual",
             "sangrado abundante", "posibilidad de embarazo", "migraña con aura"],
        fijas=[
            "solicita iniciar anticonceptivos orales como método de planificación familiar. Refiere última menstruación hace 5 días y ciclos regulares. Niega posibilidad de embarazo, migraña con aura o antecedente de trombosis.",
            "utiliza anticonceptivos orales de progestágeno mientras da pecho a su bebé y acude a control. Refiere que no ha tenido menstruación desde el parto. Niega sangrado abundante, fiebre o dolor pélvico.",
            "acude por una nueva caja de pastillas anticonceptivas. Refiere que toma su pastilla todos los días a la misma hora y ciclos menstruales regulares. Niega posibilidad de embarazo, cefalea intensa o sangrado abundante.",
            "acude por vómitos y diarrea de 2 días de evolución durante el uso de anticonceptivos orales, con duda sobre la eficacia del método. Refiere que toma su pastilla todos los días. Niega fiebre, sangrado vaginal o dolor pélvico.",
            "acude a control de anticonceptivos orales con olvido de 2 pastillas esta semana. Refiere ciclos menstruales regulares. Niega retraso menstrual, sangrado anormal o dolor pélvico.",
            "utiliza anticonceptivos orales desde hace 2 años y acude para chequeo y entrega de su método. Refiere ciclos menstruales regulares y buena tolerancia. Niega dolor en pantorrilla, dolor torácico o cefalea intensa.",
        ]),
    "depo": dict(
        d=["3 meses", "6 meses", "8 meses", "1 año", "2 años"],
        ap=["acude a aplicación de su inyección anticonceptiva trimestral",
            "utiliza anticonceptivo inyectable trimestral y acude a su control",
            "acude por su dosis trimestral de anticonceptivo inyectable",
            "acude a control del método inyectable trimestral",
            "utiliza inyección anticonceptiva trimestral desde hace {d} y acude para su dosis",
            "acude por la aplicación de su inyección de planificación familiar de cada 3 meses"],
        sx=[("amenorrea desde el inicio del método", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("sangrado irregular", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("aumento de peso", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("cefalea leve", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("mastalgia leve", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("acné", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("manchado ocasional", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."]),
            ("retraso de 2 semanas en la aplicación de su dosis", ["Refiere que su última dosis fue hace 3 meses y 2 semanas.", "Refiere que desea continuar con el método."]),
            ("molestia leve en el sitio de la dosis anterior", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 3 meses."])],
        ctx=["Refiere buena tolerancia al método.", "Refiere que su última dosis fue hace 3 meses.",
             "Refiere que desea continuar con el método.", "Refiere amenorrea desde el inicio del método."],
        tx=["Recibe acetato de medroxiprogesterona trimestral.", "", ""],
        neg=["cefalea intensa", "dolor en pantorrilla", "sangrado abundante", "dolor pélvico", "posibilidad de embarazo",
             "dolor torácico"],
        fijas=[
            "solicita iniciar anticonceptivo inyectable trimestral como método de planificación familiar. Refiere última menstruación hace 5 días y ciclos regulares. Niega posibilidad de embarazo, cefalea intensa o dolor en pantorrilla.",
            "acude para su primera dosis de inyección trimestral tras el parto, mientras da pecho a su bebé. Refiere que no ha tenido menstruación desde el parto. Niega sangrado abundante, fiebre o dolor pélvico.",
            "acude para su dosis de inyección trimestral con 1 semana de retraso. Refiere que su última dosis fue hace 3 meses y 1 semana. Niega relaciones sexuales sin protección en ese tiempo, sangrado anormal o dolor pélvico.",
        ]),
    "mensual": dict(
        d=["2 meses", "4 meses", "8 meses", "1 año"],
        ap=["acude a aplicación de su inyección anticonceptiva mensual",
            "utiliza anticonceptivo inyectable mensual y acude a su control",
            "acude por su dosis mensual de anticonceptivo inyectable",
            "utiliza inyección anticonceptiva mensual desde hace {d} y acude para su dosis"],
        sx=[("sangrado irregular leve", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 1 mes."]),
            ("aumento de peso", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 1 mes."]),
            ("cefalea leve ocasional", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 1 mes."]),
            ("mastalgia leve", ["Refiere que desea continuar con el método.", "Refiere que su última dosis fue hace 1 mes."]),
            ("retraso de 1 semana en la aplicación de su dosis", ["Refiere que su última dosis fue hace 5 semanas.", "Refiere que desea continuar con el método."])],
        ctx=["Refiere buena tolerancia al método.", "Refiere que su última dosis fue hace 1 mes.",
             "Refiere ciclos menstruales regulares con el método.", "Refiere que desea continuar con el método."],
        tx=["", ""],
        neg=["cefalea intensa", "dolor en pantorrilla", "sangrado abundante", "dolor pélvico", "posibilidad de embarazo",
             "dolor torácico"],
        fijas=[
            "solicita iniciar anticonceptivo inyectable mensual como método de planificación familiar. Refiere última menstruación hace 5 días y ciclos regulares. Niega posibilidad de embarazo, cefalea intensa o dolor en pantorrilla.",
        ]),
    "inyectable": dict(
        d=["3 meses", "6 meses", "1 año", "2 años"],
        ap=["acude a aplicación de su anticonceptivo inyectable",
            "utiliza anticonceptivo inyectable y acude a su control",
            "acude por su dosis de anticonceptivo inyectable",
            "utiliza anticonceptivo inyectable desde hace {d} y acude para su dosis"],
        sx=[("amenorrea desde el inicio del método", ["Refiere que desea continuar con el método."]),
            ("sangrado irregular", ["Refiere que desea continuar con el método."]),
            ("aumento de peso", ["Refiere que desea continuar con el método."]),
            ("cefalea leve", ["Refiere que desea continuar con el método."]),
            ("mastalgia leve", ["Refiere que desea continuar con el método."]),
            ("manchado ocasional", ["Refiere que desea continuar con el método."])],
        ctx=["Refiere buena tolerancia al método.", "Refiere que desea continuar con el método.",
             "Refiere que su última dosis fue a tiempo."],
        tx=["", ""],
        neg=["cefalea intensa", "dolor en pantorrilla", "sangrado abundante", "dolor pélvico", "posibilidad de embarazo",
             "dolor torácico"],
        fijas=[]),
    "implante": dict(
        d=["6 meses", "1 año", "2 años", "3 años"],
        ap=["acude a control de implante subdérmico colocado hace {d}",
            "utiliza implante subdérmico como método de planificación familiar y acude a control",
            "acude para revisión de su implante subdérmico",
            "es portadora de implante subdérmico colocado hace {d} y acude a control"],
        sx=[("sangrado irregular escaso", ["Refiere que desea continuar con el método.", "Refiere que palpa el implante en su lugar."]),
            ("amenorrea", ["Refiere que desea continuar con el método.", "Refiere que palpa el implante en su lugar."]),
            ("aumento de peso", ["Refiere que desea continuar con el método.", "Refiere que palpa el implante en su lugar."]),
            ("cefalea leve", ["Refiere que desea continuar con el método.", "Refiere que palpa el implante en su lugar."]),
            ("acné", ["Refiere que desea continuar con el método.", "Refiere que palpa el implante en su lugar."]),
            ("manchado ocasional", ["Refiere que desea continuar con el método.", "Refiere que palpa el implante en su lugar."]),
            ("molestia leve en el brazo donde está el implante", ["Refiere que palpa el implante en su lugar.", "Refiere que desea continuar con el método."])],
        ctx=["Refiere buena tolerancia al método.", "Refiere que palpa el implante en su lugar.",
             "Refiere que desea continuar con el método.", "Refiere ciclos menstruales poco frecuentes desde la colocación."],
        tx=["", ""],
        neg=["dolor en el sitio del implante", "enrojecimiento o secreción en el brazo", "cefalea intensa",
             "dolor pélvico", "posibilidad de embarazo", "sangrado abundante"],
        fijas=[
            "solicita información sobre la duración de su implante subdérmico, colocado hace 3 años. Refiere que palpa el implante en su lugar. Niega sangrado abundante, posibilidad de embarazo o dolor en el sitio del implante.",
            "acude a control de implante subdérmico colocado hace 2 semanas. Refiere molestia leve al presionar el sitio de inserción. Niega fiebre, secreción o salida del implante.",
        ]),
    "diu": dict(
        d=["6 meses", "1 año", "2 años", "4 años"],
        ap=["acude a control de dispositivo intrauterino colocado hace {d}",
            "utiliza dispositivo intrauterino de cobre como método de planificación familiar y acude a revisión",
            "acude a revisión de su DIU",
            "utiliza DIU y acude a control de rutina"],
        sx=[("menstruaciones más abundantes", ["Refiere que desea continuar con el método.", "Refiere que palpa los hilos del DIU."]),
            ("dismenorrea leve", ["Refiere que desea continuar con el método.", "Refiere que palpa los hilos del DIU."]),
            ("manchado entre menstruaciones", ["Refiere que desea continuar con el método.", "Refiere que palpa los hilos del DIU."]),
            ("molestia pélvica leve ocasional", ["Refiere que desea continuar con el método.", "Refiere que palpa los hilos del DIU."]),
            ("dificultad para palpar los hilos del DIU", ["Refiere que desea continuar con el método.", "Refiere ciclos menstruales regulares."])],
        ctx=["Refiere ciclos menstruales regulares.", "Refiere que palpa los hilos del DIU.",
             "Refiere que desea continuar con el método.", "Refiere buena tolerancia al método."],
        tx=["", ""],
        neg=["dolor pélvico intenso", "fiebre", "flujo con mal olor", "sangrado abundante", "retraso menstrual",
             "posibilidad de embarazo", "dolor durante las relaciones sexuales"],
        fijas=[
            "acude a control del DIU colocado hace 6 semanas. Refiere manchado leve las primeras semanas que ya disminuyó. Niega fiebre, dolor pélvico intenso o flujo con mal olor.",
        ]),
    "condon": dict(
        d=["3 meses"],
        ap=["acude por condones como método de planificación familiar y prevención de infecciones",
            "solicita condones como método de planificación familiar",
            "acude a control de planificación familiar con uso de condón",
            "refiere uso de condón en sus relaciones sexuales y solicita reabastecimiento"],
        sx=[("interés en un método de mayor duración", ["Refiere que desea información sobre otras opciones."]),
            ("uso inconsistente del condón", ["Refiere que desea orientación sobre el uso correcto."])],
        ctx=["Refiere pareja estable.", "Refiere que desea protección contra infecciones de transmisión sexual.",
             "Refiere que usa condón en todas sus relaciones sexuales.", "Refiere que desea orientación sobre el uso correcto."],
        tx=["", ""],
        neg=["síntomas genitales", "secreción genital", "ardor al orinar", "úlceras genitales"],
        fijas=[]),
    "generico": dict(
        d=["6 meses", "1 año", "2 años"],
        ap=["acude a control de planificación familiar",
            "acude por entrega de su método de planificación familiar",
            "solicita continuar con su método de planificación familiar",
            "utiliza un método de planificación familiar y acude a control"],
        sx=[("sangrado irregular", ["Refiere que desea continuar con el método."]),
            ("aumento de peso", ["Refiere que desea continuar con el método."]),
            ("cefalea leve", ["Refiere que desea continuar con el método."]),
            ("mastalgia leve", ["Refiere que desea continuar con el método."]),
            ("acné", ["Refiere que desea continuar con el método."]),
            ("náuseas leves", ["Refiere que desea continuar con el método."])],
        ctx=["Refiere buena tolerancia al método.", "Refiere ciclos menstruales regulares.",
             "Refiere que desea continuar con el método.", "Refiere que no ha tenido molestias con el método."],
        tx=["", ""],
        neg=["cefalea intensa", "dolor en pantorrilla", "dolor torácico", "sangrado abundante", "retraso menstrual",
             "posibilidad de embarazo", "dolor pélvico"],
        fijas=[
            "solicita información y orientación para elegir un método de planificación familiar. Refiere ciclos menstruales regulares. Niega posibilidad de embarazo, flujo anormal o dolor pélvico.",
            "acude a control de planificación familiar tras el parto. Refiere que desea espaciar sus embarazos. Niega sangrado abundante, fiebre o dolor pélvico.",
        ]),
}


def _armar(m, total=60):
    p = _PIEZAS[m]
    rng = random.Random("pf-" + m)            # fijo: las versiones son siempre las mismas
    out = list(p["fijas"])
    intentos = 0
    while len(out) < total and intentos < 3000:
        intentos += 1
        ap = rng.choice(p["ap"]).format(d=rng.choice(p["d"]))
        con_sx = rng.random() < 0.65 and p["sx"]
        if con_sx:
            sx, ctxs = rng.choice(p["sx"])
            enlace = rng.choice([", con ", "; se acompaña de "])
            frase = ap + enlace + sx + "."
            ctx = rng.choice(ctxs)
        else:
            frase = ap + "."
            ctx = rng.choice(p["ctx"])
        partes = [frase, ctx]
        tx = rng.choice(p["tx"])
        if tx:
            partes.append(tx)
        if rng.random() < 0.5:
            partes[1:] = partes[1:][::-1]
        neg = rng.sample(p["neg"], rng.choice([2, 3, 3]))
        partes.append("Niega " + _o(neg) + ".")
        v = " ".join(partes)
        if v in out:
            continue
        if len(out) >= 30 and any(difflib.SequenceMatcher(None, v, o, autojunk=False).ratio() > 0.85 for o in out):
            continue                      # de la 31 en adelante no se aceptan versiones casi iguales a otra
        out.append(v)
    return out


def _huella():
    import hashlib
    return hashlib.md5(repr(_PIEZAS).encode("utf-8")).hexdigest()


def _cargar():
    """Las versiones se arman con una semilla fija y tardan unos 25 s en una PC normal; por eso están ya calculadas en
    services/hea_pf_cache.py (se vuelve a generar con tools/hea_pf_cache.py). Si alguien cambia las piezas de arriba y no
    regenera el archivo, la huella no coincide y se calculan aquí (lento pero correcto)."""
    try:
        from services import hea_pf_cache
        if hea_pf_cache.HUELLA == _huella():
            return hea_pf_cache.VERSIONES
    except ImportError:
        pass
    return {m: _armar(m) for m in _PIEZAS}


VERSIONES = _cargar()


def versiones(texto, por_defecto="generico"):
    """Versiones de HEA para el método que dice `texto` (si no dice ninguno, las de `por_defecto`)."""
    return VERSIONES[metodo(texto) or por_defecto]


def sintoma(texto, por_defecto="generico"):
    return SINTOMA[metodo(texto) or por_defecto]
