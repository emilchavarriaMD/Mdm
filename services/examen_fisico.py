"""Examen físico céfalo-caudal normal, con los hallazgos positivos que corresponden a los diagnósticos elegidos.

Cada sección tiene partes con su texto normal; un diagnóstico cambia las partes que le corresponden (RULES: expresión
sobre el nombre del diagnóstico de ActivityInfo → partes con hallazgos). Si dos diagnósticos tocan la misma parte, se
unen. El abdomen siempre dice que no se explora por falta de espacio clínico adecuado. El genitourinario va en el examen
de SSR y, en APS, solo si algún diagnóstico tiene hallazgos genitourinarios.
"""
import re

from services import cie11_catalog as cat

SECCIONES = [
    ("General", [("general", "paciente consciente, orientada/o, hidratada/o, afebril y en aceptable estado general")]),
    ("Cabeza", [("cabeza", "normocéfala, sin masas ni lesiones")]),
    ("ORL", [("ojos", "ojos con pupilas isocóricas normorreactivas, conjuntivas rosadas y escleras anictéricas"),
             ("oidos", "oídos con conductos auditivos permeables y membranas timpánicas íntegras"),
             ("nariz", "nariz con fosas permeables, mucosa rosada y sin secreción"),
             ("orofaringe", "orofaringe sin hiperemia ni exudado, amígdalas sin hipertrofia")]),
    ("Cuello", [("cuello", "simétrico, móvil, sin adenopatías ni masas, tiroides no palpable, sin ingurgitación yugular")]),
    ("Tórax", [("torax", "simétrico, con buena expansibilidad y sin tiraje"), ("mamas", "")]),
    ("Corazón", [("corazon", "ruidos cardíacos rítmicos, de buena intensidad, sin soplos")]),
    ("Pulmones", [("pulmones", "murmullo vesicular conservado en ambos campos, sin ruidos agregados")]),
    ("Abdomen", [("abdomen", "no se explora de forma adecuada por falta de espacio clínico apropiado")]),
    ("Extremidades", [("extremidades", "simétricas, sin edema ni deformidades, con movilidad y fuerza conservadas, "
                                       "llenado capilar menor de 2 segundos"), ("piel", "")]),
    ("Genitourinario", [("genital", "genitales externos sin alteraciones evidentes"),
                        ("lumbar", "puño percusión lumbar negativa")]),
]
GU = ("genital", "lumbar")

FIEBRE = {"general": "paciente en aceptable estado general, febril, con malestar general"}
RESP_ALTA = {"nariz": "nariz con mucosa hiperémica y edematosa, con rinorrea", "orofaringe": "orofaringe con hiperemia leve"}

