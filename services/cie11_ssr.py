"""Lista cerrada de diagnósticos de «Diagnóstico SSR» de ActivityInfo (formulario «Morbilidad APS», activos con
APS/SSR = SSR o «APS, SSR»): 105 opciones con su código CIE-11. Es aparte de la lista de Atención primaria
(services/cie11_catalog.py); 29 opciones están en las dos. Al elegir la descripción, ActivityInfo pone el código."""
from services.cie11_catalog import plain, re

_RAW = """
Forúnculo|1B75.0
Maltrato sexual|PJ21
Candidiasis vulvovaginal|1F23.10
Contacto con o exposición a enfermedades infecciosas con un modo de transmisión predominantemente sexual|QC90.2
Dismenorrea|GA34.3
Enfermedad por virus de la inmunodeficiencia humana, sin mención de tuberculosis o malaria, sin especificación|1C62.Z
Menopausia, sin especificación|GA30.0Z
Falta del desarrollo fisiológico normal esperado, sin especificación|MG44.1Z
Hernias, sin especificación|DD5Z
Hiperplasia de la próstata|GA90
Infección urinaria, localización y microbio patógeno no especificados|GC08.Z
Leiomioma del útero|2E86.0
Sentirse enfermo|MG25
Tumor o masa en el seno femenino (nódulo mamario)|MF30
Mastodinia|GB23.5
Menstruación excesiva con ciclo irregular|GA22
Regularidad anormal del sangrado uterino|GA20.3
Amenorrea|GA20.0
Otra hipofunción especificada u otros trastornos de la glándula hipófisis|5A61.Y
Prostatocistitis|GA91.2
Erupción, sin especificación|ME66.6Z
Seguimiento de rutina del posparto|QA48.2
Supervisión de embarazo normal, sin especificación|QA42.Z
Vaginitis aguda|GA02.0
Verrugas genitales|1A95.1
Vulvitis aguda|GA00.0
Lesión de la piel de naturaleza incierta o no especificada, sin especificación|ME60.Z
Examen de salud de rutina del niño|QA00.1
Examen ginecológico|QA00.9
Examen o prueba de embarazo|QA40
Trastornos inflamatorios de la mama, sin especificación|GB21.Z
Estado de embarazo|QA41
Contacto con los servicios de salud para consejo sobre menopausia.|QA4B
Contacto con los servicios de salud para asesoramiento o consejo general sobre anticoncepción|QA21.1
Infecciones Transmitidas Sexualmente|1A9Z
Contacto con los servicios de salud para atención relativa a la anticoncepción|QA21
Consideraciones etiológicas en las disfunciones sexuales y los trastornos sexuales por dolor|HA40
Adolescencia|XT7M
Amenaza de aborto|JA40.0
Amenorrea por embarazo|GA20.0Y
Asesoramiento relacionado con la sexualidad, sin especificación|QA15.Z
Cáncer de ovario|2C73
Contacto con los servicios de salud para anticoncepción poscoital|QA21.0
Contacto con los servicios de salud para inserción de dispositivo anticonceptivo|QA21.2
Contacto con los servicios de salud por preocupaciones acerca del embarazo|QA20
Desnutrición en el embarazo|JA64
Disfunciones sexuales, sin especificación|HA0Z
Dolor pélvico femenino asociado a órganos genitales o ciclo menstrual|GA34
Eclampsia en el embarazo|JA25.0
Edema gestacional sin hipertensión|JA22.1
Enfermedades endocrinas, nutricionales o metabólicas que complican el embarazo, el parto o el puerperio|JB64.2
Hepatitis B aguda|1E50.1
Hepatitis B crónica|1E51.0
Hipertensión gestacional|JA23
Incontinencia urinaria de esfuerzo|MF50.20
Infección genital o urogenital por herpes simple|1A94.0
Molusco contagioso|1E+76
Neoplasia benigna de la mama|2F30
Neoplasias malignas de la vagina|2C71
Neoplasias malignas de la vulva|2C70
Neoplasias malignas del ano o del conducto anal|2C00
Neoplasias malignas del cuello uterino|2C77
Neoplasias malignas del pene|2C81
Otra hemorragia especificada al comienzo del embarazo|JA40.Y
Preeclamsia, sin especificación|JA24.Z
Prepucio redundante, fimosis o parafimosis|GB05
Sarcoma de Kaposi, localización primaria|2B57
Síntoma o molestia premenstrual|MF33
Trastornos hemorrágicos del ciclo menstrual|GA20
Trastornos metabólicos, sin especificación|5D2Z
Trastornos premenstruales|GA34.4
Vómitos excesivos en el embarazo, sin especificación|JA60.Z
Cuidado de la Propia Salud|VW25
Balanopostitis|GB06.0
Galactorrea|JB46.6
Enfermedades endócrinas, sin especificación|5B3Z
Hemorragia uterina y vaginal anormal, sin especificación|GA2Z
Enfermedades del aparato genital masculino sin especificación|GB0Z
Trastornos de la mama sin especificación|GB2Z
Carcinoma in situ de sitio sin especificación|2E6Z
Neoplasias benignas, excepto las de tejidos linfáticos o hematopoyéticos, del sistema nervioso central o de tejidos afines, sin especificación|2F5Z
Neoplasias de comportamiento incierto, excepto las de tejidos linfoide o hematopoyéticas, el sistema nervioso central o tejidos afines, sin especificación|2F7Z
Neoplasias de comportamiento desconocido, excepto los de tejidos linfáticos, hematopoyéticos, los del sistema nervioso central, o los de tejidos relacionados, sin especificación|2F9Z
Enfermedades de la piel, sin especificación|EM0Z
Enfermedades del sistema genitourinario, sin especificación|GC8Z
Condiciones relacionadas con la salud sexual, sin especificación|HA8Z
Embarazo que finaliza en aborto, sin especificación|JA0Z
Edema, proteinuria o trastornos hipertensivos en el embarazo, el parto o el puerperio, sin especificación|JA2Z
Hemorragia obstétrica, sin especificación|JA4Z
Trastornos maternos relacionados principalmente con el embarazo, sin especificación|JA6Z
Atención materna relacionada al feto, cavidad amniótica o con posibles problemas en el parto, sin especificación|JA8Z
Complicaciones del trabajo de parto o del parto, sin especificación|JB0Z
Parto, sin especificación|JB2Z
Complicaciones principalmente relacionadas con el puerperio, sin especificación|JB4Z
Complicación obstétrica, sin especificación|JB6Z
Afecciones que se originan en el período perinatal o neonatal, sin especificación|KD5Z
Otros síntomas, signos o hallazgos clínicos especificados no clasificados en otra parte.|MH2Y
Causas externas de morbilidad o mortalidad, sin especificación|PL2Z
Factores que influyen en el estado de salud o el contacto con los servicios de salud, sin especificación|QF4Z
Prepucio redundante, fimosis o parafimosis, sin especificación|GB05.Z
Vaginosis bacteriana|MF3A
Mastitis puerperal|JB45.0
Cervicitis|GA04
Neoplasias malignas de mama, sin especificación|2C6Z
Prurito vulvar|GA42.0
"""
CATALOG = [tuple(line.rsplit("|", 1)) for line in _RAW.strip().splitlines()]
BY_DESC = {d: c for d, c in CATALOG}


