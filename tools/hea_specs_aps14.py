from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer.|Refiere que acude a entrega de medicamentos y control."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte|en espera de tratamiento"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"
CRON = "Refiere buena adherencia al tratamiento.|Refiere que ha omitido dosis del medicamento.|Refiere control con especialista.|Refiere que sus últimos exámenes fueron estables."
GEN = "Refiere que los síntomas han ido en aumento.|Refiere estrés reciente.|Refiere que ya había tenido episodios similares.|Refiere que no ha consultado antes por esto."

G(274, "enrojecimiento y prurito en glande y prepucio|ardor y enrojecimiento en el glande con secreción blanquecina|irritación del glande con prurito|glande enrojecido y doloroso con olor desagradable|manchas rojas y descamación en glande",
  "secreción blanquecina|ardor al orinar|prurito|mal olor|edema del prepucio|dolor al retraer el prepucio",
  "Refiere higiene genital deficiente.|Refiere relaciones sexuales recientes.|Refiere uso reciente de antibióticos.|Refiere diabetes mellitus.|Refiere episodios previos.",
  "Se aplicó crema antimicótica con alivio parcial.|Se aplicó crema con corticoide sin mejoría.|No ha recibido tratamiento.",
  "fiebre|úlceras genitales|retención urinaria|secreción uretral|sangrado", dur="A")
G(275, "secreción blanquecina por los pezones|salida de leche por ambos pezones sin embarazo|secreción láctea espontánea de las mamas|humedad en el sostén por secreción de pezones|secreción por los pezones al comprimir las mamas",
  "amenorrea|cefalea|alteraciones visuales|dolor mamario|ciclos irregulares|disminución del deseo sexual",
  "Refiere que no está embarazada ni amamanta.|Refiere uso de anticonceptivos.|Refiere ciclos menstruales irregulares.|Refiere uso de medicamentos como antipsicóticos.|Refiere estrés.",
  "No ha recibido tratamiento.|Se realizó exámenes hormonales previos.",
  "masa mamaria|secreción con sangre|fiebre|alteración visual intensa|cefalea intensa", dur="L")
G(276, "acude a control sin molestias específicas|refiere cansancio y cambios de peso|refiere intolerancia al frío o al calor|acude con resultados hormonales alterados|acude por entrega de medicamento sin molestias",
  "fatiga|cambios de peso|intolerancia al frío|palpitaciones|sudoración|alteraciones menstruales",
  "Refiere control con endocrinología.|Refiere antecedente familiar de enfermedades endocrinas.|Refiere que sus exámenes de hormonas estaban alterados.|Refiere buena adherencia al tratamiento.",
  "en tratamiento hormonal|en seguimiento con endocrinología|con tratamiento irregular|sin tratamiento actual",
  "dolor torácico|dificultad respiratoria|vómitos persistentes|confusión|pérdida del conocimiento", "Y")
G(277, "sangrado vaginal fuera de su periodo menstrual|manchado intermenstrual|sangrado vaginal irregular tras relaciones sexuales|sangrado vaginal abundante y prolongado|sangrado vaginal con dolor pélvico",
  "dolor pélvico|coágulos|mareo|fatiga|dispareunia|flujo vaginal",
  "Refiere ciclos menstruales irregulares.|Refiere uso de anticonceptivos.|Refiere relaciones sexuales recientes.|Refiere menopausia.|Refiere antecedente de miomas o pólipos.",
  "No ha recibido tratamiento.|Se automedicó sin mejoría.",
  "fiebre|embarazo conocido|dolor abdominal intenso|síncope|pérdida de peso", dur="B")
G(278, "aumento de volumen en el escroto|dolor y edema testicular|dolor testicular con aumento de volumen|masa escrotal indolora|escroto edematoso con molestia al caminar",
  "dolor testicular|edema escrotal|sensación de peso|fiebre|enrojecimiento escrotal|molestia al orinar",
  "Refiere trauma previo en la zona.|Refiere relaciones sexuales sin protección.|Refiere esfuerzo físico reciente.|Refiere episodios similares previos.",
  TXA, "dolor súbito intenso|vómitos|fiebre alta|masa dura|secreción uretral|trauma reciente", dur="A")
