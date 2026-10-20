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
from services import hea_pf
from services.hea_data import ALIAS, BANK, SINONIMOS
from services.hea_data_gen import ALIAS_GEN, BANK_GEN

# El banco generado (tools/hea_gen.py) reemplaza las versiones de los diagnósticos que tienen ficha clínica nueva
# y agrega los de la lista SSR que no existían.
BANK.update(BANK_GEN)
# Planificación familiar: la HEA habla del método que dice el ATA (ACOs, DEPO, implante, DIU, condón…): services/hea_pf.py.
BANK[326]["v"] = hea_pf.VERSIONES["oral"]
BANK[152]["v"] = hea_pf.VERSIONES["generico"]
_PF = (152, 326)
SINONIMOS = dict(SINONIMOS)
SINONIMOS.update({"vaginosis": 1001, "vaginosis mixta": 1001, "vaginosis bacteriana": 1001,
                  "dismenorrea": 1007, "cervicitis": 1002, "mastitis": 1005, "mastitis puerperal": 1005,
                  "aborto": 1008, "preeclampsia": 1006, "herpes genital": 1004, "fimosis": 1018,
                  "pf": 152, "pf implante": 152, "pf jadelle": 152, "pf condon": 152, "pf preservativo": 152,
                  "pf mensual": 152, "pf trimestral": 152, "implante subdermico": 152})

def _np(t):
    """Texto sin tildes ni mayúsculas y con un solo espacio entre palabras («PF (ACOs)» → «pf acos»)."""
    return " ".join(cat.plain(t).split())


_ID = {}
for _n, _b in BANK.items():
    _ID.setdefault(_np(_b["n"]), _n)
for _n, _desc in ALIAS.items():
    _ID[_np(_desc)] = _n
for _desc, _n in ALIAS_GEN:
    _ID[_np(_desc)] = _n


_SIN = {_np(k): v for k, v in SINONIMOS.items()}


def bank_id(texto):
    """Número del banco para una descripción de ActivityInfo o un diagnóstico/abreviatura del ATA (None si no hay)."""
    p = _np(texto)
    if not p:
        return None
    if p in _ID:
        return _ID[p]
    if p in _SIN:
        return _SIN[p]
    for k, n in _SIN.items():          # «HTA crónica», «gastritis aguda», «PF (ACOS) 3 meses»…
        if len(k) > 3 and (p.startswith(k + " ") or p.endswith(" " + k)):
            return n
    for k, n in _SIN.items():          # «cuerpo extraño oído izq. 1 día»
        if len(k) > 6 and p.startswith(k):
            return n
    for k, n in _ID.items():           # «Gastritis» → «Gastritis, sin especificación»
        if k.startswith(p + " ") and len(p) > 4:
            return n
    if p.startswith("pf "):            # «PF (Jadelle) 3 meses», «PF (ACOs) y condón»…: planificación según el método
        m = hea_pf.metodo(p)
        return 326 if m == "oral" else 171 if m == "diu" else 152
    return None


_EN_LISTA = {cat.plain(d): d for d, _c in cat.CATALOG}


def sugerir_lista(abrev):
    """Sugerencia de la lista de ActivityInfo para un diagnóstico del ATA: primero lo que dice el banco de HEA
    (que conoce las abreviaturas: SDA, OMA, PF…), si ese diagnóstico existe en la lista; si no, la búsqueda por texto.
    Devuelve (descripción, código) o ("", "")."""
    n = bank_id(abrev)
    if n is not None:
        for nombre in (ALIAS.get(n), BANK[n]["n"]):
            d = _EN_LISTA.get(cat.plain(nombre or ""))
            if d:
                return cat.from_label(d)
    sug = cat.suggest(abrev)
    return sug[0] if sug else ("", "")


def fuente_hea_ssr(abrev, descripcion, es_sugerencia):
    """Texto para la HEA de SSR de una fila. La lista de SSR dice «…atención relativa a la anticoncepción» sin el método;
    el ATA dice «PF (ACOs)». Si la fila de SSR sigue siendo la sugerencia automática y el banco conoce el diagnóstico del
    ATA, se usa el texto del ATA (así la HEA habla de pastillas y no de la inyección); si la persona eligió otra
    opción en la lista, esa."""
    if es_sugerencia and abrev and bank_id(abrev) is not None:
        return abrev
    return descripcion or abrev


def fuente_hea(abrev, descripcion):
    """Qué texto usar para la HEA de una fila: el diagnóstico del ATA si el banco lo conoce y la persona dejó la
    sugerencia automática (más específico: «Cervicalgia» antes que «Afecciones de la columna»); si la persona eligió
    otra opción en la lista, esa."""
    if abrev and bank_id(abrev) is not None:
        sug = sugerir_lista(abrev)[0]
        if not descripcion or sug == descripcion or bank_id(descripcion) == bank_id(abrev):
            return abrev
    return descripcion or abrev


