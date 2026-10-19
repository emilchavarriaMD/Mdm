from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer.|Refiere que acude a entrega de medicamentos y control."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte|en espera de tratamiento"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"
CRON = "Refiere buena adherencia al tratamiento.|Refiere que ha omitido dosis del medicamento.|Refiere control con especialista.|Refiere que sus últimos exámenes fueron estables."

G(30, "exposición sexual sin protección con una pareja con infección de transmisión sexual conocida|preocupación por posible infección de transmisión sexual tras relación de riesgo|exposición sexual de riesgo reciente sin síntomas|solicita pruebas tras enterarse de que su pareja tiene una infección de transmisión sexual|contacto sexual de riesgo con pareja desconocida",
  "ansiedad|sin síntomas actuales|molestia genital leve|temor al contagio",
  "Refiere que la relación fue hace pocos días.|Refiere que su pareja fue diagnosticada recientemente.|Refiere que no utilizó preservativo.|Refiere nueva pareja sexual.|Refiere que desea pruebas y orientación.",
  "No ha recibido tratamiento.|Recibió orientación previa.",
  "secreción genital|úlceras genitales|dolor al orinar|dolor pélvico|erupción en piel|fiebre", dur="-")
G(308, "cansancio fácil|astenia sin causa aparente|fatiga que limita sus actividades|decaimiento y falta de energía|cansancio con sueño no reparador",
  "somnolencia|falta de concentración|mareo leve|hiporexia|cefalea leve",
  "Refiere estrés laboral o familiar.|Refiere pocas horas de sueño.|Refiere dieta desordenada.|Refiere cuadro viral previo.|Refiere sobrecarga de trabajo.",
  TXN, "fiebre|pérdida de peso|dolor torácico|disnea|sangrado|sudoración nocturna", dur="B")
G(309, "lesión en la mano tras accidente|herida o contusión en la mano por un golpe|dolor y edema en la mano tras caída|lesión por accidente doméstico|lesión por atrapamiento de la mano",
  "edema local|equimosis|dolor al movimiento|herida superficial|limitación para cerrar la mano",
  "Refiere accidente doméstico.|Refiere accidente laboral.|Refiere caída reciente.|Refiere que ocurrió hace pocas horas.",
  "Se aplicó hielo con alivio parcial.|Se lavó la herida con agua y jabón.|No ha recibido tratamiento.",
  "deformidad|pérdida de sensibilidad|herida profunda|sangrado importante|incapacidad para mover los dedos", dur="H")
G(310, "ingesta accidental de un producto|ingestión accidental de sustancia de limpieza|ingesta de medicamento por error|intoxicación leve por ingestión de producto desconocido|contacto accidental con producto químico",
  "náuseas|vómitos|dolor abdominal|ardor en boca o garganta|mareo|somnolencia|sialorrea",
  "Según refiere el acompañante, ocurrió hace pocas horas.|Refiere que el producto estaba al alcance.|Refiere que desconoce la cantidad ingerida.|Refiere que se trata de un medicamento.|Refiere que no provocó el vómito.",
  "No ha recibido tratamiento.|Tomó agua o leche tras la ingesta.",
  "dificultad respiratoria|convulsiones|pérdida del conocimiento|vómitos con sangre|quemaduras en boca|ingesta intencional", dur="H")
G(311, "encías sangrantes ocasionales|sangrado de encías con fatiga y debilidad|dieta pobre con encías sangrantes|piel seca y caída del cabello con dieta insuficiente|fatiga y mala cicatrización con alimentación pobre",
  "caída del cabello|piel seca|fatiga|mala cicatrización|palidez|hiporexia",
  "Refiere dieta pobre en frutas y verduras.|Refiere ingesta insuficiente de alimentos.|Refiere dificultades económicas.|Refiere dieta monótona.|Refiere pérdida de peso reciente.",
  "No ha recibido tratamiento.|Tomó multivitamínicos sin mejoría.",
  "sangrado importante|fiebre|edema generalizado|diarrea crónica|dificultad para caminar", dur="L")
