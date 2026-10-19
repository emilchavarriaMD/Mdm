"""HEA (historia de la enfermedad actual) breve y común, armada solo con lo que trae el ATA:
sexo, edad y diagnósticos. No inventa datos del paciente (tiempo de evolución, cifras, ocupación,
antecedentes): describe el cuadro característico del diagnóstico anotado. La persona la revisa y
corrige antes de usarla."""
import unicodedata


def _plain(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


# (palabras que identifican el diagnóstico, "consulta por ...", impresión diagnóstica)
# Si el diagnóstico es crónico/previo se escribe con "con diagnóstico de ...".
_CUADROS = [
    (("hta", "hipertension"), None,
     "con diagnóstico de hipertensión arterial, que acude a consulta para valoración y control. Se requiere "
     "correlacionar con las cifras tensionales actuales y la adherencia al tratamiento antihipertensivo"),
    (("dm", "diabetes"), None,
     "con diagnóstico de diabetes mellitus, que acude a consulta para valoración y control. Se requiere "
     "correlacionar con la glucemia actual y la adherencia al tratamiento"),
    (("cefalea tension", "cefalea tensional"), "cefalea de características opresivas, asociada a tensión muscular y estrés cotidiano",
     "Cuadro clínico compatible con cefalea tensional"),
    (("cefalea",), "cefalea", "Se orienta a descartar causas secundarias según la valoración"),
    (("lumbalgia", "dolor lumbar"), "dolor en región lumbar de características mecánicas, que se exacerba con los movimientos y esfuerzos físicos",
     "Cuadro clínico sugestivo de lumbalgia mecánica"),
    (("cervicalgia", "contractura cervical"), "dolor en región cervical posterior de características mecánicas, con limitación dolorosa de los movimientos del cuello",
     "Cuadro clínico sugestivo de cervicalgia / contractura musculoesquelética cervical"),
    (("hombro", "tendinitis", "tendinopatia", "manguito"), "dolor en hombro de características mecánicas, asociado a la movilización del miembro superior",
     "Cuadro clínico sugestivo de afección musculotendinosa del hombro"),
    (("mialgia",), "dolores musculares (mialgias)", "Cuadro clínico sugestivo de mialgias, probablemente por sobrecarga muscular"),
    (("artralgia", "artrosis", "osteoartritis", "gonalgia"), "dolor articular de características mecánicas",
     "Cuadro clínico compatible con patología osteoarticular degenerativa o por sobrecarga"),
    (("faringoamigdalitis", "amigdalitis", "faringitis"), "odinofagia, dolor faríngeo y molestias a la deglución",
     "Cuadro clínico sugestivo de proceso infeccioso agudo de vías respiratorias superiores (faringoamigdalitis)"),
    (("ira", "iras", "resfriado", "rinofaringitis", "infeccion respiratoria", "irs", "gripe", "catarro"),
     "cuadro de vías respiratorias superiores, con rinorrea, congestión nasal, estornudos y tos",
     "Cuadro compatible con infección respiratoria aguda de probable etiología viral"),
    (("rinitis",), "congestión nasal, rinorrea y estornudos", "Cuadro clínico compatible con rinitis"),
    (("sinusitis",), "congestión nasal, dolor facial y secreción nasal", "Cuadro clínico sugestivo de rinosinusitis"),
    (("neumonia",), "tos y síntomas respiratorios", "Cuadro clínico sugestivo de infección respiratoria baja que requiere valoración"),
    (("asma", "bronquitis", "broncoespasmo", "sibilancias"), "tos y síntomas respiratorios con sibilancias",
     "Cuadro clínico compatible con patología obstructiva de vía aérea"),
    (("otitis",), "dolor y molestias en oído", "Cuadro clínico sugestivo de otitis"),
    (("conjuntivitis",), "enrojecimiento, picazón y secreción ocular", "Cuadro clínico compatible con conjuntivitis"),
    (("parasitosis", "parasito", "helmint", "amebiasis", "giardia", "oxiuro", "ascaris", "enteroparasit"),
     "síntomas digestivos con dolor abdominal intermitente, distensión abdominal y alteraciones del hábito intestinal",
     "Se considera probable infección por enteroparásitos; se orienta manejo antiparasitario y medidas higiénico-sanitarias para prevenir la reinfección"),
    (("eda", "diarrea", "gastroenteritis"), "evacuaciones diarreicas",
     "Cuadro compatible con enfermedad diarreica aguda; se orienta manejo sintomático y prevención de la deshidratación"),
    (("gastritis", "dispepsia", "erge", "reflujo", "enfermedad acido"), "dolor o ardor epigástrico, asociado a la ingesta de alimentos",
     "Cuadro clínico sugestivo de gastritis / dispepsia"),
    (("estrenimiento", "constipacion"), "dificultad para evacuar", "Cuadro compatible con estreñimiento"),
    (("itu", "infeccion urinaria", "infeccion de vias urinarias", "cistitis", "iuv"), "síntomas urinarios (disuria, polaquiuria y urgencia miccional)",
     "Cuadro clínico sugestivo de infección de vías urinarias"),
    (("candidiasis", "vulvovaginitis", "vaginitis"), "síntomas genitales (prurito y flujo vaginal)",
     "Cuadro clínico sugestivo de vulvovaginitis, probablemente de origen micótico"),
    (("vaginosis",), "síntomas genitales con flujo vaginal", "Cuadro clínico sugestivo de vaginosis"),
    (("its", "cervicitis", "flujo vaginal"), "síntomas genitales con flujo vaginal", "Cuadro clínico sugestivo de infección genital; requiere valoración y manejo sindrómico"),
    (("varicela",), "erupción cutánea pruriginosa con lesiones vesiculares", "Cuadro clínico compatible con varicela; se recomienda aislamiento domiciliario para prevenir la transmisión"),
    (("escabiosis", "sarna"), "prurito cutáneo intenso, de predominio nocturno, con lesiones en piel", "Cuadro clínico sugestivo de escabiosis"),
    (("tiña", "tinea", "micosis", "dermatofit"), "lesiones cutáneas pruriginosas", "Cuadro clínico sugestivo de infección micótica cutánea (tiña)"),
    (("dermatitis", "eccema", "eczema"), "eritema, prurito y resequedad cutánea localizada", "Cuadro clínico que orienta a dermatitis"),
    (("impetigo", "piodermitis", "celulitis", "absceso"), "lesiones cutáneas con signos de infección", "Cuadro clínico sugestivo de infección bacteriana de piel y tejidos blandos"),
    (("urticaria", "alergia"), "lesiones cutáneas con prurito", "Cuadro clínico compatible con reacción alérgica cutánea"),
    (("anemia",), "síntomas asociados a anemia", "Cuadro clínico sugestivo de anemia; se requiere confirmar con laboratorio"),
    (("desnutricion", "bajo peso", "malnutricion"), None, "con diagnóstico de alteración del estado nutricional, que acude para valoración y orientación nutricional"),
    (("obesidad", "sobrepeso"), None, "con diagnóstico de exceso de peso, que acude para valoración y orientación nutricional"),
    (("control prenatal", "cpn", "embarazo"), None, "que acude a control prenatal"),
    (("planificacion", "anticonce"), None, "que acude a consulta de planificación familiar"),
    (("control nino", "control de nino", "cred", "control sano", "crecimiento y desarrollo"), None, "que acude a control de crecimiento y desarrollo"),
    (("ansiedad", "estres"), "síntomas de ansiedad y estrés", "Cuadro clínico compatible con ansiedad / reacción al estrés"),
    (("depresion",), "síntomas del estado de ánimo", "Cuadro clínico compatible con trastorno depresivo; requiere valoración"),
    (("trauma", "contusion", "herida", "esguince", "lesion"), "lesión de origen traumático", "Cuadro clínico compatible con lesión traumática"),
    (("dolor abdominal",), "dolor abdominal", "Cuadro clínico de dolor abdominal que requiere valoración según los hallazgos"),
    (("rc", "revision", "control", "sano"), None, "que acude a consulta de revisión / control"),
]


def _persona(rec):
    sexo = (rec.get("sexo") or "").upper()
    sust = {"M": "Beneficiaria femenina", "H": "Beneficiario masculino"}.get(sexo, "Beneficiario/a")
    anios = (rec.get("edad_anios") or "").strip()
    meses = (rec.get("edad_meses") or "").strip()
    dias = (rec.get("edad_dias") or "").strip()
    if anios and anios != "0":
        edad = f"{anios} año" + ("s" if anios != "1" else "")
    elif meses:
        edad = f"{meses} mes" + ("es" if meses != "1" else "")
    elif dias:
        edad = f"{dias} día" + ("s" if dias != "1" else "")
    else:
        edad = ""
    return sust, edad


def _buscar(dx):
    p = _plain(dx)
    if not p:
        return None
    palabras = p.replace("/", " ").replace(",", " ").split()
    for claves, motivo, impresion in _CUADROS:
        for c in claves:
            if " " in c:
                if c in p:
                    return motivo, impresion
            elif c in palabras or (len(c) > 4 and c in p):
                return motivo, impresion
    return None


_CRONICOS = [(("hta", "hipertension"), "hipertensión arterial",
              "Se requiere correlacionar con las cifras tensionales actuales y la adherencia al tratamiento antihipertensivo"),
             (("dm", "diabetes"), "diabetes mellitus",
              "Se requiere correlacionar con la glucemia actual y la adherencia al tratamiento")]


def _cronico(dx):
    palabras = _plain(dx).replace("/", " ").replace(",", " ").split()
    for claves, nombre, nota in _CRONICOS:
        if any(c in palabras or (len(c) > 4 and c in _plain(dx)) for c in claves):
            return nombre, nota
    return None


def generate_hea(rec, descripciones=None):
    """rec: fila del ATA. descripciones: {abrev_en_minúscula: descripción} (tabla de equivalencias)."""
    descripciones = descripciones or {}
    sust, edad = _persona(rec)
    cabecera = sust + (f" de {edad}" if edad else "")
    dxs = [(rec.get(f"dx{i}") or "").strip() for i in (1, 2, 3)]
    dxs = [d for d in dxs if d]
    if not dxs:
        return f"HEA: {cabecera} que acude a consulta. El ATA no registra diagnóstico; complete el motivo de consulta."
    cronicos, otros = [], []
    for d in dxs:
        nombre = descripciones.get(d.lower()) or d
        c = _cronico(nombre) or _cronico(d)
        (cronicos if c else otros).append((nombre, c or _buscar(nombre) or _buscar(d)))
    notas = [c[1][1] for c in cronicos]
    ant = ""
    if cronicos:
        ant = " con " + ("antecedente" if otros else "diagnóstico") + " de " + " y ".join(c[1][0] for c in cronicos)
    if not otros:   # solo enfermedades crónicas: consulta de control
        return f"HEA: {cabecera}{ant}, que acude a consulta para valoración y control. " + ". ".join(notas) + "."
    nombre0, h0 = otros[0]
    if h0 is None:
        texto = (f"{cabecera}{ant}, que acude a consulta con diagnóstico de {nombre0}. Se requiere caracterizar el "
                 "tiempo de evolución, la intensidad y los factores asociados para orientar el abordaje clínico.")
    else:
        motivo, impresion = h0
        if motivo is None:
            texto = f"{cabecera}{ant} {impresion}."
        else:
            texto = f"{cabecera}{ant}, que acude a consulta por {motivo}. {impresion}."
    extra = []
    for nombre, h in otros[1:]:
        extra.append(nombre if h is None else (h[1][0].lower() + h[1][1:]))
    if extra:
        texto += " Además se identifica: " + "; ".join(extra) + "."
    if notas:
        texto += " " + ". ".join(notas) + "."
    return "HEA: " + texto.replace(" ,", ",")
