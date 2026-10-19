"""Ayudas clínicas LOCALES y deterministas (plantillas y reglas; sin IA ni internet).

Principio fundamental: el diagnóstico NO demuestra que el paciente tenga los síntomas típicos.
Por eso este módulo solo:
  * sugiere preguntas para el interrogatorio,
  * sugiere signos de alarma para la consejería (para revisión médica),
  * arma un borrador de HEA usando EXCLUSIVAMENTE lo que el personal escribió,
    señalando lo que falta como PENDIENTE.
Nunca agrega síntomas, duraciones, antecedentes ni hallazgos no documentados.
"""
import re

from services.patients import age_text
from services.validators import normalize

DRAFT_MARK = ("[BORRADOR PRELIMINAR – generado con plantilla a partir de los datos documentados; "
              "requiere revisión y confirmación del personal médico]")

GENERAL_QUESTIONS = [
    "Motivo de consulta y desde cuándo (inicio y duración).",
    "Síntomas principales y su evolución desde el inicio.",
    "Síntomas asociados y síntomas negativos pertinentes.",
    "Qué lo mejora o empeora; medicamentos o remedios ya utilizados.",
    "Antecedentes personales relevantes: enfermedades crónicas, alergias a medicamentos, "
    "medicación actual, cirugías.",
    "Antecedentes familiares pertinentes y contactos con personas enfermas.",
]

GENERAL_ALARM = [
    "Dificultad para respirar.",
    "Fiebre que no cede o persiste más de 3 días.",
    "Vómitos persistentes o imposibilidad de tomar líquidos o medicamentos.",
    "Dolor intenso que empeora, o decaimiento / somnolencia marcada.",
    "Si no mejora o empeora, acudir de inmediato al establecimiento de salud más cercano.",
]

