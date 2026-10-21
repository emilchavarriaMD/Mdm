"""Frases por grupo clínico para el plan de APS (se suman a las de cada diagnóstico) y la clasificación por nombre."""
import re
import unicodedata


def _p(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


# (grupo, patrón sobre el nombre sin tildes); el primero que coincide gana
REGLAS = [
    ("neo", r"cancer|neoplasia|carcinoma|leucemia|sarcoma|tumor"),
    ("emb", r"embarazo|parto|puerper|obstetr|gestacion|eclamps|preeclam|aborto|perinatal|prenatal|materna|posparto|hemorragia obstet"),
    ("gin", r"vagin|vulv|cervicitis|menstru|amenorrea|dismenorrea|menopaus|mastitis|mastodinia|galactorrea|leiomioma|pelvico femenino|sexual|anticoncep|ginecolog|uterin|seno femenino|mama|premenstrual"),
    ("uro", r"urinari|nefritic|prostat|renal|balanopost|genital masculino|prepucio|incontinencia"),
    ("ojo", r"conjuntiv|catarata|retin|chalacion|orzuelo|queratitis|vision|ocular|parpado|nistagmo|motor ocular|refraccion|globo ocular|anexos oculares"),
    ("orl", r"oido|otitis|otalgia|cerumen|periodont|caries|aftas|gingiv|candidiasis labial|disfonia|polipo nasal|periapical|amigdal|faring|laring|nasofaring|sinusitis|rinitis|vertigo|vestibular|mareo"),
    ("res", r"asma|bronqu|neumon|tos$|^tos|covid|influenza|respirator|pulmonar|tuberculosis"),
    ("dig", r"gastr|diarrea|vomito|nausea|dispepsia|reflujo|estrenimiento|hemorroides|abdominal|hernia|intestin|hepatitis|digestivo|apetito|anorexia|colon|ano o|conducto anal|parasit"),
    ("inf", r"dengue|zika|chikungunya|fiebre|paludismo|chagas|varicela|rubeola|sarampion|viruela|inmunodeficiencia|infecciosas|transmitidas sexual|ssr|exposicion a enfermedades"),
    ("pie", r"piel|dermat|absceso|celulitis|foliculitis|furunculo|impetigo|herpes|verruga|molusco|pediculosis|sarna|pitiriasis|erupcion|urticaria|quemadura|ulcera|una encarnada|prurigo|prurito|cutane|panal|zoster"),
    ("tra", r"traumatis|herida|mordedura|picadura|fractura|luxacion|esguince|distension|lesion|envenenamiento|veneno|ruptura|accidente|causas externas|maltrato"),
    ("msk", r"artr|osteo|lumbar|ciatica|muscul|tendin|bursitis|hombro|columna|rotula|espolon|torticolis|tenosinovitis|ganglion|contractura|mialgia|condropat|polimialgia|deformidad|dolor articular|dolor agudo|esqueletic"),
    ("neu", r"cefalea|migrana|epilepsia|convulsi|parkinson|neuropat|nervio|polineuro|radiculopat|sistema nervioso|distrofia|paralisis|neuralgia|autonomo|dolor neuropatico"),
    ("men", r"depresi|ansiedad|insomnio|sueno|estres|personalidad|esquizofrenia|mental|circadiano|habla|lenguaje|desarrollo"),
    ("cro", r"hipertens|diabetes|colesterol|lipid|trigliceri|obesidad|cardiopat|angina|arritmia|aterosc|insuficiencia|metabol|tiroid|endocrin|hipotension|hipoglucemia|anemia|circulatorio|venosa|linfedema|oclusiva|edema|sangre|torac|hipofisis|nutricion|desnutricion"),
    ("ped", r"nino|recien nacido|neonat|lactante|panal|crecimiento|adolescencia|bilirrubin|onfalitis|bajo peso|falta del desarrollo"),
]


def grupo(nombre):
    t = _p(nombre)
    for g, rx in REGLAS:
        if re.search(rx, t):
            return g
    return "gen"


# Para los grupos de salud sexual y reproductiva se reutilizan las frases de tools/plan_ssr/g.py (mismos nombres)
APS = {
 "res": (["lavarse las manos con frecuencia y después de toser", "ventilar la habitación varias veces al día", "tomar bebidas tibias para aliviar la garganta y la tos", "evitar los cambios bruscos de temperatura", "evitar permanecer en lugares cerrados con mucha gente",
          "usar mascarilla si convive con personas vulnerables", "evitar el humo de tabaco leña y carbón", "dormir con la cabeza elevada", "mantener una alimentación ligera y nutritiva", "limpiar con frecuencia las superficies de uso común",
          "reposar mientras haya fiebre o decaimiento", "evitar los irritantes como polvo perfumes e insecticidas", "no suspender el tratamiento aunque mejoren los síntomas", "acudir al control si no mejora en el tiempo indicado"],
         ["respiración rápida o con esfuerzo", "labios o uñas azulados", "fiebre alta que no cede", "dolor en el pecho al respirar", "somnolencia o confusión"]),
 "dig": (["comer en porciones pequeñas y masticar despacio", "evitar alimentos grasosos picantes o muy condimentados", "evitar el alcohol el café y las bebidas gaseosas", "tomar agua hervida o potable", "lavarse las manos antes de comer y después de ir al baño",
          "lavar y cocinar bien los alimentos", "no acostarse inmediatamente después de comer", "mantener horarios regulares de comida", "aumentar el consumo de fibra de forma gradual", "evitar el tabaco",
          "mantener una buena hidratación", "registrar los alimentos que empeoran los síntomas", "evitar la automedicación con analgésicos", "acudir al control si los síntomas persisten"],
         ["dolor abdominal intenso que no cede", "vómito con sangre o heces negras", "signos de deshidratación", "fiebre alta", "abdomen duro o muy distendido"]),
 "pie": (["mantener la piel limpia y seca", "bañarse a diario con agua tibia y jabón suave", "usar ropa de algodón holgada", "evitar rascarse o tocar las lesiones", "mantener las uñas cortas y limpias",
          "no compartir toallas ropa ni objetos de aseo", "lavar la ropa de cama con agua caliente", "evitar los productos irritantes o perfumados", "evitar la exposición solar directa en la zona afectada", "no aplicar remedios caseros sobre las lesiones",
          "lavarse las manos después de tocar las lesiones", "mantener la piel hidratada con lo indicado", "completar el tratamiento indicado", "acudir al control si las lesiones aumentan o no mejoran"],
         ["lesiones que se extienden rápidamente", "fiebre", "dolor intenso o pus", "enrojecimiento y calor crecientes", "hinchazón de la cara o los labios"]),
 "ojo": (["evitar frotarse los ojos", "lavarse las manos antes de tocar los ojos", "no compartir toallas ni maquillaje", "evitar los lentes de contacto mientras dure el cuadro", "usar lentes de sol en exteriores",
          "evitar el humo y el polvo", "aplicar las gotas exactamente como se indicó", "descansar la vista en el trabajo con pantallas", "mantener buena iluminación al leer", "limpiar suavemente los párpados con agua tibia",
          "evitar el maquillaje en los ojos hasta la curación", "acudir a control oftalmológico periódico", "no usar gotas sin indicación médica", "acudir al control si no mejora"],
         ["pérdida o disminución de la visión", "dolor intenso del ojo", "enrojecimiento intenso con sensibilidad a la luz", "visión doble", "destellos o sombras nuevas"]),
 "orl": (["evitar la entrada de agua al oído", "no introducir hisopos ni objetos en el oído", "tomar abundantes líquidos", "evitar el humo de tabaco", "mantener la nariz despejada con suero fisiológico",
          "dormir con la cabeza elevada", "evitar los ruidos intensos", "evitar los cambios bruscos de temperatura", "mantener una buena higiene bucal", "evitar alimentos muy calientes o ácidos mientras haya dolor",
          "descansar la voz si hay ronquera", "evitar el alcohol y el tabaco", "no usar gotas ni enjuagues sin indicación", "acudir al control si no mejora"],
         ["fiebre alta", "dificultad para respirar o tragar", "hinchazón de la cara o del cuello", "pérdida de la audición o mareo intenso", "sangrado que no cede"]),
 "msk": (["evitar el sobreesfuerzo de la zona afectada", "alternar el reposo con la actividad", "aplicar frío las primeras 48 horas y luego calor", "realizar estiramientos suaves", "mantener una buena postura",
          "evitar cargar peso excesivo", "usar calzado cómodo y estable", "mantener un peso saludable", "retornar poco a poco a las actividades", "hacer pausas activas si trabaja sentado o de pie",
          "evitar los movimientos bruscos o repetitivos", "usar el soporte o vendaje indicado", "no masajear con fuerza la zona dolorosa", "acudir al control si no mejora"],
         ["dolor intenso que no cede", "hinchazón roja y caliente", "debilidad o adormecimiento", "imposibilidad de mover la zona", "fiebre"]),
 "tra": (["reposar la zona afectada", "aplicar frío local las primeras 48 horas", "mantener elevada la zona lesionada", "mantener las heridas limpias y cubiertas", "no aplicar remedios caseros sobre las heridas",
          "revisar la vacuna contra el tétanos", "evitar el esfuerzo con la zona lesionada", "acudir a las curaciones indicadas", "vigilar el color calor e hinchazón de la zona", "evitar el alcohol mientras dure la recuperación",
          "usar el vendaje o la férula como se indicó", "retornar gradualmente a la actividad", "mantener una alimentación nutritiva para la cicatrización", "acudir al control si no mejora"],
         ["fiebre", "dolor intenso que aumenta", "sangrado que no cede", "pus o mal olor", "adormecimiento o frío en la extremidad"]),
 "neu": (["dormir en horarios regulares", "evitar el alcohol y el tabaco", "mantener una alimentación balanceada y no saltarse comidas", "realizar ejercicio regular", "manejar el estrés con técnicas de relajación",
          "llevar un diario de síntomas con fecha y duración", "evitar los desencadenantes identificados", "tomar los medicamentos todos los días sin saltarse dosis", "evitar manejar o subir a alturas si hay mareo o convulsiones", "acompañarse en las actividades de riesgo",
          "mantener una buena hidratación", "limitar el uso de pantallas", "acudir a los controles programados", "informar a la familia sobre qué hacer en una crisis"],
         ["pérdida del conocimiento", "debilidad de un lado del cuerpo", "dificultad para hablar", "dolor de cabeza intenso y repentino", "convulsión que dura más de 5 minutos"]),
 "men": (["mantener horarios regulares de sueño", "realizar ejercicio regular", "practicar técnicas de respiración y relajación", "mantener contacto con familiares y amigos", "evitar el alcohol y las drogas",
          "reducir la cafeína", "mantener una alimentación balanceada", "plantear metas pequeñas y alcanzables", "limitar el tiempo en pantallas y redes antes de dormir", "acudir a psicoterapia con constancia",
          "tomar los medicamentos como se indican sin suspenderlos solo", "pedir apoyo a una persona de confianza", "mantener rutinas diarias", "acudir a los controles programados"],
         ["ideas de hacerse daño o de quitarse la vida", "aislamiento completo", "no comer ni dormir por varios días", "ideas delirantes o alucinaciones", "agitación intensa"]),
 "cro": (["seguir una alimentación baja en sal azúcares y grasas", "realizar al menos 150 minutos de actividad física por semana", "mantener un peso saludable", "evitar el tabaco y el exceso de alcohol", "tomar los medicamentos todos los días a la misma hora",
          "no suspender el tratamiento aunque se sienta bien", "acudir a los controles y laboratorios indicados", "llevar un registro de las mediciones en casa", "dormir de 7 a 8 horas", "manejar el estrés",
          "revisar los pies a diario si tiene diabetes", "mantener una buena hidratación", "evitar los alimentos ultraprocesados", "informar a todo el personal de salud sobre sus enfermedades y medicamentos"],
         ["dolor en el pecho", "falta de aire", "dolor de cabeza intenso", "mareo o desmayo", "sed excesiva con orina frecuente"]),
 "inf": (["reposar en casa mientras haya fiebre", "tomar abundante líquido", "controlar la fiebre con medios físicos", "usar mosquitero y repelente", "eliminar los criaderos de zancudos alrededor de la casa",
          "lavarse las manos con frecuencia", "evitar el contacto cercano con personas vulnerables mientras dure el cuadro", "mantener una alimentación ligera y nutritiva", "evitar la automedicación con antiinflamatorios", "usar ropa de manga larga en zonas con zancudos",
          "vigilar la temperatura cada 6 horas", "completar el tratamiento indicado", "avisar a los contactos cercanos si corresponde", "acudir al control en la fecha indicada"],
         ["fiebre alta persistente", "sangrado de encías o nariz", "dolor abdominal intenso", "vómitos persistentes", "somnolencia o confusión"]),
 "uro": (["tomar abundante agua durante el día", "orinar sin aguantar las ganas", "mantener una buena higiene genital", "evitar el alcohol y el café en exceso", "usar ropa interior de algodón",
          "orinar después de las relaciones sexuales", "evitar el estreñimiento", "mantener una alimentación baja en sal", "evitar los antiinflamatorios sin indicación", "completar el tratamiento indicado",
          "acudir al control con los estudios indicados", "usar preservativo en las relaciones sexuales", "vigilar el color y el volumen de la orina", "acudir al control si no mejora"],
         ["fiebre con escalofríos", "dolor intenso en la espalda baja", "sangre en la orina", "imposibilidad de orinar", "vómitos persistentes"]),
 "neo": (["acudir sin demora a la valoración especializada", "llevar todos los estudios y resultados a las consultas", "evitar el tabaco y el alcohol", "mantener una alimentación nutritiva", "descansar lo suficiente",
          "acompañarse a las citas médicas", "buscar apoyo psicológico y familiar", "no usar remedios ni productos no comprobados", "mantener los controles programados", "llevar un registro de los síntomas",
          "mantener una buena hidratación", "realizar actividad física suave según tolerancia", "informar a los familiares sobre el diagnóstico para su prevención", "conocer los servicios de apoyo disponibles"],
         ["sangrado anormal", "pérdida de peso sin causa", "dolor persistente que no cede", "bulto que crece rápidamente", "falta de aire"]),
 "ped": (["acudir a los controles de crecimiento y desarrollo", "mantener el esquema de vacunación al día", "ofrecer lactancia materna exclusiva hasta los 6 meses cuando corresponda", "ofrecer una alimentación variada y nutritiva según la edad", "lavarse las manos antes de alimentar al niño",
          "mantener la higiene del niño con agua y jabón suave", "dormir al bebé boca arriba", "evitar el humo de tabaco en el hogar", "estimular el juego y el lenguaje", "evitar los medicamentos sin indicación del médico",
          "registrar el peso y la talla en cada control", "mantener el ambiente abrigado pero no excesivo", "evitar visitas con síntomas de enfermedad", "acudir al control en la fecha indicada"],
         ["rechazo del alimento", "fiebre o temperatura baja en el recién nacido", "respiración rápida o con esfuerzo", "decaimiento o llanto inconsolable", "color amarillo o azul de la piel"]),
 "gen": (["descansar lo suficiente", "tomar abundante agua", "mantener una alimentación balanceada", "dormir de 7 a 8 horas", "evitar el tabaco y el alcohol",
          "realizar actividad física suave según tolerancia", "llevar un registro de los síntomas", "evitar la automedicación", "manejar el estrés", "lavarse las manos con frecuencia",
          "acudir a los estudios indicados", "llevar los resultados a las consultas", "mantener los controles programados", "acudir al control si no mejora"],
         ["empeoramiento de los síntomas", "fiebre persistente", "dolor intenso", "dificultad para respirar", "debilidad o mareo intenso"]),
}
