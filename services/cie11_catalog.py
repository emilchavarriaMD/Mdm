"""Lista cerrada de «Descripción de la morbilidad CIE-11» de ActivityInfo (formulario de Atención primaria
de salud), leída tal cual del formulario. El código se completa solo en ActivityInfo al elegir la descripción.
Funciona sin internet y no depende de ninguna API."""
import re
import unicodedata

_RAW = """
Absceso periapical, sin especificación|DA09.6Z
Absceso piógeno de la piel|1B75.3
Adolescencia|XT7M
Afecciones alérgicas o de hipersensibilidad, sin especificación|4A8Z
Afecciones asociadas con la columna vertebral, sin especificación|FB1Z
Afecciones de la rótula|FA32
Aftas o úlceras aftoides de la boca|DA01.10
Algunas enfermedades infecciosas o parasitarias, sin especificación|1H0Z
Amigdalitis aguda, sin especificación|CA03.Z
Amigdalitis estreptocócica|CA03.0
Anemia ferropénica, sin especificación|3A00.Z
Anemias u otros trastornos de los eritrocitos, sin especificación|3A9Z
Angina de pecho|BA40
Anomalías del desarrollo prenatal, sin especificación|LD9Z
Anomalías del desarrollo, sin especificación|LD9Z
Anorexia|MG43.7
Arritmia cardíaca, sin especificación|BC9Z
Artritis reumatoide,serología, sin especificación|FA20.Z
Artropatías inflamatorias, sin especificación|FA2Z
Artropatías, sin especificación|FA5Z
Asma no especificada con exacerbación|CA23.30
Asma no especificada sin complicaciones|CA23.32
Aterosclerosis de la extremidad inferior|BD40.0
Bronquiolitis aguda, sin especificación|CA41.Z
Bronquitis, sin especificación|CA20.Z
Bursitis por uso, uso excesivo o tensión|FB50.1
COVID-19, virus identificado|RA01.0
Candidiasis labial o de la mucosa bucal|1F23.0
Carcinoma in situ de sitio sin especificación|2E6Z
Cardiopatía Isquémica crónica|BA50 - BA5Z
Caries dental|DA08.0
Catarata sin especificación|9B10.Z
Causas externas de morbilidad o mortalidad, sin especificación|PL2Z
Celulitis bacteriana, erisipela o linfangitis, sin especificación|1B70.Z
Chalación, sin especificación|9A02.0Z
Ciática|ME84.3
Condición posterior a la COVID-19|RA02
Condropatías, sin especificación|FB82.Z
Conjuntivitis mucopurulenta, sin especificación|9A60.3Z
Conjuntivitis, sin especificación|9A60.Z
Contractura muscular|FB32.4
Convulsión por causas agudas, sin especificación|8A63.Z
Cuidado de la Propia Salud|VW25
Cáncer de esófago|2B70
Cáncer de páncreas|2C10
Cólico nefrítico|MF56
Deformidades de la columna vertebral|FA70
Dengue|1D20-1D2Z
Dermatitis y eccema, sin especificación|EA8Z
Dermatofitosis del pie|1F28.2
Dermatofitosis, sin especificación|1F28.Z
Dermatosis del pañal|EH40.1
Deshidratación|5C70.0
Desnutrición aguda en lactantes, niños o adolescentes|5B52
Desnutrición, sin especificación|5B7Z
Deterioro de la visión, incluida la ceguera|9nD90
Diabetes mellitus, tipo no especificado|5A14
Diarrea|ME05.
Disfonía, sin especificación|MA82.1Z
Disminución del apetito|MG43.8
Dispepsia funcional|DD90.3
Distensión o esguince muscular|FB32.5
Distensión o esquince del tobillo, sin especificación|ND14.72
Distrofia muscular|8C70
Dolor abdominal de otro tipo y de tipo no especificado|MD81.4
Dolor abdominal o pélvico|MD81
Dolor agudo, sin especificación|MG31.Z
Dolor articular|ME82
Dolor lumbar, sin especificación|ME84.2Z
Dolor muscular|FB56.2
Dolor neuropático crónico, sin especificación|MG30.5Z
Dolor torácico, no especificado|MD30.Z
Edema|MG29
Enfermedad de Chagas|1F53
Enfermedad de Parkinson|8A00.0
Enfermedad oclusiva arterial crónica, sin especificación|BD4Z
Enfermedad por el virus de Zika|1D48
Enfermedad por el virus del chikungunya|1D40
Enfermedad por reflujo gastroesofágico, sin especificación|DA22.Z
Enfermedad por virus de la inmunodeficiencia humana, sin mención de tuberculosis o malaria, sin especificación|1C62.Z
Enfermedad renal crónica|GB61
Enfermedades de la piel, sin especificación|EM0Z
Enfermedades de la sangre o de los órganos hematopoyéticos, sin especificación|3C0Z
Enfermedades del conducto anal, sin especificación|DB7Z
Enfermedades del oído o de la apófisis mastoides, sin especificación|AC0Z
Enfermedades del sistema circulatorio, sin especificación|BE2Z
Enfermedades del sistema digestivo, sin especificación|DE2Z
Enfermedades del sistema inmunitario, sin especificación|4B4Z
Enfermedades del sistema musculo esquelético o del tejido conjuntivo, sin especificación|FC0Z
Enfermedades del sistema nervioso, sin especificación|8E7Z
Enfermedades del sistema respiratorio, sin especificación|CB7Z
Enfermedades del sistema visual, sin especificación|9E1Z
Enfermedades endócrinas, sin especificación|5B3Z
Epilepsia o convulsiones, sin especificación|8A6Z
Erupción, sin especificación|ME66.6Z
Espolón calcáneo|FB54.3
Esquizofrenia|6A20
Estreñimiento|ME05.0
Examen de salud de rutina del niño|QA00.1
Examen de salud de rutina del recién nacido|QA00.2
Factores que influyen en el estado de salud o el contacto con los servicios de salud, sin especificación|QF4Z
Falta del desarrollo fisiológico normal esperado, sin especificación|MG44.1Z
Fiebre amarilla|1D47
Fiebre de otro origen o de origen desconocido|MG26
Fiebre del dengue, sin especificación|1D2Z
Foliculitis bacteriana superficial|1B74
Forúnculo|1B75.0
Fractura de región no especificada del cuerpo|ND56.2
Ganglión (quiste sinovial de tendón o articulación)|FB42.2
Gastritis, sin especificación|DA42.Z
Gastroenteritis o colitis infecciosa sin especificación del agente infeccioso|1A40.Z
Gingivoestomatitis por herpes simple|1F00.02
Hemorragia retiniana|9B78.5
Hemorroides|DB60
Hepatitis B aguda|1E50.1
Hepatitis B crónica|1E51.0
Hepatitis C aguda|1E50.2
Hepatitis C crónica|1E51.1
Herida abierta de región del cuerpo no especificada|ND56.1
Hernia umbilical|DD53
Hernias, sin especificación|DD5Z
Herpes zóster|1.00E+91
Hiperbilirrubinemia neonatal, sin especificación|KA87.Z
Hipercolesterolemia primaria|5C80.00
Hiperlipidemia mixta|5C80.2
Hipertensión esencial, sin especificación|BA00.Z
Hipertrigliceridemia|5C80.1
Hipoglucemia en el contexto de la diabetes mellitus|5A21
Hipoglucemia sin diabetes asociada|5A41
Hipotensión, sin especificación|BA2Z
Impetiginación secundaria de la piel|1B72.2
Incontinencia urinaria de esfuerzo|MF50.20
Infecciones intestinales bacterianas, sin especificación|1A0Z
Infecciones intestinales por protozoarios, sin especificación|1A3Z
Infecciones por herpes simple, sin especificación|1F00.Z
Infecciones pulmonares, sin especificación|CA4Z
Infecciones respiratorias no clasificadas en otra parte|CA45
Infección de herida postraumática, no clasificada en otra parte|NF0A.3
Infección respiratoria aguda de las vías altas, sitio no especificado|CA07.0
Infección urinaria, localización y microbio patógeno no especificados|GC08.Z
Influenza por virus no identificado|1,00E+32
Insuficiencia renal, sin especificación|GB6Z
Insuficiencia venosa periférica crónica de las extremidades inferiores, sin especificación|BD74.Z
Lesiones del hombro|FB53
Lesión de la piel de naturaleza incierta o no especificada, sin especificación|ME60.Z
Leucemia, no especificada|2B33.4
Linfedema, sin especificación|BD93.Z
Luxación, distensión o esguince de articulaciones o ligamentos a nivel del tobillo o del pie, sin especificación|ND14.Z
Luxación, distensión o esguince de parte del cuerpo no especificada|ND56.3
Maltrato físico|PJ20
Mareo y vértigo, sin especificación|MB48.Z
Mialgia|FB56.2
Migraña, sin especificación|8A80.Z
Molusco contagioso|1E+76
Mordedura de intención no determinada por un animal|PG65
Nasofaringitis aguda|CA00
Neoplasias benignas, excepto las de tejidos linfáticos o hematopoyéticos, del sistema nervioso central o de tejidos afines, sin especificación|2F5Z
Neoplasias de comportamiento desconocido, excepto los de tejidos linfáticos, hematopoyéticos, los del sistema nervioso central, o los de tejidos relacionados, sin especificación|2F9Z
Neoplasias de comportamiento incierto, excepto las de tejidos linfoide o hematopoyéticas, el sistema nervioso central o tejidos afines, sin especificación|2F7Z
Neoplasias de los tejidos hematopoyéticos o linfáticos, sin especificación|2B3Z
Neoplasias malignas de la orofaringe|2B6A
Neoplasias malignas de mama, sin especificación|2C6Z
Neoplasias malignas del ano o del conducto anal|2C00
Neumonía bacteriana, sin especificación|CA40.0Z
Nistagmo|9C84
Náusea|MD90.0
Obesidad|5B81
Onfalitis del recién nacido|KA65.1
Orzuelo|9A01.2
Osteoartritis de la rodilla, sin especificación|FA01.Z
Osteoartritis, sin especificación|FA0Z
Osteoporosis|FB83.1
Otalgia|AB70.2
Otitis externa, sin especificación|AA3Z
Otitis media, sin especificación|AB0Z
Otra hipofunción especificada u otros trastornos de la glándula hipófisis|5A61.Y
Otra otitis media supurativa crónica|AA91.2
Otras deformidades adquiridas de las extremidades|FA31
Otras infecciones bacterianas piógenas especificadas de la piel o de los tejidos subcutáneos|1B7Y
Otras neoplasias de cerebro o del sistema nervioso central, sin especificación|2A0Z
Otras quemaduras especificadas de la superficie externa del cuerpo, especificadas por sitio|ND9Y
Otro vértigo periférico|AB34.1
Otros síntomas o signos especificados que afectan al aparato digestivo o al abdomen|ME1Y
Otros síntomas o signos especificados que involucran a la piel|ME6Y
Otros síntomas o signos especificados relativos al sistema nervioso|MB6Y
Otros síntomas, signos o hallazgos clínicos especificados no clasificados en otra parte.|MH2Y
Otros trastornos especificados de la densidad y estructura óseas|FB80.Y
Otros trastornos especificados de los anexos oculares o de la órbita|9A4Y
Otros trastornos especificados del equilibrio hidroelectrolítico o ácido-básico|5C7Y
Otros trastornos especificados del segmento anterior del globo ocular|9B3Y
Otros trastornos especificados del segmento posterior del globo ocular|9C0Y
Paludismo, sin especificación|1F4Z
Parasitosis, sin especificación|1G2Z
Parálisis del nervio motor ocular|9C81
Pediculosis, sin especificación|1G00.Z
Periodontitis aguda|DA0C
Picadura o envenenamiento de intención no determinada por un animal|PG68
Pitiriasis versicolor|1F2D.0
Polimialgia reumática|FA22
Polineuropatía, sin especificación|8C0Z
Prurigo sin especificación|EC91.Z
Pólipo nasal|CA0J.Z
Quemadura solar con ampollas o exudación|EJ40.1
Queratitis infecciosa|9A71
Radiculopatía, sin especificación|8B93.Z
Recién nacido con peso bajo al nacer, sin especificación|KA21.2Z
Retinopatía de fondo y cambios vasculares retinianos|9B78.1
Rinitis alérgica, sin especificación|CA08.0Z
Rubéola|1F02
Ruptura espontánea de la membrana sinovial o del tendón|FB41
Sarampión|1F03
Sarcoma de Kaposi, localización primaria|2B57
Sarna clásica|1G04.0
Sentirse enfermo|MG25
Sinusitis aguda|CA01
Sinusitis crónica|CA0A
Síndrome Nefrótico|GB41
Síndrome del intestino irritable, sin especificación|DD91.0Z
Síndrome nefrítico|GB40
Síndrome respiratorio agudo grave|1D65
Síndrome vestibular agudo|AB30
Tapón de cerumen en el oído|AA42
Tenosinovitis|FB40
Tortícolis|FA71
Tos|MD12
Trastorno de estrés postraumático complejo|6B41
Trastorno de personalidad|6D10
Trastornos de ansiedad o relacionados con el miedo, sin especificación|6B0Z
Trastornos de cefalea, sin especificación|8A81.Z
Trastornos de insomnio, sin especificación|7A0Z
Trastornos de la refracción, sin especificación|9D00.Z
Trastornos de los tejidos blandos, sin especificación|FB6Z
Trastornos del ciclo circadiano del sueño y la vigilia, sin especificación|7A0Z
Trastornos del desarrollo del habla o del lenguaje, sin especificación|6A01.Z
Trastornos del nervio facial|8B88
Trastornos del nervio trigémino|8B82
Trastornos del sistema nervioso autónomo, sin especificación|8D8Z
Trastornos del sueño y la vigilia, sin especificación|7B2Z
Trastornos depresivos, sin especificación|6A7Z
Trastornos infecciosos del párpado|9A01
Trastornos mentales, del comportamiento o del neurodesarrollo, sin especificación|6E8Z
Trastornos metabólicos, sin especificación|5D2Z
Trastornos nutricionales, sin especificación|5C3Z
Traumatismo en región no especificada del cuerpo|ND56
Traumatismo en tendones o músculos de región no especificada del cuerpo|ND56.6
Traumatismo superficial en región no especificada del cuerpo|ND56.0
Traumatismos en el tobillo o el pie, sin especificación|ND1Z
Traumatismos en la cabeza, sin especificación|NA0Z
Traumatismos, intoxicaciones u otras consecuencias de causas externas, sin especificación|NF2Z
Tuberculosis respiratoria no confirmada|1B10.1
Tumefacción, masa o tumor intraabdominal o pélvico|MD82
Uña encarnada|EE13.1
Varicela|1.00E+90
Veneno de serpiente o hemocoagulasa por mordedura|XM6QQ2
Verrugas comunes|1.00E+80
Virosis intestinales, sin especificación|1A2Z
Viruela de los simios|1.00E+71
Vómito|MD90.1
Úlcera de piel de naturaleza incierta, especificada como del miembro inferior|ME60.2
Úlcera del pie diabético|BD54
"""