# (id, nombre, regex sobre texto normalizado, preguntas, signos de alarma)
APS_CATEGORIES = [
    ("ira", "Infección respiratoria alta / faringoamigdalitis / rinosinusitis",
     r"\bresp\w*\s+alta|faring|amigdal|resfri|rinofar|sinusit|rinosinus|rinitis|\bgripe|catarro|laringit|\bira\b",
     ["Tiempo de evolución y secuencia de síntomas.",
      "Fiebre: cuantificada o sensación de alza térmica, desde cuándo.",
      "Odinofagia, rinorrea, congestión nasal, tos (seca o con flemas).",
      "Dificultad para respirar o para tragar.",
      "Contacto con personas con síntomas similares; automedicación."],
     ["Dificultad para respirar o respiración rápida.",
      "Labios o cara azulados / morados.",
      "Fiebre alta o que persiste más de 3 días.",
      "Dificultad para tragar con salivación excesiva, o incapacidad para tomar líquidos.",
      "Somnolencia o irritabilidad marcada (especialmente en niños)."]),
    ("respiratoria_baja", "Neumonía / bronquitis / asma / tos",
     r"neumon|bronquit|\basma|bronquial|\bepoc\b|\btos\b|bronquiolit|sibilan",
     ["Duración de la tos; si es seca o productiva y características del esputo.",
      "Fiebre, disnea, sibilancias, dolor torácico al respirar o toser.",
      "Exposición a humo de leña o tabaco; antecedente de asma o uso de inhaladores.",
      "Hemoptisis (tos con sangre); pérdida de peso; sudoración nocturna."],
     ["Dificultad para respirar, hundimiento de costillas o no poder hablar frases completas.",
      "Labios azulados.", "Fiebre alta persistente.", "Tos con sangre.",
      "Dolor torácico intenso."]),
    ("gastro", "Diarrea / gastroenteritis / parasitosis intestinal",
     r"diarrea|gastroenter|enteritis|disenter|amebia|parasit|giardi|helmint|oxiur|ascari",
     ["Inicio, número de evacuaciones al día y características (acuosas, moco, sangre).",
      "Vómitos, fiebre, dolor abdominal.",
      "Ingesta de líquidos, sed, frecuencia de orina.",
      "Fuente de agua y alimentos; contactos con síntomas similares.",
      "Si hay prurito anal o expulsión de parásitos (si aplica)."],
     ["Sangre en las heces.",
      "Signos de deshidratación: sed intensa, boca seca, orina escasa, ojos hundidos, decaimiento.",
      "Vómitos persistentes que impiden hidratarse.", "Fiebre alta.",
      "Dolor abdominal intenso o abdomen distendido.",
      "En niños: rechazo a líquidos, somnolencia o irritabilidad."]),
    ("dispepsia", "Gastritis / dispepsia / reflujo / úlcera",
     r"gastritis|dispeps|reflujo|\berge\b|ulcera|epigastr|pirosis|colon irritable|colitis",
     ["Localización, carácter y duración del dolor; relación con las comidas.",
      "Pirosis, regurgitación, náuseas o vómitos.",
      "Uso de antiinflamatorios (AINEs), alcohol, tabaco, café.",
      "Heces negras, vómito con sangre, pérdida de peso, dificultad para tragar."],
     ["Vómito con sangre o heces negras.", "Dolor abdominal intenso o persistente.",
      "Pérdida de peso sin causa aparente.", "Dificultad para tragar.",
      "Vómitos persistentes."]),
    ("urinaria", "Infección urinaria",
     r"urinaria|cistitis|pielonef|\bitu\b|\bivu\b|disuria|uretritis",
     ["Disuria, polaquiuria, urgencia miccional, hematuria.",
      "Dolor suprapúbico o lumbar; fiebre o escalofríos; náuseas/vómitos.",
      "Secreción uretral o flujo vaginal; posibilidad de embarazo.",
      "Episodios previos, diabetes, uso de sonda u otros factores."],
     ["Fiebre o escalofríos.", "Dolor lumbar intenso.", "Sangre en la orina.",
      "Vómitos que impiden tomar el tratamiento.",
      "Sin mejoría en 48–72 horas de tratamiento.", "Si hay embarazo, consultar de inmediato."]),
    ("hta", "Hipertensión arterial",
     r"hipertens|\bhta\b|presion arterial alta|presion alta",
     ["Tiempo de diagnóstico, tratamiento actual y adherencia.",
      "Cifras previas de presión arterial.",
      "Cefalea, mareo, visión borrosa, dolor torácico, disnea, palpitaciones.",
      "Consumo de sal, alcohol, tabaco; comorbilidades y antecedentes familiares."],
     ["Dolor de cabeza muy intenso o súbito.", "Dolor de pecho o falta de aire.",
      "Debilidad de cara o extremidades, dificultad para hablar.",
      "Pérdida súbita de visión o confusión.", "Desmayo."]),
    ("diabetes", "Diabetes mellitus / hiperglucemia",
     r"diabet|\bdm\s?2\b|\bdm\s?1\b|hiperglu|glucemia",
     ["Tiempo de diagnóstico, tratamiento y adherencia; glucemias previas.",
      "Poliuria, polidipsia, polifagia, pérdida de peso.",
      "Alteraciones visuales, parestesias, heridas que no cicatrizan.",
      "Alimentación, actividad física, complicaciones previas."],
     ["Sed intensa con orina excesiva y decaimiento.",
      "Confusión, somnolencia o vómitos persistentes.",
      "Sudoración fría, temblor o mareo (posible hipoglucemia).",
      "Heridas o úlceras en los pies con enrojecimiento, secreción o dolor."]),
    ("cefalea", "Cefalea / migraña",
     r"cefale|migra|jaqueca",
     ["Inicio, localización, carácter, intensidad, duración y frecuencia.",
      "Aura, náuseas/vómitos, fotofobia/fonofobia.",
      "Desencadenantes; traumatismo previo; fiebre o rigidez de nuca.",
      "Analgésicos utilizados y respuesta."],
     ["Dolor de cabeza súbito y muy intenso.", "Fiebre con rigidez de nuca.",
      "Debilidad, alteración del habla o de la visión.", "Convulsiones o pérdida de conciencia.",
      "Vómitos persistentes o cefalea tras un golpe."]),
    ("musculoesqueletico", "Dolor musculoesquelético / lumbalgia / artralgia",
     r"lumbalg|lumbar|mialg|dolor muscular|artralg|artrosis|artritis|cervicalg|tendin|contractura|"
     r"dolor articular|osteoartr|dorsalg|lumbociat|ciatic",
     ["Localización, inicio (esfuerzo, trauma), carácter e intensidad.",
      "Irradiación, parestesias o debilidad; limitación funcional; rigidez matutina.",
      "Fiebre; control de esfínteres; analgésicos usados y respuesta."],
     ["Debilidad progresiva de las piernas.", "Pérdida de control de la orina o las heces.",
      "Adormecimiento en la zona genital o glútea.", "Fiebre con dolor intenso.",
      "Dolor nocturno intenso que no cede."]),
    ("piel", "Lesiones de piel / dermatitis / micosis / escabiosis",
     r"dermatit|escabi|sarna|impetig|micosis|\btina\b|\btinea|pitiriasis|urticaria|celulitis|"
     r"absceso|herida|prurito|eccema|erisipela",
     ["Inicio, localización y evolución de las lesiones.",
      "Prurito o dolor; fiebre.",
      "Contactos con lesiones similares; exposición a plantas o productos.",
      "Tratamientos usados; alergias."],
     ["Enrojecimiento que se extiende rápidamente.", "Fiebre.", "Dolor intenso, pus o mal olor.",
      "Lesiones en ojos, boca o genitales.", "Hinchazón de cara o labios, o falta de aire."]),
    ("febril", "Síndrome febril / dengue / arbovirosis",
     r"fiebre|dengue|\bzika|chikungu|febril|malaria|paludismo",
     ["Inicio y curva de la fiebre; si fue medida.",
      "Cefalea, dolor retroocular, mialgias, artralgias, exantema.",
      "Sangrados, vómitos, dolor abdominal.",
      "Residencia o viaje a zona con transmisión; contactos con casos similares.",
      "Medicamentos utilizados para la fiebre."],
     ["Dolor abdominal intenso o continuo.", "Vómitos persistentes.",
      "Sangrado de encías, nariz, vómito o heces.", "Somnolencia, irritabilidad o confusión.",
      "Manos y pies fríos, sudoración fría o desmayo.", "Muy poca orina.",
      "Dificultad para respirar.",
      "Vigilar de forma especial cuando la fiebre baja (posible periodo crítico)."]),
    ("oido", "Otitis / dolor de oído",
     r"otitis|\boido|otalgia|otorrea",
     ["Otalgia, otorrea, hipoacusia; fiebre.",
      "Infección respiratoria previa; ingreso de agua u objetos al oído.",
      "Tiempo de evolución; uso de gotas u otros medicamentos."],
     ["Fiebre alta.", "Dolor muy intenso o inflamación detrás de la oreja.",
      "Mareo intenso o debilidad de un lado de la cara.", "Secreción con sangre."]),
    ("ojo", "Conjuntivitis / problemas oculares",
     r"conjuntiv|\bojo|ocular|pterigi|querat|orzuelo|blefarit",
     ["Ojo(s) afectado(s), inicio y evolución.",
      "Secreción, prurito, dolor, enrojecimiento, fotofobia.",
      "Alteración de la visión; trauma o cuerpo extraño; uso de lentes de contacto."],
     ["Dolor ocular intenso.", "Disminución o pérdida de la visión.",
      "Mucha sensibilidad a la luz.", "Enrojecimiento que empeora o antecedente de golpe en el ojo."]),
    ("nutricional", "Anemia / estado nutricional",
     r"anemia|desnutri|obesidad|sobrepeso|malnutri|bajo peso",
     ["Tiempo de evolución; astenia, palidez, mareo.",
      "Alimentación habitual; cambios de peso.",
      "Sangrados (menstruales, digestivos); parasitosis; embarazo o lactancia."],
     ["Falta de aire o palpitaciones.", "Desmayo o mareo intenso.",
      "Sangrado visible o heces oscuras.", "Hinchazón de pies o cara.",
      "En niños: rechazo a los alimentos o decaimiento marcado."]),
    ("abdominal", "Dolor abdominal",
     r"abdominal|colico|apendic|colecist|abdomen agudo",
     ["Localización, inicio, carácter, intensidad e irradiación.",
      "Relación con alimentos; náuseas/vómitos; fiebre.",
      "Hábito intestinal y urinario; FUM si aplica."],
     ["Dolor intenso que empeora o abdomen duro.", "Vómitos persistentes.", "Fiebre.",
      "Sangre en heces o vómito.", "No poder expulsar gases ni heces.", "Desmayo."]),
]