def label(desc):
    return f"{desc}  [{BY_DESC.get(desc, '')}]"


def descriptions():
    return [d for d, _c in CATALOG]


def from_label(text):
    """(descripcion, codigo) a partir de lo elegido en el selector; ('', '') si no está en la lista SSR."""
    t = (text or "").strip()
    if "  [" in t and t.endswith("]"):
        t = t.rsplit("  [", 1)[0]
    if t in BY_DESC:
        return t, BY_DESC[t]
    p = plain(t)
    for d, c in CATALOG:
        if plain(d) == p:
            return d, c
    return "", ""


# Abreviaturas/diagnósticos frecuentes del ATA en pacientes de SSR → texto a buscar (solo sugerencia).
SINONIMOS = {
    "pf": "Contacto con los servicios de salud para atención relativa a la anticoncepción",
    "pf acos": "Contacto con los servicios de salud para atención relativa a la anticoncepción",
    "pf aco": "Contacto con los servicios de salud para atención relativa a la anticoncepción",
    "planificacion familiar": "Contacto con los servicios de salud para atención relativa a la anticoncepción",
    "anticoncepcion": "Contacto con los servicios de salud para atención relativa a la anticoncepción",
    "its": "Infecciones Transmitidas Sexualmente", "ets": "Infecciones Transmitidas Sexualmente",
    "vaginosis": "Vaginosis bacteriana", "vaginosis mixta": "Vaginosis bacteriana",
    "vaginosis bacteriana": "Vaginosis bacteriana", "vaginitis": "Vaginitis aguda",
    "candidiasis vaginal": "Candidiasis vulvovaginal", "candidiasis vag": "Candidiasis vulvovaginal",
    "candidiasis": "Candidiasis vulvovaginal", "vulvovaginitis": "Vaginitis aguda",
    "dismenorrea": "Dismenorrea", "amenorrea": "Amenorrea", "menopausia": "Menopausia, sin especificación",
    "climaterio": "Menopausia, sin especificación", "cpn": "Supervisión de embarazo normal, sin especificación",
    "control prenatal": "Supervisión de embarazo normal, sin especificación",
    "embarazo": "Estado de embarazo", "prueba de embarazo": "Examen o prueba de embarazo",
    "ivu": "Infección urinaria, localización", "itu": "Infección urinaria, localización",
    "infeccion urinaria": "Infección urinaria, localización", "cervicitis": "Cervicitis",
    "mastodinia": "Mastodinia", "mastitis": "Mastitis puerperal", "nodulo mamario": "Tumor o masa en el seno femenino",
    "papanicolau": "Examen ginecológico", "citologia": "Examen ginecológico", "examen ginecologico": "Examen ginecológico",
    "vih": "Enfermedad por virus de la inmunodeficiencia humana", "herpes genital": "Infección genital o urogenital por herpes",
    "condilomas": "Verrugas genitales", "verrugas genitales": "Verrugas genitales", "hpb": "Hiperplasia de la próstata",
    "prurito vulvar": "Prurito vulvar", "leucorrea": "Vaginitis aguda", "flujo vaginal": "Vaginitis aguda",
    "sangrado uterino anormal": "Hemorragia uterina y vaginal anormal", "sua": "Hemorragia uterina y vaginal anormal",
    "posparto": "Seguimiento de rutina del posparto", "puerperio": "Seguimiento de rutina del posparto",
}