CATALOG = [tuple(line.rsplit("|", 1)) for line in _RAW.strip().splitlines()]
BY_DESC = {d: c for d, c in CATALOG}


def plain(s):
    s = unicodedata.normalize("NFD", s or "")
    return re.sub(r"[^a-z0-9 ]+", " ", "".join(ch for ch in s if unicodedata.category(ch) != "Mn").lower()).strip()


def label(desc):
    return f"{desc}  [{BY_DESC.get(desc, '')}]"


def descriptions():
    return [d for d, _c in CATALOG]


def descriptions_sorted():
    """Las descripciones de la lista de ActivityInfo en orden alfabético (sin tomar en cuenta acentos)."""
    return sorted(descriptions(), key=plain)


def from_label(text):
    """Devuelve (descripcion, codigo) a partir de lo escrito/elegido en el selector; ('', '') si no está en la lista."""
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


# Abreviaturas frecuentes del ATA → texto a buscar en la lista (solo sugerencia; la persona confirma).
SINONIMOS = {
    "malaria": "Paludismo", "tb": "Tuberculosis respiratoria", "tuberculosis": "Tuberculosis respiratoria",
    "oma": "Otitis media", "otitis media aguda": "Otitis media", "erc": "Enfermedad renal crónica",
    "vih": "Enfermedad por virus de la inmunodeficiencia humana", "sda": "Gastroenteritis o colitis infecciosa",
    "rc": "Nasofaringitis aguda", "resfriado comun": "Nasofaringitis aguda", "fab": "Amigdalitis estreptocócica",
    "fav": "Amigdalitis aguda", "faringoamigdalitis": "Amigdalitis aguda", "tina pedis": "Dermatofitosis del pie",
    "tinea pedis": "Dermatofitosis del pie", "forunculosis": "Forúnculo", "dismenorrea": "Dolor abdominal o pélvico",
    "control nino sano": "Examen de salud de rutina del niño", "nino sano": "Examen de salud de rutina del niño",
    "parasitismo intestinal": "Parasitosis", "parasitismo": "Parasitosis",
    "cervicalgia": "Afecciones asociadas con la columna vertebral", "dermatitis seborreica": "Dermatitis y eccema",
    "dermatitis atopica": "Dermatitis y eccema", "dermatitis a": "Dermatitis y eccema", "mialgias": "Mialgia",
    "hta": "Hipertensión esencial", "hipertension arterial": "Hipertensión esencial",
    "hipertension": "Hipertensión esencial", "dm": "Diabetes mellitus", "dm2": "Diabetes mellitus",
    "diabetes": "Diabetes mellitus", "itu": "Infección urinaria", "ivu": "Infección urinaria",
    "infeccion de vias urinarias": "Infección urinaria", "erge": "Enfermedad por reflujo gastroesofágico",
    "rge": "Enfermedad por reflujo gastroesofágico", "reflujo": "Enfermedad por reflujo gastroesofágico",
    "ira": "Infección respiratoria aguda de las vías altas", "iras": "Infección respiratoria aguda de las vías altas",
    "irag": "Infecciones respiratorias no clasificadas", "resfriado": "Nasofaringitis aguda",
    "gripe": "Influenza por virus no identificado", "eda": "Gastroenteritis o colitis infecciosa",
    "gastroenteritis": "Gastroenteritis o colitis infecciosa", "cefalea": "Trastornos de cefalea",
    "lumbalgia": "Dolor lumbar", "lumbago": "Dolor lumbar", "faringitis": "Amigdalitis aguda",
    "amigdalitis": "Amigdalitis aguda", "rinitis": "Rinitis alérgica", "dermatitis": "Dermatitis y eccema",
    "colon irritable": "Síndrome del intestino irritable", "sii": "Síndrome del intestino irritable",
    "anemia": "Anemia ferropénica", "gastritis": "Gastritis", "pb": "Parasitosis", "parasitosis": "Parasitosis",
    "ansiedad": "Trastornos de ansiedad", "depresion": "Trastornos depresivos", "insomnio": "Trastornos de insomnio",
    "obesidad": "Obesidad", "dislipidemia": "Hiperlipidemia mixta", "tos": "Tos", "fiebre": "Fiebre de otro origen",
    "mialgia": "Mialgia", "artralgia": "Dolor articular", "mareo": "Mareo y vértigo", "vertigo": "Mareo y vértigo",
    "conjuntivitis": "Conjuntivitis, sin especificación", "otitis": "Otitis media", "sinusitis": "Sinusitis aguda",
    "asma": "Asma no especificada sin complicaciones", "bronquitis": "Bronquitis", "neumonia": "Neumonía bacteriana",
    "varicela": "Varicela", "dengue": "Dengue", "escabiosis": "Sarna clásica", "sarna": "Sarna clásica",
    "pediculosis": "Pediculosis", "micosis": "Dermatofitosis, sin especificación", "tiña": "Dermatofitosis, sin especificación",
}