SSR_CATEGORIES = [
    ("emergencia", "Anticoncepción de emergencia",
     r"emergencia|poscoital|postcoital",
     ["Fecha y hora de la relación sexual sin protección o del fallo del método.",
      "FUM y día del ciclo; relaciones sin protección previas en este ciclo.",
      "Uso previo de anticoncepción de emergencia en este ciclo; vómitos tras la toma.",
      "Medicamentos actuales; método anticonceptivo habitual."],
     ["Retraso menstrual de más de 7 días: realizar prueba de embarazo.",
      "Dolor abdominal bajo intenso o sangrado anormal abundante.",
      "Vómitos dentro de las primeras 2 horas tras la toma: consultar si debe repetirse la dosis.",
      "Recordar que no protege contra ITS."]),
    ("anticoncepcion", "Planificación familiar / métodos anticonceptivos",
     r"anticonce|planificacion|\bdiu\b|implante|inyectable|pildora|esterilizacion|preservativ",
     ["Método actual o previo, tiempo de uso, satisfacción y efectos adversos.",
      "FUM, regularidad de ciclos y posibilidad de embarazo.",
      "Antecedentes ginecoobstétricos (gestas, partos, abortos, cesáreas); lactancia.",
      "Condiciones que condicionan la elección: hipertensión, migraña con aura, tabaquismo, "
      "antecedente de trombosis, sangrado vaginal sin explicar, cáncer de mama.",
      "Medicación actual y deseo reproductivo."],
     ["Dolor abdominal intenso.", "Dolor de pecho o falta de aire.",
      "Dolor de cabeza intenso o nuevo, o alteraciones de la visión.",
      "Dolor intenso o hinchazón en una pierna.",
      "Sangrado abundante o prolongado; retraso menstrual (posible embarazo).",
      "Enrojecimiento, pus o dolor en el sitio de inyección o implante."]),
    ("its_flujo", "ITS / flujo vaginal / prurito genital",
     r"\bits\b|transmision sexual|flujo|prurito genital|vaginit|vaginosis|cervicit|candidiasis|"
     r"tricomon|sifilis|gonorrea|clamidia|herpes|\bvph\b|verruga|uretritis|vulvovag",
     ["Características del flujo (color, olor, cantidad); prurito, irritación, ardor.",
      "Úlceras o lesiones genitales; dolor pélvico o dispareunia; sangrado postcoital.",
      "Disuria; fiebre.",
      "Inicio y evolución; tratamientos o duchas vaginales previas.",
      "Pareja(s) con síntomas; relaciones sin protección; ITS previas.",
      "FUM y posibilidad de embarazo."],
     ["Dolor pélvico o abdominal bajo intenso.", "Fiebre o escalofríos.",
      "Sangrado vaginal anormal.", "Úlceras o lesiones nuevas.",
      "Síntomas que persisten tras el tratamiento.",
      "Su(s) pareja(s) sexual(es) deben recibir evaluación y tratamiento cuando corresponda."]),
    ("urinaria", "Infección urinaria",
     r"urinaria|cistitis|pielonef|\bitu\b|\bivu\b|disuria",
     ["Disuria, polaquiuria, urgencia, hematuria.",
      "Dolor suprapúbico o lumbar; fiebre; náuseas/vómitos.",
      "Flujo vaginal asociado; FUM y posibilidad de embarazo; episodios previos."],
     ["Fiebre o escalofríos.", "Dolor lumbar intenso.", "Sangre en la orina.",
      "Vómitos que impiden tomar el tratamiento.", "Sin mejoría en 48–72 horas."]),
    ("menstrual", "Alteración menstrual",
     r"menstru|amenorrea|dismenorrea|sangrado uterino|metrorragia|menorragia|oligomenorrea|"
     r"polimenorrea",
     ["FUM; duración, regularidad y cantidad del sangrado.",
      "Sangrado intermenstrual o postcoital; dismenorrea.",
      "Método anticonceptivo; posibilidad de embarazo.",
      "Cambios de peso, estrés, síntomas tiroideos o de hiperandrogenismo."],
     ["Sangrado muy abundante (empapar una toalla cada hora).", "Mareo o desmayo.",
      "Dolor pélvico intenso.", "Retraso menstrual con dolor (descartar embarazo).",
      "Sangrado después de la menopausia."]),
    ("pelvico", "Dolor pélvico",
     r"pelvic",
     ["Localización, inicio, carácter e intensidad; relación con el ciclo.",
      "Flujo vaginal, fiebre, síntomas urinarios o intestinales, dispareunia.",
      "FUM y posibilidad de embarazo; antecedente de ITS; uso de DIU."],
     ["Dolor intenso o de inicio súbito.", "Fiebre.", "Desmayo o mareo intenso.",
      "Sangrado vaginal con dolor.", "Retraso menstrual con dolor (urgencia)."]),
]

