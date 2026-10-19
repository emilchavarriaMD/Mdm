from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
RES = "Refiere contacto con personas con cuadro respiratorio.|Refiere cambios bruscos de temperatura en los últimos días.|Refiere exposición a polvo o humo.|Refiere asistencia a escuela o trabajo con casos similares."

G(83, "masa palpable en mama detectada al autoexamen|nódulo mamario indoloro de crecimiento lento|masa en mama de consistencia firme y bordes definidos|aumento de volumen localizado en mama con molestia leve|nódulo en cuadrante superior externo de mama",
  "dolor mamario leve|secreción por el pezón|cambios en la piel de la mama|retracción del pezón|adenopatía axilar|variación con el ciclo menstrual",
  "Refiere antecedente familiar de cáncer de mama.|Refiere que nunca se ha realizado mamografía.|Refiere que el nódulo no varía con la menstruación.|Refiere que lo notó durante el baño.|Refiere antecedente de lactancia prolongada.",
  "No ha recibido tratamiento.|No se ha realizado estudios previos.|Se realizó ultrasonido previo.",
  "pérdida de peso|fiebre|dolor óseo|ulceración de la piel|secreción sanguinolenta por el pezón", dur="B")
G(84, "dolor en ambas mamas de predominio premenstrual|sensibilidad y pesadez mamaria bilateral|dolor mamario cíclico que se alivia con la menstruación|dolor en mama con irradiación a axila|mastalgia con aumento de volumen mamario leve",
  "pesadez mamaria|sensibilidad al roce|aumento de volumen mamario|irritabilidad|distensión abdominal|cefalea",
  "Refiere que el dolor se presenta días antes de la menstruación.|Refiere consumo frecuente de café.|Refiere uso de sostén inadecuado.|Refiere uso de anticonceptivos hormonales.|Refiere estrés reciente.",
  "Se aplicó compresas calientes con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "nódulo palpable|secreción por el pezón|fiebre|cambios en la piel|enrojecimiento mamario", dur="L")
G(85, "menstruaciones abundantes con coágulos y duración prolongada|sangrado menstrual abundante e irregular|ciclos menstruales irregulares con sangrado profuso|menstruación de más de 8 días con uso de múltiples compresas|sangrado menstrual abundante con mareo y fatiga",
  "coágulos|dismenorrea|mareo|fatiga|palidez|dolor pélvico|cefalea",
  "Refiere ciclos irregulares desde hace meses.|Refiere uso de más de 6 compresas al día.|Refiere antecedente de anemia.|Refiere antecedente familiar de miomas.|Refiere uso de anticonceptivos.",
  "No ha recibido tratamiento.|Tomó antiinflamatorios con alivio parcial.|Tomó hierro de forma irregular.",
  "fiebre|dolor abdominal intenso|embarazo conocido|sangrado entre ciclos|pérdida de peso", dur="L")
G(86, "ciclos menstruales irregulares de longitud variable|menstruaciones que llegan cada 20 a 60 días|ciclos impredecibles con sangrado de intensidad variable|retrasos menstruales frecuentes con sangrado escaso|sangrado menstrual irregular sin patrón definido",
  "retrasos menstruales|sangrado escaso|sangrado abundante|acné|aumento de vello facial|aumento de peso|dolor pélvico leve",
  "Refiere ciclos irregulares desde la adolescencia.|Refiere cambios recientes de peso.|Refiere estrés o cambios de rutina.|Refiere uso previo de anticonceptivos.|Refiere antecedente familiar de ovario poliquístico.",
  "No ha recibido tratamiento.|Tomó anticonceptivos sin continuidad.|Utilizó remedios caseros sin mejoría.",
  "dolor pélvico intenso|fiebre|embarazo conocido|flujo anormal|pérdida de peso", dur="L")
G(87, "ausencia de menstruación de varias semanas|retraso menstrual de más de 2 ciclos|amenorrea con náuseas matutinas y sensibilidad mamaria|falta de menstruación desde su último ciclo|ausencia de menstruación con aumento de peso",
  "náuseas matutinas|sensibilidad mamaria|aumento de peso|acné|cefalea|fatiga|bochornos",
  "Refiere última menstruación hace más de 2 meses.|Refiere vida sexual activa sin protección.|Refiere uso previo de anticonceptivos.|Refiere estrés reciente.|Refiere cambios recientes de peso.",
  "No ha recibido tratamiento.|Se realizó prueba de embarazo en casa.|Tomó remedios caseros para provocar menstruación.",
  "dolor pélvico|sangrado vaginal|fiebre|salida de leche por el pezón|alteraciones visuales", dur="L")
G(88, "dolores musculares generalizados|mialgias de predominio en espalda y piernas|dolor muscular con sensación de cuerpo cortado|dolor muscular tras esfuerzo físico|dolor y sensibilidad muscular difuso",
  "malestar general|fatiga|cefalea|escalofríos|rigidez|dolor al movimiento",
  "Refiere esfuerzo físico inusual.|Refiere cuadro gripal reciente.|Refiere trabajo físico pesado.|Refiere inicio de medicamentos nuevos.|Refiere poca ingesta de líquidos.",
  TXA, "orina oscura|debilidad intensa|fiebre alta|inflamación de las articulaciones|trauma reciente|erupción", dur="A")
G(89, "acude a control sin crisis recientes|refiere cefalea pulsátil hemicraneal con náuseas y fotofobia|refiere episodios de cefalea migrañosa de 2 a 3 veces al mes|acude a control con aumento de la frecuencia de las crisis|refiere aura visual antes de la cefalea",
  "náuseas|fotofobia|fonofobia|vómitos|aura visual|cefalea hemicraneal|mareo",
  "Refiere que las crisis se desencadenan por estrés o falta de sueño.|Refiere antecedente familiar de migraña.|Refiere que las crisis coinciden con la menstruación.|Refiere ayunos o consumo de café como desencadenante.",
  "en tratamiento con acetaminofén en crisis|en tratamiento con ibuprofeno en crisis|en tratamiento con propranolol profiláctico|con tratamiento irregular",
  "déficit neurológico|fiebre|rigidez de cuello|cefalea súbita muy intensa|trauma craneal", dur="Y")
G(90, "tos productiva con expectoración purulenta|fiebre alta con escalofríos y dolor torácico al respirar|disnea con tos y esputo amarillo-verdoso|tos, fiebre y dificultad respiratoria progresiva|dolor torácico pleurítico con tos y malestar general",
  "fiebre alta|escalofríos|dolor pleurítico|disnea|esputo purulento|astenia|hiporexia",
  RES, TXB, "esputo con sangre|cianosis|confusión|rechazo de alimentos|dolor abdominal|vómitos persistentes", dur="A")
G(91, "náuseas persistentes con intolerancia a algunos alimentos|náuseas matutinas con sensación de llenura|náuseas con sialorrea y hiporexia|náuseas postprandiales sin vómitos|sensación nauseosa constante con malestar epigástrico",
  "hiporexia|sialorrea|distensión abdominal|epigastralgia|mareo|cefalea",
  "Refiere ingesta de alimentos grasosos.|Refiere estrés reciente.|Refiere inicio de un medicamento nuevo.|Refiere retraso menstrual.|Refiere ayunos prolongados.",
  TXN, "vómitos persistentes|dolor abdominal intenso|fiebre|pérdida de peso|diarrea|sangre en vómito", dur="A")
G(92, "vómitos de contenido alimentario|vómitos repetidos con náuseas y malestar general|vómitos de varias veces al día con intolerancia a la vía oral|vómitos postprandiales con dolor epigástrico|vómitos con cefalea y decaimiento",
  "náuseas|dolor abdominal|sed|decaimiento|intolerancia a líquidos|diarrea|fiebre baja",
  "Refiere ingesta reciente de alimentos en mal estado.|Refiere contacto con personas con cuadro similar.|Refiere ingesta de abundante alcohol o grasas.|Refiere retraso menstrual.",
  "Ha tomado suero oral con alivio parcial.|Tomó antiheméticos sin mejoría.|No ha recibido tratamiento.",
  "sangre en vómito|vómitos en proyectil|dolor abdominal intenso|fiebre alta|signos de deshidratación|cefalea intensa", dur="A")
G(93, "enrojecimiento alrededor del ombligo|secreción de mal olor en el muñón umbilical|eritema periumbilical con secreción purulenta|ombligo húmedo y enrojecido con secreción|muñón umbilical con enrojecimiento y supuración",
  "secreción purulenta|mal olor|edema periumbilical|irritabilidad|rechazo parcial de las tomas|fiebre",
  "La madre refiere que el muñón aún no ha caído.|La madre refiere que lo cura con alcohol o remedios caseros.|La madre refiere que nació por cesárea.|La madre refiere parto atendido en casa.",
  "La madre aplicó alcohol con poca mejoría.|La madre aplicó remedios caseros en el ombligo.|No ha recibido tratamiento.",
  "fiebre alta|rechazo total de las tomas|somnolencia|extensión del enrojecimiento al abdomen|convulsiones|decaimiento marcado", dur="D", u="días")
G(94, "dolor en cara anterior de rodilla al subir escaleras|dolor retropatelar al flexionar la rodilla|dolor en rodilla tras permanecer sentado mucho tiempo|crepitación y dolor anterior de rodilla|dolor de rodilla que aumenta al agacharse",
  "crepitaciones|sensación de fallo|dolor al subir escaleras|rigidez tras estar sentado|edema leve|chasquidos",
  "Refiere actividad deportiva frecuente.|Refiere sobrepeso.|Refiere trabajo que requiere flexión repetida.|Refiere trauma previo en la rodilla.",
  TXA + "|Utiliza rodillera con alivio parcial.", "bloqueo articular|fiebre|edema importante|inestabilidad franca|trauma agudo", dur="B")
G(95, "dolor en un oído de intensidad moderada|otalgia con sensación de oído tapado|dolor de oído que empeora por la noche|dolor ótico con hipoacusia leve|dolor en oído irradiado a mandíbula",
  "hipoacusia|sensación de plenitud ótica|acúfenos|cefalea|dolor al masticar|fiebre baja",
  "Refiere cuadro gripal previo.|Refiere exposición a agua en piscina o baño.|Refiere uso de hisopos en el oído.|Refiere dolor dental o de garganta asociado.",
  TXA, "secreción por el oído|fiebre alta|vértigo|parálisis facial|edema detrás de la oreja|trauma ótico", dur="A")
G(96, "dolor en un oído con prurito en el conducto|otalgia que aumenta al tocar la oreja|dolor ótico con secreción y sensación de oído tapado|dolor que aumenta al mover el pabellón auricular|ardor y prurito ótico tras entrar al agua",
  "prurito ótico|secreción serosa|hipoacusia leve|sensación de plenitud|edema del conducto|dolor al masticar",
  "Refiere que estuvo en piscina o río recientemente.|Refiere uso frecuente de hisopos.|Refiere uso de audífonos.|Refiere episodios similares previos.",
  "Se aplicó gotas caseras sin mejoría.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "fiebre|hipoacusia marcada|vértigo|trauma ótico|edema retroauricular|diabetes mellitus", dur="A")
G(97, "otalgia intensa con fiebre|dolor de oído con hipoacusia y sensación de plenitud|otalgia que inició después de un cuadro gripal|dolor ótico con irritabilidad y fiebre|salida de secreción por el oído con alivio del dolor|dolor de oído nocturno con fiebre",
  "fiebre|hipoacusia|irritabilidad|secreción ótica|congestión nasal|rechazo de alimentos|llanto nocturno",
  "Refiere cuadro gripal previo.|Refiere episodios previos de otitis.|Refiere asistencia a guardería o escuela.|La madre refiere que el niño se lleva la mano al oído.",
  TXB, "parálisis facial|edema retroauricular|vértigo|fiebre alta persistente|rigidez de cuello|vómitos persistentes", dur="A")
G(98, "dolor en varias articulaciones|dolor articular de manos, rodillas y pies|dolor migratorio en articulaciones|dolor poliarticular con rigidez|artralgias con edema leve en articulaciones",
  "rigidez matutina|edema articular|fatiga|fiebre baja|limitación del movimiento|calor local",
  "Refiere que el dolor empeora con el frío.|Refiere cuadro viral previo.|Refiere trabajo con esfuerzo físico.|Refiere antecedente familiar de enfermedades reumáticas.",
  TXA, "fiebre alta|erupción cutánea|ojo rojo|dolor torácico|debilidad muscular|trauma reciente", dur="L")
G(99, "episodio de movimientos tónico-clónicos generalizados|crisis convulsiva con pérdida del conocimiento y mordedura de lengua|convulsión de breve duración con somnolencia posterior|crisis convulsiva con relajación de esfínteres|episodio de rigidez y sacudidas generalizadas",
  "pérdida del conocimiento|mordedura de lengua|relajación de esfínteres|somnolencia postcrisis|confusión|cefalea",
  "Refiere que fue presenciado por familiares.|Refiere fiebre previa.|Refiere desvelo o consumo de alcohol.|Refiere trauma craneal reciente.|Refiere que es el primer episodio.",
  "No ha recibido tratamiento.|Recibió atención de urgencia previa.",
  "fiebre alta|rigidez de cuello|trauma craneal|vómitos persistentes|déficit neurológico|nuevo episodio", dur="H")
G(100, "dolor anal intenso al defecar|dolor anal con sangrado rojo brillante|ardor y prurito anal con evacuaciones dolorosas|aumento de volumen doloroso en región anal|dolor y sensación de masa en el ano",
  "sangrado rojo brillante|prurito anal|dolor al sentarse|aumento de volumen perianal|estreñimiento|sensación de evacuación incompleta",
  "Refiere estreñimiento crónico.|Refiere esfuerzo excesivo al evacuar.|Refiere dieta baja en fibra.|Refiere estar sentado mucho tiempo.|Refiere episodios similares previos.",
  "Se automedicó con pomadas con alivio parcial.|Realizó baños de asiento con alivio parcial.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|pérdida de peso|sangrado abundante|heces negras|cambio persistente del hábito intestinal", dur="B")
G(101, "acude a control sin secreción ótica activa|refiere secreción por el oído de forma intermitente|refiere hipoacusia y otorrea de larga data|acude con otorrea fétida de varios días|refiere episodios recurrentes de secreción ótica",
  "otorrea intermitente|hipoacusia|sensación de plenitud ótica|otalgia ocasional|acúfenos",
  "Refiere perforación timpánica conocida.|Refiere infecciones de oído desde la infancia.|Refiere ingreso de agua en el oído.|Refiere uso de gotas óticas previas.",
  "en seguimiento por otorrinolaringología|con tratamiento tópico intermitente|sin tratamiento actual",
  "fiebre|vértigo|parálisis facial|dolor intenso|edema retroauricular|cefalea intensa", dur="Y")
G(102, "dolor en región dorsal y lumbar|dolor de espalda alta con rigidez|dolor lumbar con limitación para inclinarse|dolor vertebral que empeora al estar sentado mucho tiempo|dolor y rigidez de columna al despertar",
  "rigidez matutina|contractura paravertebral|limitación de movimientos|dolor al cambiar de posición|hormigueo en extremidades",
  "Refiere postura sentada prolongada.|Refiere cargar objetos pesados.|Refiere sedentarismo.|Refiere sobrepeso.|Refiere trauma previo en espalda.",
  TXA + "|Aplicó calor local con alivio parcial.", "fiebre|pérdida de fuerza|pérdida del control de esfínteres|pérdida de peso|dolor nocturno intenso", dur="B")
G(103, "dolor abdominal difuso de intensidad moderada|dolor abdominal tipo cólico con distensión|dolor abdominal con cambios del ritmo de evacuación|dolor abdominal que mejora con la evacuación|dolor abdominal recurrente con flatulencia",
  "distensión abdominal|flatulencia|diarrea|estreñimiento|náuseas|hiporexia|eructos",
  "Refiere ingesta reciente de alimentos irritantes.|Refiere estrés o ansiedad.|Refiere episodios similares previos.|Refiere dieta desordenada.",
  TXA, "fiebre|vómitos persistentes|sangre en heces|pérdida de peso|dolor abdominal intenso súbito|ictericia", dur="B")
G(104, "acude a control endocrinológico sin síntomas nuevos|refiere fatiga, intolerancia al frío y aumento de peso|refiere cefalea y alteraciones visuales leves|refiere cansancio, mareo y disminución del apetito|acude por entrega de medicamento sin molestias",
  "fatiga|intolerancia al frío|aumento de peso|cefalea|alteraciones visuales|disminución del deseo sexual|hipotensión",
  "Refiere control con endocrinología.|Refiere que sus exámenes hormonales estuvieron alterados.|Refiere que dejó el medicamento en varias ocasiones.|Refiere cirugía hipofisaria previa.",
  "en tratamiento hormonal sustitutivo|con tratamiento irregular|en seguimiento especializado",
  "cefalea intensa|pérdida de la visión|vómitos|convulsiones|mareo con desmayo|fiebre", dur="Y")