G(312, "lesiones en piel pruriginosas|erupción en piel con prurito y descamación|manchas y placas en piel con picazón|lesiones cutáneas con enrojecimiento y costras|piel con lesiones de aparición reciente",
  "prurito|descamación|enrojecimiento|costras|resequedad|ardor",
  "Refiere contacto con productos químicos.|Refiere exposición solar.|Refiere inicio de nuevos medicamentos.|Refiere antecedente de piel sensible.|Refiere estrés.",
  "Se aplicó crema hidratante con alivio parcial.|Se aplicó crema con corticoide sin mejoría.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|dolor intenso|lesiones en mucosas|ampollas", dur="B")
G(313, "moretones con facilidad en piernas|equimosis frecuentes con sangrado de encías|palidez con moretones espontáneos|sangrado nasal frecuente con fatiga|aparición de manchas violáceas sin trauma",
  "sangrado de encías|sangrado nasal|palidez|fatiga|petequias|menstruaciones abundantes",
  "Refiere uso de anticoagulantes o antiinflamatorios.|Refiere antecedente familiar de problemas de coagulación.|Refiere dieta pobre en hierro.|Refiere menstruaciones abundantes.",
  "No ha recibido tratamiento.|Se realizó exámenes previos.",
  "sangrado profuso|fiebre|dolor óseo|pérdida de peso|sangre en heces u orina|confusión", dur="L")
G(314, "molestia en un oído|sensación de oído tapado|dolor leve y sensación de plenitud en oído|picazón en el oído con hipoacusia|zumbido en un oído",
  "hipoacusia leve|acúfenos|prurito ótico|plenitud ótica|dolor leve|mareo",
  "Refiere uso de hisopos.|Refiere cuadro gripal previo.|Refiere ingreso de agua al oído.|Refiere exposición a ruido.",
  "Se aplicó gotas caseras sin mejoría.|No ha recibido tratamiento.",
  "secreción por el oído|fiebre|vértigo intenso|parálisis facial|dolor intenso|trauma ótico", dur="B")
G(315, "palpitaciones ocasionales|latidos rápidos y sensación de desfallecimiento|palpitaciones con ansiedad|sensación de latidos irregulares ocasionales|palpitaciones que ceden con el reposo",
  "mareo|ansiedad|sudoración|disnea leve|dolor torácico leve|fatiga",
  "Refiere consumo de café o bebidas energéticas.|Refiere estrés reciente.|Refiere pocas horas de sueño.|Refiere antecedente de hipertensión.|Refiere antecedente de enfermedad tiroidea.",
  TXN, "síncope|dolor torácico opresivo|disnea importante|palpitaciones sostenidas|sudoración fría", dur="B")
G(316, "molestias digestivas|malestar abdominal con náuseas y distensión|ardor y pesadez después de las comidas|cambios en el ritmo evacuatorio con molestia abdominal|sensación de llenura y gases",
  "náuseas|distensión abdominal|flatulencia|ardor|estreñimiento|diarrea ocasional",
  "Refiere ingesta de alimentos irritantes.|Refiere estrés reciente.|Refiere comidas irregulares.|Refiere consumo de café o alcohol.",
  TXA, "vómitos persistentes|sangre en heces|pérdida de peso|fiebre|ictericia|dolor abdominal intenso", dur="B")
G(317, "reacciones alérgicas repetidas en piel|ronchas y prurito recurrentes|episodios repetidos de estornudos y prurito|reacciones alérgicas con edema leve de párpados|erupciones alérgicas tras ciertos alimentos o medicamentos",
  "prurito|ronchas|estornudos|edema de párpados|lagrimeo|rinorrea",
  "Refiere antecedente familiar de alergias.|Refiere que reacciona al polvo o a ciertos alimentos.|Refiere episodios similares previos.|Refiere contacto con mascotas.",
  "Tomó antihistamínicos con alivio parcial.|No ha recibido tratamiento.",
  "dificultad respiratoria|edema de labios o lengua|silbidos en el pecho|mareo|dolor abdominal intenso", dur="L")
G(318, "dolor en articulaciones y músculos|dolor osteomuscular generalizado|rigidez y dolor en articulaciones al despertar|dolor en espalda, rodillas y manos|molestias musculares y articulares tras actividad",
  "rigidez matutina|fatiga|limitación leve de movimientos|crujidos|edema leve|calambres",
  "Refiere esfuerzo físico frecuente.|Refiere trabajo con cargas pesadas.|Refiere sobrepeso.|Refiere sedentarismo.|Refiere cuadro viral previo.",
  TXA, "fiebre|enrojecimiento articular|deformidad|pérdida de fuerza|trauma reciente|pérdida de peso", dur="B")