GENERAL_SSR_QUESTIONS = [
    "Motivo de consulta, inicio y evolución.",
    "FUM, ciclo menstrual y posibilidad de embarazo.",
    "Antecedentes ginecoobstétricos pertinentes.",
    "Uso actual de anticonceptivos y fecha de la última dosis (si aplica).",
    "Antecedentes de ITS y datos relevantes para la consulta.",
]


def _matches(categories, text):
    norm = normalize(text)
    return [c for c in categories if re.search(c[2], norm)]


def suggest_questions(kind, dx_text="", extra_text=""):
    """Devuelve (título, [preguntas sugeridas]). Son sugerencias, no datos del paciente."""
    cats = _matches(APS_CATEGORIES if kind == "aps" else SSR_CATEGORIES, f"{dx_text} {extra_text}")[:3]
    base = GENERAL_QUESTIONS if kind == "aps" else GENERAL_SSR_QUESTIONS
    if not cats:
        return "Preguntas generales de interrogatorio", list(base)
    title = " + ".join(c[1] for c in cats)
    questions = []
    for c in cats:
        questions += [q for q in c[3] if q not in questions]
    return title, questions + ["Antecedentes personales relevantes, alergias y medicación actual."]


def suggest_alarm_signs(kind, dx_text="", extra_text=""):
    cats = _matches(APS_CATEGORIES if kind == "aps" else SSR_CATEGORIES, f"{dx_text} {extra_text}")[:3]
    if not cats:
        return list(GENERAL_ALARM)
    signs = []
    for c in cats:
        signs += [s for s in c[4] if s not in signs]
    signs.append("Si no mejora o empeora, acudir de inmediato al establecimiento de salud más cercano.")
    return signs