# Enfermedades crónicas que algunas versiones mencionan de paso («…hipertensión arterial y diabetes mellitus…»):
# esa versión solo se usa si el paciente realmente tiene ese diagnóstico.
_MENCIONES = [
    (r"(?<!sin )\bdiabet", {38, 66, 141}),
    (r"\bhipertensi[oó]n\b|\bhta\b", {64, 206, 238, 183}),
    (r"\basma\b", {15, 16}),
    (r"renal cr[oó]nica|insuficiencia renal", {191, 213}),
    (r"\bvih\b", {48, 247}),
    (r"\bepilep", {50}),
    (r"\bobesidad\b", {227}),
]


# Detalles que no encajan con la edad o el sexo del paciente (la versión se descarta si hay otras).
_ADULTO = r"trabaj|laboral|jornada|oficina|computadora|pareja|relaci[oó]n(es)? sexual|tabaqu|fuma|alcohol|cerveza|" \
          r"embaraz|anticoncep|menopaus|jubil|nietos|esposa|esposo|hijos"
_BEBE = r"pa[nñ]al|lactancia|tomas? de leche|biber[oó]n|amamant"
_NINO = _BEBE + r"|seg[uú]n refiere la madre|refiere la madre|la madre refiere|escuela|maestr|jugando|jugaba|ni[nñ]os de su edad"
_SOLO_MUJER = r"menstrua|embaraz|vagin|vulv|anticoncep|[uú]tero|ovario|amamant|regla\b|mamas?\b|pez[oó]n"
_SOLO_HOMBRE = r"pr[oó]stat|escroto|test[ií]cul|\bpene\b|glande|prepucio"


def _edad_anios(edad, unidad):
    try:
        n = float(str(edad).strip())
    except (TypeError, ValueError):
        return None
    return n if (unidad or "años").startswith("a") else n / (12 if (unidad or "").startswith("m") else 365)


def _version_ok(version, ids, sexo=None, anios=None):
    cuerpo = " ".join(f for f in _frases(version) if not f.startswith("Niega "))
    low = cuerpo.lower()
    if re.search(r"embarazo actual|gestaci[oó]n actual|\bgestante\b|semanas de gestaci", low) and not any(
            n in BANK and re.search(r"embarazo|gestacional|prenatal|aborto", BANK[n]["n"].lower()) for n in ids):
        return False                       # no se dice «embarazo actual» si ningún diagnóstico es de embarazo
    for patron, propios in _MENCIONES:
        if re.search(patron, low) and not (propios & ids):
            return False
    if anios is not None:
        if anios < 12 and (re.search(_ADULTO, low) or "automedic" in low):
            return False
        if anios < 3 and re.search(r"refiere\b(?! la madre)", low) and "madre" not in low and "familiar" not in low:
            pass   # en lactantes la historia la da un familiar; no se descarta solo por eso
        if anios >= 3 and re.search(_BEBE, low):
            return False
        if anios >= 15 and re.search(_NINO, low):
            return False
    s = (sexo or "").upper()
    if s == "H" and re.search(_SOLO_MUJER, low):
        return False
    if s == "M" and re.search(_SOLO_HOMBRE, low):
        return False
    return True


def _frases(texto):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", texto.strip()) if s.strip()]


# Palabras demasiado generales para decidir si un «Niega …» contradice a otro diagnóstico.
_GENERALES = set("""del las los con por sin una uno que para como mas muy otro otra otros otras dolor dolores lesion
lesiones leve leves intenso intensa region zona piel aumento volumen sensacion evolucion cuadro sintomas signos
ocasional ocasionales general malestar presenta propios propias ambos ambas lado derecho derecha izquierdo izquierda
parte partes tipo dias semanas meses horas""".split())


def _raices(textos):
    return {w[:5] for t in textos for w in cat.plain(t).split() if len(w) >= 3 and w not in _GENERALES}


def _menciona(texto, raices):
    return any(w[:5] in raices for w in cat.plain(texto).split() if len(w) >= 3 and w not in _GENERALES)


def _filtrar_negativos(frase, raices, otros_textos=""):
    """'Niega a, b o c.' → quita los ítems que mencionan algo que otro diagnóstico sí presenta."""
    cuerpo = frase[len("Niega "):].rstrip(". ")
    items = [i.strip() for i in re.split(r",\s+|\s+[ou]\s+|\s+ni\s+", cuerpo) if i.strip()]
    otros = cat.plain(otros_textos)
    # «Niega dolor» a secas choca con un segundo diagnóstico doloroso
    quedan = [i for i in items if not _menciona(i, raices) and not (cat.plain(i) in _GENERALES and cat.plain(i)[:4] in otros)]
    if not quedan:
        return ""
    if len(quedan) == 1:
        return f"Niega {quedan[0]}."
    return "Niega " + ", ".join(quedan[:-1]) + f" {_o(quedan[-1])} " + quedan[-1] + "."