G(319, "hormigueo en manos y pies|adormecimiento y hormigueo en extremidades|parestesias con debilidad leve|sensación de corriente en manos|entumecimiento de pies con ardor",
  "debilidad leve|calambres|ardor|dolor nocturno|mareo|torpeza para manipular objetos",
  "Refiere diabetes mellitus.|Refiere postura prolongada.|Refiere movimientos repetitivos de manos.|Refiere consumo de alcohol.|Refiere dieta pobre.",
  TXN, "debilidad de una extremidad|dificultad para hablar|pérdida de control de esfínteres|pérdida del equilibrio|alteración visual", dur="B")
G(320, "tos y congestión nasal|tos con rinorrea y dolor de garganta|congestión nasal con tos nocturna|tos con flemas y malestar general|obstrucción nasal con estornudos y tos",
  "rinorrea|odinofagia|estornudos|fiebre baja|cefalea|malestar general",
  "Refiere contacto con personas con cuadro respiratorio.|Refiere cambios bruscos de temperatura.|Refiere exposición a polvo o humo.|Refiere asistencia a escuela o trabajo con casos similares.",
  TXA, "dificultad respiratoria|fiebre alta|dolor torácico|esputo con sangre|silbidos en el pecho", dur="A")
G(321, "visión borrosa|visión borrosa con cefalea|dificultad para enfocar de cerca|disminución de la visión de lejos|visión nublada intermitente",
  "cefalea|fatiga visual|lagrimeo|ardor ocular|dificultad para leer",
  "Refiere uso prolongado de pantallas.|Refiere que no se ha hecho examen visual hace años.|Refiere antecedente familiar de problemas visuales.|Refiere diabetes o hipertensión.",
  "No ha recibido tratamiento.|Usa lentes con graduación antigua.",
  "pérdida súbita de visión|dolor ocular intenso|destellos luminosos|trauma ocular|diplopía", dur="B")
G(322, "acude a control con dolor mamario o masa conocida|refiere nódulo en mama de crecimiento progresivo|refiere cambios en la piel de la mama|acude por entrega de medicamento sin molestias nuevas|refiere dolor óseo o fatiga",
  "masa mamaria|cambios en la piel|retracción del pezón|secreción por el pezón|adenopatía axilar|dolor óseo",
  ONC, ONCTX, ONCN, "Y")
G(323, "masa en estudio|masa palpable en estudio con biopsia pendiente|nódulo de comportamiento incierto en seguimiento|masa localizada hallada recientemente|bulto con crecimiento lento en estudio",
  "dolor leve|crecimiento lento|molestia local|pérdida de peso leve",
  "Refiere que tiene estudios de imagen pendientes.|Refiere biopsia pendiente.|Refiere antecedente familiar de neoplasias.|Refiere que la masa ha crecido.",
  "No ha recibido tratamiento.|En estudio diagnóstico.",
  "pérdida de peso importante|fiebre|sangrado|dolor intenso|adenopatías", dur="L")
G(324, "alteración congénita conocida|acude a seguimiento por anomalía congénita|acude a control de alteración del desarrollo desde el nacimiento|acude por molestias relacionadas con su malformación congénita|seguimiento de defecto congénito sin síntomas nuevos",
  "retraso del desarrollo|infecciones frecuentes|limitación funcional|dificultad para alimentarse|molestia local",
  "La madre refiere que fue notada al nacer.|La madre refiere control con especialista.|La madre refiere antecedentes familiares.|La madre refiere control prenatal completo.",
  "En seguimiento especializado.|No ha recibido tratamiento.",
  "fiebre|dificultad respiratoria|cianosis|convulsiones|vómitos persistentes", dur="-")
G(325, "dolor cervical de intensidad moderada|cervicalgia con rigidez y limitación del giro|dolor en cuello que irradia a hombros|dolor cervical tras postura prolongada|dolor cervical con contractura muscular|dolor de cuello al despertar",
  "rigidez cervical|contractura|irradiación a hombros|cefalea occipital|limitación del giro|mareo",
  "Refiere postura prolongada frente a computadora.|Refiere dormir en mala posición.|Refiere esfuerzo físico o carga de peso.|Refiere estrés laboral.|Refiere exposición al aire frío.",
  TXA + "|Aplicó calor local con alivio parcial.", "fiebre|debilidad de brazos|hormigueo intenso|trauma cervical|dificultad para tragar|rigidez con cefalea intensa", dur="A")