# ---------------------------------------------------------------------------
# Borradores de HEA (solo con datos documentados)
# ---------------------------------------------------------------------------

APS_HEA_FIELDS = [
    ("hea_motivo", "Motivo de consulta", True),
    ("hea_inicio", "Inicio y duración del cuadro", True),
    ("hea_sintomas", "Síntomas principales", True),
    ("hea_evolucion", "Evolución", True),
    ("hea_asociados", "Síntomas asociados", True),
    ("hea_factores", "Factores agravantes o atenuantes", True),
    ("hea_antecedentes", "Antecedentes relevantes", True),
    ("hea_negativos", "Síntomas negativos pertinentes", True),
    ("hea_otros", "Otros datos referidos por el paciente", False),
]

SSR_HEA_FIELDS = [
    ("hea_inicio", "Inicio y evolución"),
    ("hea_urinarios", "Síntomas urinarios"),
    ("hea_flujo", "Características del flujo vaginal"),
    ("hea_olor_prurito", "Olor, prurito o irritación"),
    ("hea_dolor", "Dolor pélvico o genital"),
    ("fum", "Fecha de última menstruación (FUM)"),
    ("hea_ciclo", "Características del ciclo menstrual"),
    ("hea_antec_go", "Antecedentes ginecoobstétricos"),
    ("hea_anticonceptivo_actual", "Uso actual de anticonceptivos"),
    ("hea_fecha_ultima_dosis", "Fecha de la última dosis anticonceptiva"),
    ("hea_riesgo_embarazo", "Riesgo de embarazo y pruebas realizadas"),
    ("hea_antec_its", "Antecedentes de ITS y datos relevantes"),
    ("hea_otros", "Otros síntomas y antecedentes"),
]