# (patrón sobre el nombre sin acentos, hallazgos)
RULES = [
    # --- piel y partes blandas
    (r"absceso piogeno|forunculo|otras infecciones bacterianas piogenas|foliculitis", {"piel": "lesión nodular o pustulosa eritematosa, caliente, indurada y dolorosa a la palpación, con halo de eritema y, en ocasiones, fluctuación y drenaje purulento"}),
    (r"celulitis|erisipela", {"general": "paciente en aceptable estado general, con fiebre baja", "piel": "placa eritematosa, caliente, edematosa y dolorosa, de bordes mal definidos, con aumento de volumen del segmento afectado; adenopatías regionales dolorosas"}),
    (r"impetig", {"piel": "lesiones erosivas con costras melicéricas (color miel) sobre base eritematosa"}),
    (r"herida abierta|infeccion de herida", {"piel": "herida con bordes irregulares, eritema perilesional, edema y secreción serosa o purulenta"}),
    (r"traumatismo superficial|excoriacion", {"piel": "excoriaciones y abrasiones superficiales con eritema y costras hemáticas"}),
    (r"quemadura solar", {"piel": "eritema intenso con ampollas y descamación en áreas expuestas, dolorosas al tacto"}),
    (r"otras quemaduras", {"piel": "quemadura de espesor parcial con eritema, flictenas y dolor intenso"}),
    (r"dermatitis y eccema|dermatitis seborreica|prurigo|erupcion|afecciones alergicas|enfermedades de la piel|prurito|lesiones de la piel|otros sintomas o signos especificados que involucran a la piel", {"piel": "lesiones eritematosas, pruriginosas y descamativas, con excoriaciones por rascado"}),
    (r"dermatofitosis del pie", {"piel": "descamación, maceración y fisuras en espacios interdigitales de los pies, con eritema"}),
    (r"dermatofitosis", {"piel": "lesiones anulares eritematosas con borde elevado y descamativo, centro más claro"}),
    (r"pitiriasis", {"piel": "máculas hipopigmentadas con descamación fina en tronco y cuello"}),
    (r"onicomicosis", {"piel": "uñas engrosadas, amarillentas, quebradizas, con onicólisis"}),
    (r"onicocriptosis", {"piel": "borde ungueal del dedo gordo del pie con eritema, edema, dolor y tejido de granulación"}),
    (r"sarna|escabiasis", {"piel": "pápulas excoriadas y trayectos lineales en espacios interdigitales y muñecas, con costras por rascado"}),
    (r"pediculosis", {"cabeza": "liendres y pediculos visibles en cuero cabelludo, con excoriaciones y costras en región occipital"}),
    (r"molusco", {"piel": "pápulas pequeñas, color piel, perladas, con umbilicación central"}),
    (r"verrugas comunes", {"piel": "pápulas hiperqueratósicas, rugosas e indoloras en dorso de manos y dedos"}),
    (r"herpes simple, sin esp|infecciones por herpes simple", {"cabeza": "vesículas agrupadas sobre base eritematosa en labio, con costras"}),
    (r"herpes zoster", {"torax": "vesículas agrupadas sobre base eritematosa con distribución unilateral en dermatoma, con costras y dolor a la palpación"}),
    (r"varicela", {"piel": "lesiones vesiculares en distintas etapas (máculas, pápulas, vesículas y costras) en cara, tronco y extremidades"}),
    (r"sarampion|rubeola|zika|chikungunya", {"general": "paciente en aceptable estado general, con fiebre", "piel": "exantema maculopapular eritematoso"}),
    (r"viruela de los simios", {"general": "paciente con fiebre y adenopatías", "piel": "lesiones vesiculopustulosas umbilicadas en distintas etapas"}),
    (r"dermatosis del panal", {"piel": "eritema con erosiones en región del pañal, con pápulas satélite"}),
    (r"ulcera de piel|ulcera del pie diabetico", {"extremidades": "úlcera con bordes irregulares, fondo con tejido de granulación o fibrina, secreción y eritema perilesional; pulsos distales disminuidos", "piel": ""}),
    (r"mordedura", {"piel": "herida punzante o desgarro por mordedura con eritema, edema y dolor local"}),
    (r"picadura|alacran", {"piel": "área de picadura con eritema, edema y dolor local, parestesias en la zona"}),
    (r"serpiente", {"general": "paciente ansiosa/o, con dolor", "piel": "dos orificios punzantes con edema progresivo, equimosis y dolor intenso en el miembro afectado"}),
    (r"lesion de la piel de naturaleza incierta|neoplasias benignas, excepto|neoplasias de comportamiento", {"piel": "lesión nodular o elevada, bien delimitada, de crecimiento lento, móvil y no dolorosa"}),
    # --- ojos
    (r"conjuntivitis", {"ojos": "conjuntiva hiperémica, con secreción mucopurulenta o serosa y edema palpebral; agudeza visual conservada"}),
    (r"chalaz|chalac", {"ojos": "nódulo firme e indoloro en el párpado, sin eritema marcado"}),
    (r"orzuelo|trastornos infecciosos del parpado", {"ojos": "párpado eritematoso, edematoso y doloroso, con nódulo con punto purulento en el borde"}),
    (r"anexos oculares", {"ojos": "borde palpebral eritematoso con escamas y costras"}),
    (r"segmento anterior|queratitis", {"ojos": "inyección conjuntival periquerática, fotofobia y lagrimeo; agudeza visual disminuida"}),
    (r"segmento posterior|hemorragia retiniana|retinopatia", {"ojos": "agudeza visual disminuida; fondo de ojo con alteraciones retinianas"}),
    (r"catarata", {"ojos": "opacidad del cristalino con disminución de la agudeza visual y reflejo pupilar conservado"}),
    (r"refraccion|deterioro de la vision|enfermedades del sistema visual", {"ojos": "agudeza visual disminuida, pupilas isocóricas normorreactivas, conjuntivas rosadas"}),
    (r"nistagmo|paralisis del nervio motor ocular", {"ojos": "movimientos oculares alterados con limitación de la motilidad extrínseca y diplopía"}),
    # --- oídos
    (r"cerumen", {"oidos": "conducto auditivo externo ocluido por tapón de cerumen, membrana timpánica no visualizable"}),
    (r"otitis externa", {"oidos": "conducto auditivo externo eritematoso, edematoso y doloroso a la tracción del pabellón, con secreción"}),
    (r"otitis media, sin|otalgia|otitis media cronica|otra otitis", {"oidos": "membrana timpánica eritematosa, abombada y opaca, con disminución de la movilidad; otorrea si hay perforación"}),
    (r"cuerpo extrano en oido", {"oidos": "cuerpo extraño visible en conducto auditivo externo con eritema local"}),
    (r"enfermedades del oido", {"oidos": "conducto auditivo con eritema leve y membrana timpánica con alteraciones"}),
    (r"vertigo|sindrome vestibular", {"oidos": "oídos sin alteraciones; nistagmo horizontal-rotatorio, prueba de Dix-Hallpike positiva y marcha inestable"}),
    (r"mareo", {"general": "paciente con mareo, sin déficit neurológico focal"}),
    # --- nariz / garganta
    (r"nasofaringitis|infeccion respiratoria aguda de las vias altas|infecciones respiratorias no clasificadas|rinitis|sinusitis aguda|coriza", RESP_ALTA),
    (r"rinitis alergica", {"nariz": "mucosa nasal pálida y edematosa, con rinorrea hialina y cornetes hipertróficos"}),
    (r"sinusitis", {"nariz": "mucosa hiperémica con secreción mucopurulenta, dolor a la palpación de senos maxilares y frontales"}),
    (r"polipo nasal", {"nariz": "masa pálida, brillante y móvil que obstruye la fosa nasal"}),
    (r"amigdalitis|faringitis", {"orofaringe": "faringe hiperémica con amígdalas hipertróficas, eritematosas y con exudado blanquecino", "cuello": "adenopatías cervicales anteriores dolorosas"}),
    (r"estreptococ", {"orofaringe": "faringe muy hiperémica, amígdalas hipertróficas con exudado purulento y petequias en paladar"}),
    (r"disfonia", {"orofaringe": "faringe levemente hiperémica; voz ronca"}),
    (r"aftas|aftoides|gingivoestomatitis|candidiasis labial", {"orofaringe": "úlceras redondeadas con halo eritematoso y fondo blanquecino en mucosa oral, dolorosas"}),
    (r"candidiasis labial|candidiasis de la mucosa", {"orofaringe": "placas blanquecinas removibles en lengua y mucosa oral"}),
    (r"caries|periapical|periodontitis|gingiv|odontalgia", {"orofaringe": "caries con destrucción coronaria, dolor a la percusión de la pieza, encía eritematosa y edematosa, con o sin fístula o drenaje purulento"}),
    (r"herpes labial", {}),
    # --- cuello / ganglios
    (r"cervicalgia|tortic|radiculopatia", {"cuello": "contractura de la musculatura paravertebral cervical y trapecio, dolor a la palpación y limitación para los movimientos de rotación y flexión"}),
    (r"tiroid|hipotiroidismo", {"cuello": "tiroides palpable o no, sin nódulos; sin adenopatías"}),
    (r"leucemia|linfoma|hematopoyeticos o linfaticos", {"general": "paciente con palidez cutáneo-mucosa", "cuello": "adenopatías cervicales múltiples, móviles, de consistencia elástica", "pulmones": ""}),
    # --- tórax / pulmones / corazón
    (r"bronquitis", {"pulmones": "murmullo vesicular conservado con roncus y estertores bronquiales dispersos, sin tiraje"}),
    (r"asma", {"pulmones": "sibilancias espiratorias difusas, espiración prolongada", "torax": "simétrico, con uso leve de músculos accesorios si hay crisis"}),
    (r"bronquiolitis", {"pulmones": "sibilancias y crepitantes finos difusos con espiración prolongada", "torax": "tiraje subcostal e intercostal, aleteo nasal"}),
    (r"neumonia|infecciones pulmonares|tuberculosis respiratoria", {"general": "paciente febril, con polipnea y aspecto de enfermedad", "pulmones": "disminución del murmullo vesicular con estertores crepitantes localizados y aumento de las vibraciones vocales en el área afectada"}),
    (r"covid|influenza|sindrome respiratorio agudo grave", {"general": "paciente febril, con malestar general, astenia y tos", "pulmones": "murmullo vesicular conservado, con estertores finos escasos o sin ruidos agregados; saturación de oxígeno a valorar"}),
    (r"tos$|^tos\b|condicion posterior a la covid", {"pulmones": "murmullo vesicular conservado, sin ruidos agregados"}),
    (r"enfermedades del sistema respiratorio", {"pulmones": "ruidos respiratorios con roncus escasos"}),
    (r"angina|cardiopatia isquemica|dolor toracico", {"corazon": "ruidos cardíacos rítmicos, sin soplos; frecuencia cardíaca normal", "torax": "sin dolor a la palpación de la pared torácica"}),
    (r"arritmia|palpitaciones", {"corazon": "ruidos cardíacos arrítmicos o taquicárdicos, sin soplos"}),
    (r"enfermedad de chagas|sistema circulatorio", {"corazon": "ruidos cardíacos rítmicos, con posible desdoblamiento o soplo sistólico suave", "extremidades": "edema leve de miembros inferiores"}),
    (r"hipertension esencial|hipertension gestacional|preeclam|edema, proteinuria", {"general": "paciente en aceptable estado general, con cifras de presión arterial elevadas", "corazon": "ruidos cardíacos rítmicos, sin soplos; sin ingurgitación yugular"}),
    (r"insuficiencia venosa|linfedema|edema$|^edema\b|edema gestacional", {"extremidades": "edema de miembros inferiores con fóvea, várices visibles, hiperpigmentación y cambios tróficos de la piel"}),
    (r"aterosclerosis|arterial oclusiva|oclusiva arterial", {"extremidades": "pulsos distales disminuidos o ausentes, piel fría, pálida y con disminución del vello; llenado capilar prolongado"}),
    # --- extremidades / osteomuscular
    (r"osteoartritis|artropatia|artritis|dolor articular|gonartrosis|osteoartritis de la rodilla", {"extremidades": "dolor a la palpación y a la movilización articular, crepitación, limitación del rango de movimiento y leve edema articular"}),
    (r"artritis reumatoide|poliartralgias|polimialgia", {"extremidades": "edema, calor y dolor en articulaciones pequeñas de manos y muñecas con rigidez, simétricos; limitación para el cierre del puño"}),
    (r"esguince|luxacion|distension|tobillo|ligament", {"extremidades": "edema y equimosis en la articulación afectada, dolor a la palpación y a la movilización, con limitación del apoyo"}),
    (r"fractura", {"extremidades": "deformidad, edema, equimosis y dolor intenso a la palpación del foco, con impotencia funcional; pulsos y sensibilidad distal conservados"}),
    (r"contractura|mialgia|dolor muscular|traumatismo en tendones|ruptura espontanea|musculo", {"extremidades": "dolor a la palpación y contractura muscular en el grupo afectado, con limitación para el estiramiento; sin déficit de fuerza"}),
    (r"lumbar|ciatica|columna|dorsal|glutea|tejidos blandos", {"extremidades": "dolor a la palpación de la musculatura paravertebral lumbar, con contractura y limitación a la flexión; Lasègue positivo si hay irradiación, fuerza y sensibilidad conservadas"}),
    (r"bursitis|hombro|tenosinovitis|ganglion|rotula|condropatias|patela|espolon|talon", {"extremidades": "dolor a la palpación y a los movimientos de la zona afectada, con limitación funcional leve y sin eritema ni calor marcados"}),
    (r"otras deformidades adquiridas", {"extremidades": "desviación del primer dedo del pie con prominencia ósea medial, dolorosa, con eritema y callosidad"}),
    (r"traumatismos? en|contusion|traumatismo en region no", {"extremidades": "edema, equimosis y dolor a la palpación en la zona del trauma, con movilidad conservada"}),
    (r"traumatismos en la cabeza", {"cabeza": "hematoma o aumento de volumen en región traumatizada, sin heridas penetrantes", "general": "paciente consciente, orientada/o, Glasgow 15 puntos"}),
    (r"distrofia muscular", {"extremidades": "disminución de la fuerza proximal, marcha anserina y atrofia muscular"}),
    (r"osteoporosis|densidad y estructura osea", {"extremidades": "dolor a la palpación de columna, cifosis dorsal leve y disminución de la talla"}),
    # --- neurológico
    (r"cefalea|migrana", {"cabeza": "sin lesiones; dolor a la palpación de musculatura pericraneal y temporal, sin signos meníngeos", "cuello": "contractura de la musculatura cervical posterior"}),
    (r"epilepsia|convulsion", {"general": "paciente somnolienta/o o en periodo postcrítico, sin déficit neurológico focal"}),
    (r"parkinson", {"extremidades": "temblor de reposo, rigidez en rueda dentada y bradicinesia; marcha con pasos cortos"}),
    (r"polineuropatia|dolor neuropatico|nervioso", {"extremidades": "disminución de la sensibilidad en guante y calcetín, con reflejos osteotendinosos disminuidos"}),
    (r"nervio facial", {"cabeza": "asimetría facial con desviación de la comisura labial, borramiento del surco nasolabial e imposibilidad para cerrar el ojo del lado afectado"}),
    (r"trigemino", {"cabeza": "dolor desencadenado por la palpación de puntos gatillo en la distribución del trigémino"}),
    (r"autonomo|hipotension", {"general": "paciente con tendencia a la hipotensión ortostática"}),
    (r"insomnio|trastornos del sueno|ciclo circadiano", {"general": "paciente con facies de cansancio, ojeras y somnolencia diurna"}),
    (r"ansiedad|estres postraumatico", {"general": "paciente ansiosa/o, inquieta/o, con taquicardia leve y sudoración palmar"}),
    (r"depresivos", {"general": "paciente con afecto aplanado, hipoprosexia y enlentecimiento psicomotor"}),
    (r"esquizofrenia|trastornos mentales|personalidad|comportamiento", {"general": "paciente con alteración del comportamiento y del juicio, colaboradora/o de forma parcial"}),
    (r"maltrato fisico", {"general": "paciente ansiosa/o, con ánimo decaído", "piel": "equimosis y hematomas en distintas etapas de evolución, con dolor a la palpación"}),
    (r"maltrato sexual", {"general": "paciente ansiosa/o, llorosa/o, con temor; se brinda espacio privado y confidencial", "genital": "se valora únicamente con su consentimiento"}),
    # --- generales / sistémicos
    (r"fiebre|fiebre amarilla|enfermedades infecciosas o parasitarias|sentirse enfermo", FIEBRE),
    (r"dengue", {"general": "paciente febril, con malestar general, dolor retroocular y mialgias", "piel": "eritema facial y exantema; prueba del torniquete a valorar"}),
    (r"paludismo", {"general": "paciente febril, con escalofríos, palidez y esplenomegalia a valorar"}),
    (r"deshidratacion", {"general": "paciente con mucosas secas, turgencia de la piel disminuida, llenado capilar prolongado y ojos hundidos"}),
    (r"desnutricion|anorexia|falta del desarrollo|trastornos nutricionales|nutricion", {"general": "paciente con bajo peso, disminución del tejido celular subcutáneo y masa muscular, y palidez"}),
    (r"anemia|anemias|sangre|hematopoy", {"general": "paciente con palidez de piel y mucosas, taquicárdica leve", "ojos": "conjuntivas pálidas"}),
    (r"obesidad", {"general": "paciente con obesidad, IMC elevado, acantosis nigricans a valorar"}),
    (r"diabetes", {"extremidades": "sensibilidad conservada o disminuida en monofilamento, pulsos distales presentes, sin úlceras"}),
    (r"hipoglucemia", {"general": "paciente sudorosa/o, con temblor y palidez"}),
    (r"hiperbilirrubinemia|hepatitis|ictericia", {"general": "paciente con tinte ictérico en piel", "ojos": "escleras ictéricas"}),
    (r"enfermedad renal|insuficiencia renal|nefritico|nefrotico", {"general": "paciente con palidez y edema palpebral", "extremidades": "edema de miembros inferiores con fóvea"}),
    (r"vih|inmunodeficiencia", {"general": "paciente en aceptable estado general, con pérdida de peso a valorar", "orofaringe": "mucosa oral sin candidiasis"}),
    (r"kaposi", {"piel": "máculas y nódulos violáceos en piel y mucosas"}),
    (r"neoplasias malignas de la orofaringe", {"orofaringe": "lesión ulcerada o exofítica en orofaringe", "cuello": "adenopatías cervicales duras y fijas"}),
    (r"cancer|neoplasias malignas|carcinoma|neoplasias de los tejidos|otras neoplasias de cerebro", {"general": "paciente en regular estado general, con pérdida de peso y palidez"}),
    (r"hiperplasia de la prostata|prostatocistitis", {"genital": "tacto rectal con próstata aumentada de tamaño, de consistencia elástica y con o sin dolor, sin nódulos duros", "lumbar": "puño percusión lumbar negativa"}),
    (r"hipercolesterol|hiperlipidemia|hipertrigliceridemia", {"general": "paciente con sobrepeso; sin xantomas ni xantelasmas"}),
    (r"cuidado de la propia salud|factores que influyen|examen de salud|control de salud", {"general": "paciente en buen estado general, con peso y talla acordes"}),
    (r"examen de salud de rutina del nino|crecimiento", {"general": "paciente en buen estado general, activo, con peso y talla acordes para la edad"}),
    (r"recien nacido|neonatal|periodo perinatal|peso bajo al nacer|onfalitis", {"general": "recién nacido en regular estado general, con peso bajo y llanto débil, ictericia en cara y tronco si procede"}),
    (r"onfalitis", {"general": "recién nacido activo, reactivo", "torax": "simétrico", "abdomen": "", "piel": "ombligo con eritema periumbilical, secreción purulenta y mal olor"}),
    (r"hernia", {"extremidades": "", "genital": "masa reductible en región inguinal que aumenta con la maniobra de Valsalva, sin signos de estrangulamiento"}),
    (r"hernia umbilical", {"genital": ""}),
    (r"hemorroides|conducto anal", {"genital": "región anal con hemorroides externas o prolapsadas, fisura o plexos hemorroidales dolorosos; tacto rectal con sangre en el dedo de guante"}),
    (r"ano o del conducto anal", {"genital": "lesión en región anal, de bordes irregulares, dolorosa"}),
    (r"intestinal|gastroenteritis|diarrea|virosis intestinal|parasitosis|colitis", {"general": "paciente con mucosas levemente secas"}),
    (r"insuficiencia|piel y mucosas", {}),
    (r"hipoacusia", {"oidos": "hipoacusia"}),
    (r"gastritis|dispepsia|reflujo|digestivo|estrenimiento|colon irritable|intestino irritable|nausea|vomito", {}),
    (r"mastodinia|trastornos de la mama|trastornos inflamatorios de la mama|mastitis|tumor o masa en el seno|neoplasia benigna de la mama|galactorrea|neoplasias malignas de mama", {}),
]
# hallazgos genitourinarios y mamarios (ginecológicos), separados para claridad
RULES += [
    (r"candidiasis vulvovaginal", {"genital": "vulva eritematosa y edematosa con fisuras; leucorrea blanquecina, espesa, grumosa, adherida a las paredes vaginales, sin mal olor"}),
    (r"vaginitis aguda|vulvovaginitis", {"genital": "vulva eritematosa y edematosa; flujo vaginal amarillento, purulento, fétido y abundante, con eritema de las paredes vaginales y cuello uterino"}),
    (r"vaginosis bacteriana", {"genital": "flujo vaginal grisáceo, homogéneo, fluido, de olor a pescado, adherido a las paredes vaginales, sin eritema marcado"}),
    (r"cervicitis", {"genital": "secreción mucopurulenta por el orificio cervical, cuello uterino eritematoso y friable, con sangrado al contacto; dolor leve a la movilización cervical"}),
    (r"vulvitis", {"genital": "vulva eritematosa, edematosa y dolorosa, con fisuras o excoriaciones y flujo escaso"}),
    (r"prurito vulvar", {"genital": "vulva con excoriaciones por rascado, eritema leve y liquenificación"}),
    (r"herpes simple genital|infeccion genital|genital u orogenital", {"genital": "vesículas agrupadas y úlceras superficiales dolorosas sobre base eritematosa en región genital, con adenopatías inguinales dolorosas"}),
    (r"verrugas genitales", {"genital": "lesiones papilomatosas, verrugosas, en forma de coliflor, en región genital y perianal"}),
    (r"infecciones transmitidas sexualmente|contacto con o exposicion a enfermedades infecciosas con un modo de transmision", {"genital": "secreción anormal o lesiones genitales, adenopatías inguinales; a valorar según el caso"}),
    (r"balanopostitis", {"genital": "glande y prepucio eritematosos, edematosos, con secreción blanquecina y erosiones"}),
    (r"prepucio redundante|fimosis", {"genital": "prepucio que no logra retraerse, con edema y eritema; en parafimosis, glande edematoso y doloroso"}),
    (r"enfermedades del aparato genital masculino", {"genital": "aumento de volumen escrotal doloroso, con eritema o masa a la palpación"}),
    (r"incontinencia urinaria", {"genital": "escape de orina con la maniobra de Valsalva; cistocele a valorar"}),
    (r"infeccion urinaria|cistitis|enfermedades del sistema genitourinario", {"genital": "dolor suprapúbico a la palpación", "lumbar": "puño percusión lumbar negativa o dolorosa si hay compromiso alto"}),
    (r"colico nefritico", {"general": "paciente inquieta/o, con dolor intenso", "lumbar": "puño percusión lumbar positiva del lado afectado"}),
    (r"mastodinia|trastornos de la mama sin|dolor mamario", {"mamas": "mamas simétricas, dolor a la palpación bilateral y sensibilidad difusa; sin masas, retracciones ni secreción por el pezón"}),
    (r"trastornos inflamatorios de la mama|mastitis puerperal", {"mamas": "mama con eritema, calor, induración y dolor a la palpación; sin zona fluctuante; adenopatías axilares dolorosas"}),
    (r"tumor o masa en el seno|nodulo mamario|neoplasia benigna de la mama", {"mamas": "masa palpable en la mama, de bordes definidos, móvil, no adherida a planos profundos, sin cambios en la piel ni secreción por el pezón; sin adenopatías axilares"}),
    (r"neoplasias malignas de mama", {"mamas": "masa mamaria dura, de bordes irregulares, adherida a planos, con retracción de piel o pezón y adenopatías axilares"}),
    (r"galactorrea", {"mamas": "secreción láctea bilateral a la expresión de los pezones; sin masas"}),
    (r"leiomioma|miomatosis|masa o tumor intraabdominal|tumefaccion, masa", {"genital": "tacto bimanual con útero aumentado de tamaño, irregular, de consistencia firme, no doloroso"}),
    (r"menstruacion excesiva|regularidad anormal|trastornos hemorragicos|hemorragia uterina|amenorrea$|^amenorrea\b", {"genital": "sangrado vaginal escaso o abundante con coágulos; cuello uterino sin lesiones; útero de tamaño normal, no doloroso"}),
    (r"dismenorrea|dolor pelvico femenino", {"genital": "dolor a la palpación en hipogastrio y a la movilización cervical, útero y anexos sin masas"}),
    (r"sintoma o molestia premenstrual|trastornos premenstruales", {"mamas": "mamas con sensibilidad y nodularidad difusa", "general": "paciente irritable"}),
    (r"menopausia", {"genital": "mucosa vaginal pálida, delgada y seca, con atrofia vulvovaginal", "general": "paciente con bochornos y sudoración"}),
    (r"examen ginecologico|examen o prueba de embarazo", {"genital": "genitales externos sin lesiones; cuello uterino de aspecto normal si se explora"}),
    (r"estado de embarazo|supervision de embarazo|amenorrea por embarazo|embarazo", {"general": "paciente en aceptable estado general, con ganancia de peso acorde", "genital": "útero gestante con altura uterina acorde a la edad gestacional, frecuencia cardíaca fetal presente y sin sangrado ni pérdida de líquido", "extremidades": "sin edema significativo ni várices"}),
    (r"amenaza de aborto|aborto|hemorragia al comienzo|hemorragia obstetrica|hemorragia", {"general": "paciente pálida, con taquicardia leve", "genital": "sangrado vaginal escaso o moderado de color rojo oscuro; cuello uterino cerrado; útero acorde a la edad gestacional"}),
    (r"preeclam|eclampsia|hipertension gestacional|edema, proteinuria|edema gestacional", {"general": "paciente con cifras tensionales elevadas, edema palpebral y facial", "extremidades": "edema con fóvea en miembros inferiores, reflejos osteotendinosos aumentados", "genital": "altura uterina acorde; frecuencia cardíaca fetal presente"}),
    (r"vomitos excesivos|desnutricion en el embarazo", {"general": "paciente con mucosas secas, pérdida de peso y decaimiento", "genital": "útero gestante acorde a la edad gestacional"}),
    (r"parto|trabajo de parto|puerperio|posparto|complicaciones principalmente relacionadas con el puerperio", {"genital": "útero involucionando, a nivel infraumbilical, loquios en cantidad y aspecto normales; herida quirúrgica o episiorrafia sin signos de infección"}),
    (r"mastitis", {}),
    (r"anticoncepcion|planificacion familiar|dispositivo|consejo sobre menopausia|asesoramiento", {}),
    (r"disfunciones sexuales|salud sexual|sexualidad", {"genital": "genitales externos sin alteraciones; sin lesiones ni signos de infección"}),
    (r"cancer de ovario|neoplasias malignas de la vagina|neoplasias malignas de la vulva|neoplasias malignas del cuello uterino|neoplasias malignas del pene", {"genital": "lesión exofítica o ulcerada, friable, que sangra al contacto, de bordes irregulares; adenopatías inguinales"}),
    (r"adolescencia", {"cabeza": "lesiones de acné (comedones, pápulas y pústulas) en cara", "torax": "lesiones de acné en espalda y tórax"}),
    (r"complicaciones del trabajo de parto|complicacion obstetrica|atencion materna relacionada al feto|trastornos maternos", {"genital": "altura uterina acorde o discordante con la edad gestacional, frecuencia cardíaca fetal presente"}),
]