G(326, "utiliza anticonceptivos orales como método de planificación y acude a control|acude a control de anticonceptivos orales sin molestias|acude para continuar sus anticonceptivos orales|refiere náuseas leves y manchado con los anticonceptivos orales|refiere olvido ocasional de pastillas anticonceptivas",
  "náuseas leves|manchado intermenstrual|cefalea leve|mastalgia|aumento de peso|acné",
  "Refiere que toma sus pastillas todos los días.|Refiere uso del método desde hace más de un año.|Refiere olvidos ocasionales.|Refiere que desea continuar con el método.|Refiere ciclos regulares con el método.",
  "Recibe anticonceptivos orales combinados.|Recibe anticonceptivos orales de progestágeno.",
  "retraso menstrual|dolor en pantorrilla|cefalea intensa|alteraciones visuales|dolor torácico|sangrado abundante", dur="-")
G(327, "sensación de cuerpo extraño en el oído|dolor y sensación de objeto dentro del oído|hipoacusia con sensación de oído ocupado|molestia ótica tras introducir un objeto|zumbido y dolor tras ingreso de un insecto",
  "dolor ótico|hipoacusia|zumbido|prurito|sensación de movimiento dentro del oído|salida de secreción",
  "Refiere que introdujo un objeto pequeño en el oído.|Refiere que un insecto entró en el oído.|Según refiere la madre, el niño se introdujo un objeto.|Refiere uso de hisopos.|Refiere que el cuadro inició hace pocas horas.",
  "Intentó extraerlo sin éxito.|Se aplicó gotas caseras sin mejoría.|No ha recibido tratamiento.",
  "sangrado por el oído|fiebre|vértigo intenso|pérdida de la audición|trauma ótico", dur="H")
G(328, "descamación y prurito en piel cabelluda y cara|escamas grasosas en cuero cabelludo con prurito|enrojecimiento y descamación en cejas y surcos nasales|caspa abundante con enrojecimiento|placas eritematosas con escamas amarillentas en cara",
  "descamación grasosa|prurito|eritema|caspa|enrojecimiento nasolabial|costras en cuero cabelludo",
  "Refiere que los síntomas empeoran con el estrés o el frío.|Refiere piel grasa.|Refiere episodios similares previos.|Refiere uso de champú inadecuado.|Refiere antecedente familiar de caspa.",
  "Se aplicó champú anticaspa con alivio parcial.|Se aplicó crema hidratante sin mejoría.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|dolor intenso|caída intensa del cabello|lesiones diseminadas", dur="L")
G(329, "acude a control sin molestias y con buena adherencia a levotiroxina|refiere cansancio, aumento de peso e intolerancia al frío|refiere somnolencia, piel seca y estreñimiento|acude con resultados de TSH elevada|refiere caída del cabello y fatiga",
  "fatiga|aumento de peso|intolerancia al frío|piel seca|estreñimiento|caída del cabello|somnolencia",
  "Refiere buena adherencia al tratamiento.|Refiere que omite la dosis con frecuencia.|Refiere antecedente familiar de enfermedad tiroidea.|Refiere control con endocrinología.|Refiere que su TSH estuvo alterada.",
  "en tratamiento con levotiroxina|con uso irregular de levotiroxina|en tratamiento con levotiroxina y control de TSH",
  "palpitaciones|dolor torácico|bradicardia sintomática|confusión|edema generalizado", "Y")
G(330, "uñas engrosadas y amarillentas|uñas frágiles con cambio de color y descamación debajo de la uña|engrosamiento y deformidad de la uña|uñas amarillas con restos queratósicos|alteración de uñas con dolor al calzado",
  "engrosamiento ungueal|cambio de color|desprendimiento de la uña|dolor al calzado|mal olor|descamación periungueal",
  "Refiere pie de atleta previo.|Refiere uso de calzado cerrado.|Refiere trauma previo en la uña.|Refiere diabetes mellitus.|Refiere contacto con piscinas o duchas públicas.",
  "Se aplicó esmalte o crema antimicótica sin mejoría.|Se aplicó remedios caseros sin cambios.|No ha recibido tratamiento.",
  "dolor intenso|fiebre|secreción purulenta|enrojecimiento que se extiende|pérdida de sensibilidad", dur="L")