def _y(siguiente):
    """«y» → «e» ante palabra que empieza con sonido i («asma e hipertensión»)."""
    w = cat.plain(siguiente).split()[0] if cat.plain(siguiente) else ""
    return "e" if (w.startswith("i") or (w.startswith("hi") and not w.startswith(("hie", "hia")))) else "y"


def _o(siguiente):
    """«o» → «u» ante palabra que empieza con sonido o («fiebre u otalgia»)."""
    w = cat.plain(siguiente).split()[0] if cat.plain(siguiente) else ""
    return "u" if w.startswith(("o", "ho")) else "o"


def _lista(items):
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + f" {_y(items[-1])} " + items[-1]


def cabecera(sexo, edad, unidad="años"):
    """«Beneficiaria Fem de 30 años de edad, que presenta » (sexo: M mujer, H hombre, como en el ATA)."""
    s = (sexo or "").upper()
    quien = {"M": "Beneficiaria Fem", "H": "Beneficiario Masc"}.get(s, "Beneficiaria/o Fem/Masc")
    edad = (str(edad or "")).strip()
    unidad = (unidad or "años").strip()
    if edad == "1":
        unidad = {"años": "año", "meses": "mes", "días": "día"}.get(unidad, unidad)
    de = f" de {edad} {unidad} de edad" if edad else ""
    return f"{quien}{de}, que presenta "


def _ya_mencionado(item, texto_low):
    """¿La versión elegida ya nombra esta enfermedad crónica? (para no escribirla dos veces)."""
    for patron, propios in _MENCIONES:
        if item["n"] in propios and re.search(patron, texto_low):
            return True
    return cat.plain(item["t"]) in cat.plain(texto_low)

_NO_EXTRA = re.compile(r"embaraz|gestaci|anticoncep|menopaus|ni[nñ]|madre|escuela|\bmeses de edad", re.I)


def _secundarios(otros_s, principal, cuerpo_principal, ids, sexo, anios, rng):
    """Para cada diagnóstico agudo que no es el principal: (cuadro, un dato extra, negativos). Se toma de una de sus
    versiones del banco para que no quede en una sola palabra; los dos primeros llevan dato extra y negativos."""
    out = []
    contra = _raices([cuerpo_principal])
    for k, i in enumerate(otros_s):
        if not i["v"]:
            continue
        buenas = ([v for v in i["v"] if _version_ok(v, ids, sexo, anios)] or [v for v in i["v"] if _version_ok(v, ids)]
                  or i["v"])
        fr = _frases(rng.choice(buenas))
        cuadro = fr[0].rstrip(". ")
        if cuadro.lower().startswith(("refiere ", "presenta ")):
            cuadro = cuadro.split(" ", 1)[1]
        if re.match(r"\d", cuadro):                      # «3 días de evolución con…» → «cuadro de 3 días de evolución con…»
            cuadro = "cuadro de " + cuadro
        elif cuadro.lower().startswith("acude a "):
            cuadro = "cuadro que motiva consulta: " + cuadro[8:]
        extra, nieg = "", ""
        if k < 2:
            extra = next((f for f in fr[1:] if not f.startswith("Niega ") and not f.startswith("No ha recibido")
                          and not _NO_EXTRA.search(f)), "")
            ng = next((f for f in fr[1:] if f.startswith("Niega ")), "")
            if ng:
                nieg = _filtrar_negativos(ng, contra | _raices([cuadro]), cuerpo_principal)
        out.append((cuadro, extra, nieg))
    return out