try:
    from services.examen_variantes import VARIANTES
except ImportError:
    VARIANTES = {}


class _Primera:
    @staticmethod
    def choice(op):
        return op[0]


def _var(texto, rng):
    """Una redacción al azar entre las versiones de ese hallazgo (todas con la misma positividad)."""
    op = VARIANTES.get(texto)
    return rng.choice(op) if op else texto


_COMPILADAS = [(re.compile(p), h) for p, h in RULES]


def _hallazgos(descripciones):
    """{parte: [textos]} sumando los de cada diagnóstico (sin repetir)."""
    out = {}
    for d in descripciones:
        nombre = cat.plain(d or "")
        if not nombre:
            continue
        for rx, h in _COMPILADAS:
            if rx.search(nombre):
                for k, v in h.items():
                    if v and v not in out.setdefault(k, []):
                        out[k].append(v)
    return out


def _unir(items):
    return "; ".join(items)


def compose(descripciones, ssr=False, rng=None):
    """Texto del examen físico, una línea por sección, en el orden céfalo-caudal."""
    rng = rng or _Primera()                # sin rng: siempre la primera redacción (estable para las pruebas)
    h = _hallazgos(descripciones)
    lineas = []
    for titulo, partes in SECCIONES:
        if titulo == "Genitourinario" and not ssr and not any(k in h for k in GU):
            continue
        trozos = []
        for clave, normal in partes:
            if clave in h and clave != "abdomen":
                trozos.append(_unir([_var(x, rng) for x in h[clave]]))
            elif normal:
                trozos.append(_var(normal, rng))
        if titulo == "Corazón" and False:
            pass
        if not trozos:
            continue
        txt = ", ".join(trozos) if titulo == "ORL" else "; ".join(trozos) if titulo not in ("Extremidades", "Genitourinario") else "; ".join(trozos)
        txt = txt.strip()
        for pref in (titulo.lower() + " ", "extremidades " if titulo == "Extremidades" else titulo.lower() + " "):
            if txt.lower().startswith(pref):
                txt = txt[len(pref):]
                break
        lineas.append(f"{titulo}: {txt[:1].upper() + txt[1:]}.")
    return " ".join(lineas)