_SSR_RELEVANT = {
    "emergencia": {"hea_inicio", "fum", "hea_ciclo", "hea_riesgo_embarazo", "hea_anticonceptivo_actual"},
    "anticoncepcion": {"fum", "hea_ciclo", "hea_antec_go", "hea_anticonceptivo_actual",
                       "hea_fecha_ultima_dosis", "hea_riesgo_embarazo"},
    "its_flujo": {"hea_inicio", "hea_flujo", "hea_olor_prurito", "hea_dolor", "fum",
                  "hea_riesgo_embarazo", "hea_antec_its"},
    "urinaria": {"hea_inicio", "hea_urinarios", "fum", "hea_riesgo_embarazo"},
    "menstrual": {"hea_inicio", "fum", "hea_ciclo", "hea_antec_go", "hea_anticonceptivo_actual",
                  "hea_riesgo_embarazo"},
    "pelvico": {"hea_inicio", "hea_dolor", "fum", "hea_riesgo_embarazo", "hea_antec_its"},
}


def _intro(patient, dx):
    parts = []
    sexo = (patient.get("sexo") or "").lower()
    edad = age_text(patient)
    if sexo or edad:
        s = "Paciente"
        if sexo:
            s += f" de sexo {sexo}"
        if edad:
            s += f", de {edad} de edad"
        parts.append(s + ".")
    if dx:
        parts.append(f"Diagnóstico registrado en esta atención: {dx}.")
    return " ".join(parts)


def _clean(text):
    return (text or "").strip()


def build_hea_aps(patient, fields, dx_principal=""):
    """Devuelve (texto_borrador, lista_de_datos_pendientes). Usa solo lo que está escrito."""
    lines = [DRAFT_MARK, _intro(patient, _clean(dx_principal))]
    pending, filled = [], 0
    for key, label, core in APS_HEA_FIELDS:
        value = _clean(fields.get(key))
        if value:
            filled += 1
            lines.append(f"{label}: {value}")
        elif core:
            pending.append(label)
    if filled == 0:
        lines.append("No se dispone de información documentada sobre el cuadro clínico. "
                     "Solo se cuenta con el diagnóstico registrado; los datos del interrogatorio "
                     "están PENDIENTES de completar.")
    elif pending:
        lines.append("Datos pendientes de documentar: " + "; ".join(pending) + ".")
    return "\n".join(l for l in lines if l), pending


def build_hea_ssr(patient, fields, motivo="", categoria="", dx_principal=""):
    from services.validators import fmt_date
    lines = [DRAFT_MARK, _intro(patient, _clean(dx_principal))]
    if _clean(categoria):
        lines.append(f"Categoría de atención: {_clean(categoria)}.")
    if _clean(motivo):
        lines.append(f"Motivo de consulta: {_clean(motivo)}")
    cats = _matches(SSR_CATEGORIES, f"{categoria} {motivo} {dx_principal}")
    relevant = set()
    for c in cats:
        relevant |= _SSR_RELEVANT.get(c[0], set())
    if not relevant:
        relevant = {"hea_inicio", "fum", "hea_antec_go", "hea_anticonceptivo_actual"}
    pending, filled = [], 0
    if not _clean(motivo):
        pending.append("Motivo de consulta")
    for key, label in SSR_HEA_FIELDS:
        value = _clean(fields.get(key))
        if key in ("fum", "hea_fecha_ultima_dosis") and value:
            value = fmt_date(value) if "-" in value and len(value) == 10 else value
        if value:
            filled += 1
            lines.append(f"{label}: {value}")
        elif key in relevant:
            pending.append(label)
    if filled == 0 and not _clean(motivo):
        lines.append("No se dispone de información documentada del interrogatorio; los datos están "
                     "PENDIENTES de completar.")
    elif pending:
        lines.append("Datos pendientes de documentar: " + "; ".join(pending) + ".")
    return "\n".join(l for l in lines if l), pending