def compose(sexo, edad, dx_descripciones, unidad="años", rng=None):
    """Devuelve (texto, avisos). dx_descripciones: descripciones de la lista de ActivityInfo (máx. 3)."""
    rng = rng or random
    avisos = []
    items = []
    vistos = set()
    anios = _edad_anios(edad, unidad)
    for d in [x for x in dx_descripciones if x and x.strip()][:4]:
        n = bank_id(d)
        if n is not None and n in vistos:      # el mismo diagnóstico dos veces
            continue
        vistos.add(n)
        if n is None:
            avisos.append(f"No hay HEA preparada para «{d}»; complete ese diagnóstico a mano.")
            items.append(dict(n=None, k="S", t=re.sub(r",? sin especificación$", "", d).strip().lower(), v=[], desc=d))
        else:
            b = BANK[n]
            v, t = b["v"], b["t"]
            if n in _PF:                   # planificación familiar: versiones y frase del método que dice el ATA
                m = hea_pf.metodo(d) or ("oral" if n == 326 else "generico")
                v, t = hea_pf.VERSIONES[m], hea_pf.SINTOMA[m]
            elif n == 171 and _np(d).startswith("pf "):    # «PF DIU»: colocación o control (el ATA no lo distingue)
                v = list(v) + hea_pf.VERSIONES["diu"]
            items.append(dict(n=n, k=b["k"], t=t, v=v, desc=d, s=b["s"]))
            if b["s"] == "F" and (sexo or "").upper() == "H":
                avisos.append(f"«{d}» es propio de mujeres y el paciente figura como hombre.")
            if b["s"] == "M" and (sexo or "").upper() == "M":
                avisos.append(f"«{d}» es propio de hombres y la paciente figura como mujer.")
            if b["u"] in ("meses", "días") and anios is not None and anios >= 3:
                avisos.append(f"«{d}» es propio de lactantes o recién nacidos; revise la edad o el diagnóstico.")
    head = cabecera(sexo, edad, unidad)
    if not items:
        return head.replace(", que presenta ", "") + " que acude a consulta. El ATA no registra diagnóstico.", avisos

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

    ids = {i["n"] for i in items if i["n"] is not None}
    if principal["v"]:
        buenas = ([v for v in principal["v"] if _version_ok(v, ids, sexo, anios)]
                  or [v for v in principal["v"] if _version_ok(v, ids)] or principal["v"])
        version = rng.choice(buenas)
    else:                                   # diagnóstico sin banco
        version = principal["t"]
    ya = _raices([version])
    otros_s = [i for i in otros_s if not (_raices([i["t"]]) and _raices([i["t"]]) <= ya)]   # no repetir lo ya dicho
    frases = _frases(version)
    neg = [f for f in frases if f.startswith("Niega ")]
    cuerpo = [f for f in frases if not f.startswith("Niega ")]
    cuerpo_txt = " ".join(cuerpo)

    # 1) antecedentes crónicos juntos
    low_v = cuerpo_txt.lower()
    labels = [i["t"] for i in otros_c if not _ya_mencionado(i, low_v)]
    if principal["k"] == "C":
        if cuerpo_txt.lower().startswith("antecedente de "):
            resto = cuerpo_txt[len("antecedente de "):]
            texto = "antecedente de " + (_lista(labels) + f" {_y(resto)} " if labels else "") + resto
        else:
            texto = ("antecedente de " + _lista([principal["t"]] + labels) + "; " + cuerpo_txt) if cuerpo_txt else \
                    "antecedente de " + _lista([principal["t"]] + labels)
    else:
        if labels and re.match(r"(acude|refiere|solicita|desea|utiliza|se encuentra|cursa|requiere)\b", cuerpo_txt):
            ant = "antecedente de " + _lista(labels) + ". Actualmente "
        elif labels and cuerpo_txt.lower().startswith("cuadro"):
            ant = "antecedente de " + _lista(labels) + " y "
        else:
            ant = ("antecedente de " + _lista(labels) + " y cuadro actual de ") if labels else ""
        texto = ant + cuerpo_txt
    if not texto.endswith((".", "!", "?")):
        texto += "."
    # 2) los otros diagnósticos agudos se cuentan con su propio cuadro (descripción, algún dato y sus negativos)
    sec = _secundarios(otros_s, principal, cuerpo_txt, ids, sexo, anios, rng)
    # 3) negativos del cuadro principal (sin los que contradicen a los otros diagnósticos), pegados a su cuadro
    raices = _raices([i["t"] for i in otros_s] + [i["t"] for i in otros_c] + [i["t"] for i in otros_x]
                     + [c for c, _x, _n in sec])
    for f in neg:
        g = _filtrar_negativos(f, raices, " ".join(i["t"] for i in otros_s + otros_c + otros_x)) if raices else f
        if g:
            texto += " " + g
    for j, (cuadro, extra, nieg) in enumerate(sec):
        texto += (" Además refiere " if j == 0 else " También refiere ") + cuadro + "."
        if extra:
            texto += " " + extra
        if nieg:
            texto += " " + nieg
    for i in otros_s[len(sec):]:
        texto += " Además refiere " + i["t"] + "."
    # 4) contexto / motivos
    for j, i in enumerate(otros_x):
        texto += (" Además, " if (j == 0 and not otros_s) else " Asimismo, ") + i["t"] + "."
    if re.match(r"(acude|refiere|solicita|desea|utiliza|se encuentra|cursa|requiere)\b", texto):
        head = head.replace(", que presenta ", ", que ")     # «…de edad, que acude a control…»
    return head + texto, avisos
