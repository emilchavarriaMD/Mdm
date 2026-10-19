"""Arma la HEA de un paciente con 1, 2 o 3 diagnósticos a partir del banco de versiones (hea_data.BANK).

Reglas (una sola historia, no tres pegadas):
  1. Los diagnósticos crónicos van juntos como «antecedente de …».
  2. El primer diagnóstico agudo (en el orden del ATA) da el cuadro actual: se elige una de sus versiones.
  3. Los demás diagnósticos agudos se agregan como síntomas («Además refiere …»).
  4. Los motivos de contacto/estados (embarazo, anticoncepción, controles…) van como cláusula aparte.
  5. Del cuadro principal se quitan los «Niega …» que contradigan los otros diagnósticos.
"""
import random
import re

from services import cie11_catalog as cat
from services.hea_data import ALIAS, BANK

_ID = {}
for _n, _b in BANK.items():
    _ID.setdefault(cat.plain(_b["n"]), _n)
for _n, _desc in ALIAS.items():
    _ID[cat.plain(_desc)] = _n


def bank_id(descripcion):
    """Número del banco para una descripción de la lista de ActivityInfo (o None si no hay HEA para ella)."""
    return _ID.get(cat.plain(descripcion))


def _frases(texto):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", texto.strip()) if s.strip()]


def _raices(textos):
    return {w[:5] for t in textos for w in cat.plain(t).split() if len(w) >= 5}


def _filtrar_negativos(frase, raices):
    """'Niega a, b o c.' → quita los ítems que mencionan algo que otro diagnóstico sí presenta."""
    cuerpo = frase[len("Niega "):].rstrip(". ")
    items = [i.strip() for i in re.split(r",\s+|\s+o\s+|\s+ni\s+", cuerpo) if i.strip()]
    quedan = [i for i in items if not any(r in cat.plain(i) for r in raices)]
    if not quedan:
        return ""
    if len(quedan) == 1:
        return f"Niega {quedan[0]}."
    return "Niega " + ", ".join(quedan[:-1]) + " o " + quedan[-1] + "."


def _lista(items):
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " y " + items[-1]


def cabecera(sexo, edad, unidad="años"):
    """«Beneficiaria Fem de 30 años de edad, que presenta » (sexo: M mujer, H hombre, como en el ATA)."""
    s = (sexo or "").upper()
    quien = {"M": "Beneficiaria Fem", "H": "Beneficiario Masc"}.get(s, "Beneficiaria/o Fem/Masc")
    edad = (str(edad or "")).strip()
    de = f" de {edad} {unidad}{'' if unidad.endswith('s') else 's'} de edad" if edad else ""
    return f"{quien}{de}, que presenta "


def compose(sexo, edad, dx_descripciones, unidad="años", rng=None):
    """Devuelve (texto, avisos). dx_descripciones: descripciones de la lista de ActivityInfo (máx. 3)."""
    rng = rng or random
    avisos = []
    items = []
    for d in [x for x in dx_descripciones if x and x.strip()][:3]:
        n = bank_id(d)
        if n is None:
            avisos.append(f"No hay HEA preparada para «{d}»; complete ese diagnóstico a mano.")
            items.append(dict(n=None, k="S", t=re.sub(r",? sin especificación$", "", d).lower(), v=[], desc=d))
        else:
            b = BANK[n]
            items.append(dict(n=n, k=b["k"], t=b["t"], v=b["v"], desc=d, s=b["s"]))
            if b["s"] == "F" and (sexo or "").upper() == "H":
                avisos.append(f"«{d}» es propio de mujeres y el paciente figura como hombre.")
            if b["s"] == "M" and (sexo or "").upper() == "M":
                avisos.append(f"«{d}» es propio de hombres y la paciente figura como mujer.")
    head = cabecera(sexo, edad, unidad)
    if not items:
        return "HEA: " + head.replace(", que presenta ", "") + " que acude a consulta. El ATA no registra diagnóstico.", avisos

    cron = [i for i in items if i["k"] == "C"]
    agud = [i for i in items if i["k"] == "S"]
    ctx = [i for i in items if i["k"] == "X"]
    if agud:
        principal = next((i for i in agud if i["v"]), agud[0])
    elif cron:
        principal = cron[0]
    else:
        principal = ctx[0]
    otros_c = [i for i in cron if i is not principal]
    otros_s = [i for i in agud if i is not principal]
    otros_x = [i for i in ctx if i is not principal]

    if principal["v"]:
        version = rng.choice(principal["v"])
    else:                                   # diagnóstico sin banco
        version = principal["t"]
    ya = _raices([version])
    otros_s = [i for i in otros_s if not (_raices([i["t"]]) and _raices([i["t"]]) <= ya)]   # no repetir lo ya dicho
    frases = _frases(version)
    neg = [f for f in frases if f.startswith("Niega ")]
    cuerpo = [f for f in frases if not f.startswith("Niega ")]
    cuerpo_txt = " ".join(cuerpo)

    # 1) antecedentes crónicos juntos
    labels = [i["t"] for i in otros_c]
    if principal["k"] == "C":
        if cuerpo_txt.lower().startswith("antecedente de "):
            resto = cuerpo_txt[len("antecedente de "):]
            texto = "antecedente de " + (_lista(labels) + " y " if labels else "") + resto
        else:
            texto = ("antecedente de " + _lista([principal["t"]] + labels) + "; " + cuerpo_txt) if cuerpo_txt else \
                    "antecedente de " + _lista([principal["t"]] + labels)
    else:
        ant = ("antecedente de " + _lista(labels) + " y cuadro actual de ") if labels else ""
        texto = ant + cuerpo_txt
    if not texto.endswith((".", "!", "?")):
        texto += "."
    # 2) otros agudos como síntomas
    if otros_s:
        texto += " Además refiere " + _lista([i["t"] for i in otros_s]) + "."
    # 3) contexto / motivos
    for i in otros_x:
        t = i["t"]
        texto += " Además, " + t + "."
    # 4) negativos compatibles
    raices = _raices([i["t"] for i in otros_s] + [i["t"] for i in otros_c] + [i["t"] for i in otros_x])
    for f in neg:
        g = _filtrar_negativos(f, raices) if raices else f
        if g:
            texto += " " + g
    return "HEA: " + head + texto, avisos