G(279, "dolor y sensibilidad en mamas|dolor mamario bilateral con pesadez|molestia mamaria con aumento de volumen|dolor en mama con sensación de nódulos|mastalgia con sensibilidad al tacto",
  "pesadez mamaria|sensibilidad|nodularidad|dolor irradiado a la axila|aumento de volumen|cambios con el ciclo",
  "Refiere que el dolor varía con el ciclo menstrual.|Refiere uso de anticonceptivos.|Refiere antecedente familiar de cáncer de mama.|Refiere uso de sostén inadecuado.",
  "Se aplicó compresas calientes con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "nódulo palpable|secreción sanguinolenta por el pezón|cambios en la piel|fiebre|retracción del pezón", dur="L")
G(280, "fiebre, malestar general y mialgias|fiebre con escalofríos y cefalea|malestar general con fiebre y dolor de cuerpo|fiebre con astenia e hiporexia|fiebre con erupción y malestar",
  "escalofríos|cefalea|mialgias|astenia|hiporexia|náuseas|erupción",
  "Refiere contacto con personas enfermas.|Refiere viaje reciente.|Refiere exposición a mosquitos.|Refiere ingesta de alimentos o agua de dudosa procedencia.",
  TXA, "dificultad respiratoria|rigidez de cuello|sangrado|confusión|vómitos persistentes|fiebre mayor de 5 días", dur="A")
G(281, "acude a control con cefalea persistente|refiere cefalea, vómitos y alteraciones visuales|refiere debilidad progresiva de un lado del cuerpo|acude por entrega de medicamento sin molestias nuevas|refiere crisis convulsivas ocasionales",
  "cefalea matutina|vómitos|alteraciones visuales|convulsiones|debilidad focal|cambios de personalidad",
  ONC, ONCTX, "pérdida del conocimiento|convulsiones prolongadas|fiebre|vómitos persistentes|confusión", "Y")
G(282, "acude a control con adenopatías y fatiga|refiere pérdida de peso, sudoración nocturna y fiebre|refiere masas en cuello o axilas|acude por entrega de medicamento sin molestias nuevas|refiere fatiga y prurito generalizado",
  "adenopatías|sudoración nocturna|pérdida de peso|fiebre|fatiga|prurito",
  ONC, ONCTX, ONCN, "Y")
G(283, "acude a control por carcinoma in situ|acude por seguimiento posterior a resección de lesión|acude con resultado de biopsia previa|acude por seguimiento sin síntomas|acude a control sin molestias nuevas",
  "sangrado leve|molestia local|dolor leve|cambio de color de la lesión",
  "Refiere biopsia previa con carcinoma in situ.|Refiere seguimiento con especialista.|Refiere cirugía previa.|Refiere que está asintomática/o.",
  "en seguimiento clínico|en vigilancia sin tratamiento|con tratamiento irregular",
  "sangrado importante|dolor intenso|pérdida de peso|fiebre|masa creciente", "Y")
G(284, "masa blanda, móvil e indolora en espalda|nódulo subcutáneo de crecimiento lento|bulto blando indoloro en tejido subcutáneo|masa móvil bajo la piel sin cambios recientes|tumoración blanda que no duele",
  "crecimiento lento|movilidad bajo la piel|consistencia blanda|sin dolor|molestia estética",
  "Refiere que la masa lleva meses o años.|Refiere antecedente familiar de lipomas.|Refiere que no ha cambiado.|Refiere que la nota al apoyarse.",
  "No ha recibido tratamiento.|Se realizó ultrasonido previo.",
  "crecimiento rápido|dolor intenso|ulceración|fiebre|pérdida de peso|adenopatías", dur="L")
G(285, "masa en estudio en región abdominal|bulto abdominal palpable detectado recientemente|masa abdominal con dolor leve|aumento de volumen localizado en abdomen|masa abdominal hallada en ultrasonido",
  "dolor leve|distensión abdominal|pérdida de peso|saciedad temprana|náuseas|cambios en las evacuaciones",
  "Refiere que un estudio de imagen reportó una masa.|Refiere antecedente familiar de neoplasias.|Refiere que la masa ha crecido.|Refiere que no tiene estudios previos.",
  "No ha recibido tratamiento.|Se realizó ultrasonido previo.",
  "vómitos|fiebre|ictericia|sangrado digestivo|dolor intenso súbito|pérdida de peso importante", dur="L")
G(286, "evacuaciones líquidas|diarrea acuosa de varias veces al día|deposiciones blandas y frecuentes|diarrea con cólico abdominal leve|evacuaciones diarreicas con náuseas",
  "cólico abdominal|náuseas|distensión|urgencia evacuatoria|hiporexia|sed|fiebre baja",
  "Refiere ingesta de alimentos en la calle.|Refiere consumo de agua no tratada.|Refiere contacto con personas con diarrea.|Refiere ingesta de lácteos o mariscos.|Refiere uso reciente de antibióticos.",
  "Ha tomado suero oral con alivio parcial.|Se automedicó con antidiarreicos sin mejoría.|No ha recibido tratamiento.",
  "sangre en las heces|fiebre alta|deshidratación importante|dolor abdominal intenso|vómitos persistentes", dur="A")
G(287, "sensación de llenura después de comer y saciedad temprana|plenitud postprandial con eructos|dolor y pesadez en epigastrio tras las comidas|náuseas con saciedad precoz|distensión en la parte alta del abdomen después de comer",
  "eructos|náuseas|distensión epigástrica|hiporexia|pesadez|acidez",
  "Refiere comidas copiosas o muy grasosas.|Refiere estrés reciente.|Refiere consumo de café o alcohol.|Refiere uso de antiinflamatorios.|Refiere episodios similares previos.",
  "Tomó antiácidos con alivio parcial.|Tomó omeprazol con mejoría transitoria.|No ha recibido tratamiento.",
  "pérdida de peso|vómitos persistentes|sangrado digestivo|dificultad para tragar|anemia|dolor abdominal intenso", dur="B")
G(288, "buen estado general que acude a control de crecimiento y desarrollo|asintomático, acude a control de salud con su madre|control de niño sano con esquema de vacunación al día|acude a control para evaluación de peso y talla|acude a valoración de salud de rutina sin molestias",
  "buen apetito|sueño adecuado|actividad normal para su edad|desarrollo psicomotor acorde",
  "La madre refiere buena alimentación.|La madre refiere esquema de vacunación completo.|La madre refiere que no ha enfermado recientemente.|La madre refiere que juega y se desarrolla bien.|La madre refiere que asiste a la escuela.",
  "No ha recibido tratamiento.|Recibe suplementos según esquema.",
  "fiebre|tos|diarrea|vómitos|rechazo de alimentos|retraso del desarrollo", dur="-")
G(289, "buen estado general que acude a control del recién nacido|asintomático, acude a primer control con su madre|recién nacido con lactancia exclusiva que acude a control|acude a control de peso y cordón umbilical|recién nacido sin molestias que acude a revisión",
  "buena succión|evacuaciones normales|micción adecuada|sueño normal|cordón umbilical seco",
  "La madre refiere lactancia materna exclusiva.|La madre refiere parto atendido en unidad de salud.|La madre refiere que nació a término.|La madre refiere que el cordón umbilical sigue en su lugar.",
  "No ha recibido tratamiento.|Recibió vacunas del recién nacido.",
  "fiebre|ictericia|rechazo de las tomas|dificultad respiratoria|secreción por el ombligo", dur="-", u="días")
G(290, "nerviosismo, preocupación constante y dificultad para relajarse|ansiedad con palpitaciones y sensación de ahogo|crisis de angustia con temblor y sudoración|preocupación excesiva con tensión muscular e insomnio|miedo intenso con palpitaciones y opresión torácica",
  "palpitaciones|temblor|sudoración|opresión torácica|insomnio|tensión muscular|irritabilidad",
  "Refiere estrés laboral o familiar.|Refiere problemas económicos.|Refiere pérdida reciente de un ser querido.|Refiere consumo de café o estimulantes.|Refiere episodios similares previos.",
  "No ha recibido tratamiento.|Tomó infusiones relajantes con alivio parcial.|Se automedicó con ansiolíticos sin receta.",
  "ideas de hacerse daño|dolor torácico intenso|consumo de alcohol o drogas|alucinaciones|pérdida del conocimiento", dur="L")
G(291, "tristeza persistente, pérdida del interés en sus actividades y cansancio|estado de ánimo bajo con insomnio y hiporexia|desánimo, llanto fácil y dificultad para concentrarse|apatía con aislamiento y sentimientos de inutilidad|tristeza con cambios en el sueño y en el apetito",
  "llanto fácil|insomnio|hiporexia|fatiga|dificultad para concentrarse|aislamiento|sentimientos de culpa",
  "Refiere problemas familiares o económicos.|Refiere pérdida reciente de un ser querido.|Refiere antecedente de depresión.|Refiere estrés laboral.|Refiere que los síntomas afectan sus actividades.",
  "No ha recibido tratamiento.|Recibió apoyo psicológico previo.|Se automedicó con infusiones sin mejoría.",
  "ideas de hacerse daño|intento previo de suicidio|alucinaciones|consumo de alcohol o drogas|periodos de euforia", dur="L")
G(292, "pesadillas, recuerdos intrusivos y sobresaltos|insomnio con pesadillas recurrentes tras un evento traumático|hipervigilancia, irritabilidad y evitación de recuerdos|recuerdos intrusivos con ansiedad intensa|sobresaltos y dificultad para dormir desde un evento traumático",
  "hipervigilancia|irritabilidad|evitación de lugares o personas|insomnio|ansiedad|llanto fácil|aislamiento",
  "Refiere que vivió un evento traumático hace meses.|Refiere violencia previa.|Refiere dificultad para hablar de lo sucedido.|Refiere que los síntomas se desencadenan por recuerdos.",
  "No ha recibido tratamiento.|Recibió apoyo psicológico previo.",
  "ideas de hacerse daño|consumo de alcohol o drogas|alucinaciones|conducta violenta|amenaza vigente", dur="L")
G(293, "acude a control con dificultad en sus relaciones interpersonales|refiere impulsividad e inestabilidad emocional|refiere conflictos recurrentes en su familia o trabajo|acude por entrega de medicamento sin cambios|refiere cambios de ánimo y dificultad para controlar la ira",
  "impulsividad|inestabilidad emocional|irritabilidad|ansiedad|insomnio|aislamiento",
  "Refiere seguimiento con psiquiatría o psicología.|Refiere que los problemas son de larga data.|Refiere conflictos familiares.|Refiere dificultad para mantener empleos.",
  "en seguimiento psicológico|en tratamiento farmacológico|con tratamiento irregular|sin tratamiento actual",
  "ideas de hacerse daño|conducta violenta|consumo de drogas|alucinaciones|crisis de agitación", "Y")
G(294, "somnolencia excesiva durante el día|sueño no reparador con cansancio diurno|dificultad para despertar con somnolencia constante|ronquidos fuertes con somnolencia diurna|sueño excesivo con dificultad de concentración",
  "ronquidos|cefalea matutina|fatiga|dificultad de concentración|irritabilidad|pausas respiratorias",
  "Refiere sobrepeso.|Refiere trabajo en turnos.|Refiere pocas horas de sueño.|Refiere uso de medicamentos sedantes.|Refiere que se duerme en actividades cotidianas.",
  "No ha recibido tratamiento.|Tomó café en exceso sin mejoría.",
  "pérdida del conocimiento súbita|pausas respiratorias observadas|ideas de hacerse daño|dolor nocturno|consumo de alcohol", dur="L")
G(295, "pústulas pequeñas centradas en folículos pilosos|lesiones pustulosas con prurito en barba o piernas|pápulas y pústulas foliculares tras el afeitado|pústulas dolorosas en muslos o glúteos|brotes de pústulas en pelo del tórax o espalda",
  "prurito|dolor leve|eritema folicular|costras pequeñas|sensación de ardor",
  "Refiere afeitado reciente.|Refiere uso de ropa ajustada.|Refiere sudoración abundante.|Refiere episodios similares previos.|Refiere uso de piscinas o jacuzzi.",
  "Se aplicó crema antibiótica con alivio parcial.|Se aplicó remedios caseros sin mejoría.|No ha recibido tratamiento.",
  "fiebre|dolor intenso|lesiones extensas|nódulos profundos|diabetes mellitus", dur="B")
G(296, "bulto en dorso de muñeca|masa indolora en muñeca que aumenta con el uso|tumoración firme y móvil sobre un tendón|bulto en mano o pie que aparece y desaparece|abultamiento en muñeca con molestia al hacer fuerza",
  "dolor leve con el esfuerzo|hormigueo en dedos|limitación leve del movimiento|variación del tamaño",
  "Refiere movimientos repetitivos de la mano.|Refiere que el bulto cambia de tamaño.|Refiere trauma previo en la muñeca.|Refiere que ha crecido en los últimos meses.",
  "No ha recibido tratamiento.|Se golpeó el bulto sin éxito.|Se aplicó remedios caseros sin cambios.",
  "dolor intenso|enrojecimiento|fiebre|pérdida de fuerza|crecimiento rápido", dur="L")
G(297, "sangrado rojo brillante escaso al evacuar|sangre en papel higiénico con dolor anal|prurito anal con sangrado ocasional|sensación de masa anal que sale al evacuar|dolor y sangrado anal tras estreñimiento",
  "prurito anal|dolor al evacuar|sensación de masa anal|ardor anal|estreñimiento|manchado de ropa interior",
  "Refiere estreñimiento crónico.|Refiere esfuerzo excesivo al evacuar.|Refiere dieta baja en fibra.|Refiere embarazo o parto reciente.|Refiere estar sentada/o muchas horas.",
  "Realizó baños de asiento con alivio parcial.|Se aplicó pomadas con alivio parcial.|No ha recibido tratamiento.",
  "sangrado abundante|heces negras|pérdida de peso|cambio persistente del hábito intestinal|fiebre|dolor intenso con masa dura", dur="B")
G(298, "manchas claras y descamativas|máculas hipopigmentadas con descamación fina en tronco|manchas blanquecinas que se acentúan al sol|manchas marrón claro en espalda y cuello|lesiones descamativas con prurito leve",
  "descamación fina|prurito leve|hipopigmentación|sudoración|manchas en hombros",
  "Refiere sudoración abundante.|Refiere clima caluroso y húmedo.|Refiere exposición solar reciente.|Refiere piel grasa.|Refiere episodios similares previos.",
  "Se aplicó crema antimicótica con alivio parcial.|Se aplicó remedios caseros sin cambios.|No ha recibido tratamiento.",
  "dolor|fiebre|lesiones sangrantes|ulceración|pérdida de sensibilidad en las manchas", dur="L")
G(299, "obstrucción nasal progresiva|congestión nasal permanente con pérdida del olfato|respiración bucal con ronquidos|rinorrea y obstrucción nasal bilateral crónica|nariz tapada con disminución del olfato",
  "hiposmia|rinorrea|ronquidos|goteo posterior|cefalea frontal|respiración bucal",
  "Refiere antecedente de rinitis alérgica.|Refiere asma.|Refiere uso crónico de descongestionantes.|Refiere infecciones nasales repetidas.",
  "No ha recibido tratamiento.|Utilizó descongestionantes sin mejoría.|Usó antihistamínicos con alivio parcial.",
  "sangrado nasal|dolor facial intenso|fiebre|alteración visual|deformidad nasal", dur="L")
G(300, "dolor en el pecho|dolor torácico punzante que aumenta al respirar|dolor torácico opresivo de pocos minutos|dolor en región anterior del tórax tras esfuerzo|dolor torácico con sensación de ardor",
  "disnea|palpitaciones|sudoración|dolor al respirar profundo|dolor a la palpación|ardor retroesternal",
  "Refiere esfuerzo físico previo.|Refiere tos reciente.|Refiere estrés o ansiedad.|Refiere antecedente de reflujo.|Refiere antecedente de hipertensión o diabetes.",
  TXA, "dolor irradiado a brazo o mandíbula|sudoración fría|síncope|disnea importante|palpitaciones sostenidas|antecedente de cardiopatía", dur="H")
G(301, "dolor agudo|dolor agudo de inicio súbito|dolor intenso localizado|dolor punzante que limita sus actividades|dolor agudo con irradiación",
  "irradiación del dolor|limitación de actividades|náuseas|sudoración|edema local",
  "Refiere que el dolor inició después de un esfuerzo.|Refiere que el dolor inició de forma súbita.|Refiere que no tuvo trauma.|Refiere episodios similares previos.",
  TXA, "fiebre|trauma reciente|pérdida del conocimiento|déficit neurológico|sangrado|vómitos persistentes", dur="H")
G(302, "dolor muscular en espalda y piernas|mialgias tras esfuerzo físico|dolor muscular generalizado|dolor y sensibilidad en músculos|dolor muscular con fatiga",
  "fatiga|rigidez|sensibilidad muscular|calambres|malestar general",
  "Refiere esfuerzo físico reciente.|Refiere trabajo físico pesado.|Refiere cuadro viral previo.|Refiere sedentarismo y esfuerzo ocasional.|Refiere poca ingesta de líquidos.",
  TXA + "|Aplicó calor local con alivio parcial.", "orina oscura|debilidad intensa|fiebre alta|inflamación de articulaciones|trauma reciente", dur="A")
G(303, "dolor en muslo posterior|dolor muscular tras estiramiento brusco|dolor y molestia al caminar tras distensión muscular|dolor en pantorrilla tras ejercicio|dolor muscular localizado con edema leve",
  "edema leve|equimosis|dolor al estirar|dolor al contraer|sensación de tirón",
  "Refiere actividad deportiva reciente.|Refiere que sintió un tirón.|Refiere que no calentó antes del ejercicio.|Refiere esfuerzo físico.",
  "Se aplicó hielo con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|imposibilidad para caminar|fiebre|parestesias|edema marcado", dur="A")
G(304, "malestar general|sensación de enfermedad sin síntomas específicos|cansancio y decaimiento generalizados|malestar corporal con hiporexia|sensación de estar enfermo con astenia",
  "astenia|hiporexia|decaimiento|cefalea leve|dolor corporal|escalofríos",
  "Refiere cuadro gripal previo.|Refiere estrés reciente.|Refiere pocas horas de sueño.|Refiere cambios recientes en su rutina.",
  TXN, "fiebre alta|dolor torácico|dificultad respiratoria|vómitos persistentes|pérdida de peso", dur="A")
G(305, "acné leve en cara y espalda|lesiones de acné con prurito en cara|comedones y pápulas en frente y mejillas|cambios propios de la adolescencia con acné|brotes de acné de forma cíclica",
  "comedones|pápulas|piel grasa|prurito leve|cicatrices|aumento de vello",
  "Refiere cambios hormonales propios de la adolescencia.|Refiere piel grasa.|Refiere que se manipula las lesiones.|Refiere antecedente familiar de acné.|Refiere ciclos menstruales irregulares.",
  "Se aplicó cremas sin receta sin mejoría.|Utilizó remedios caseros.|No ha recibido tratamiento.",
  "fiebre|lesiones dolorosas profundas|cicatrices extensas|ideas de hacerse daño|dolor intenso", dur="L")
G(306, "solicita orientación sobre hábitos de vida saludable|desea orientación sobre alimentación y actividad física|acude para chequeo de salud sin molestias|solicita consejería nutricional y de ejercicio|desea mejorar sus hábitos de salud",
  "preocupación por su peso|sedentarismo|alimentación desordenada|estrés|poco descanso",
  "Refiere que desea bajar de peso.|Refiere sedentarismo.|Refiere antecedente familiar de enfermedades crónicas.|Refiere que no tiene molestias actuales.",
  "No ha recibido tratamiento.|Recibió orientación previa.",
  "dolor torácico|disnea|pérdida de peso|fiebre|síntomas persistentes", dur="-")
G(307, "solicita valoración médica general|acude para chequeo médico sin síntomas|solicita revisión y orientación de salud|desea revisión clínica de rutina|acude por control de salud general",
  "buen estado general|sin molestias|dudas sobre su salud|preocupación por su salud",
  "Refiere que no ha tenido controles recientes.|Refiere antecedente familiar de enfermedades crónicas.|Refiere que desea un chequeo de rutina.|Refiere que no toma medicamentos.",
  "No ha recibido tratamiento.|Trae exámenes previos.",
  "fiebre|dolor|pérdida de peso|disnea|síntomas urinarios o digestivos", dur="-")