def suggest(text, limit=1, estricto=False):
    """Mejores coincidencias de la lista SSR para el texto del ATA (la persona confirma en la ventana)."""
    q = " ".join(plain(text).split())
    if not q:
        return []
    sin = {" ".join(plain(k).split()): v for k, v in SINONIMOS.items()}
    if q in sin:
        q = plain(sin[q])
        estricto = False
        exacto_sin = True
    elif q.startswith("pf "):         # «PF (Depo)», «PF (ACOs) 3 meses», «PF implante»…: todos van a la misma opción de SSR
        q = plain(SINONIMOS["pf"])
        estricto = False
        exacto_sin = True
    else:
        exacto_sin = False
    words = [w for w in q.split() if len(w) > 2]
    corta = len(q) <= 4
    scored = []
    for d, c in CATALOG:
        p = plain(d)
        pal = p.split()
        if estricto and p != q:
            continue          # en modo estricto solo vale el nombre exacto o un sinónimo conocido (no coincidencias parciales)
        if p == q:
            s = 100
        elif p.startswith(q + " ") or (not corta and p.startswith(q)):
            s = 80
        elif (q in pal) if corta else (q in p):
            s = 60
        elif words and all(w in p for w in words) and not corta:
            s = 40
        else:
            continue
        scored.append((s - len(p) / 1000.0, d, c))
    scored.sort(key=lambda x: -x[0])
    return [(d, c) for _s, d, c in scored[:limit]]