def suggest(text, limit=1):
    """Mejores coincidencias de la lista de ActivityInfo para el texto del ATA (abreviatura o diagnóstico)."""
    q = plain(text)
    if not q:
        return []
    sin = {plain(k): v for k, v in SINONIMOS.items()}
    if q in sin:
        q = plain(sin[q])
    words = [w for w in q.split() if len(w) > 2]
    corta = len(q) <= 4            # abreviaturas: «OMA», «ERC»… solo palabra completa, nunca dentro de otra palabra
    scored = []
    for d, c in CATALOG:
        p = re.sub(r"\bsin mencion de [a-z ]*", "", plain(d))   # «…sin mención de tuberculosis o malaria» no cuenta
        pal = p.split()
        if p == q:
            s = 100
        elif p.startswith(q + " ") or (not corta and p.startswith(q)):
            s = 80
        elif (q in pal) if corta else (q in p):
            s = 60
        elif words and all(w in p for w in words) and not corta:
            s = 40
        elif words and not corta and sum(w in p for w in words) * 2 >= len(words) + 1:
            s = 20
        else:
            continue
        s -= len(p) / 1000.0  # a igualdad, la descripción más corta
        scored.append((s, d, c))
    scored.sort(key=lambda x: -x[0])
    return [(d, c) for _s, d, c in scored[:limit]]
