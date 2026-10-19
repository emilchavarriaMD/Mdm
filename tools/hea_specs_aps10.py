from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer.|Refiere que acude a entrega de medicamentos y control."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte|en espera de tratamiento"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"

G(165, "acude a control con dificultad para tragar|refiere disfagia progresiva y pérdida de peso|acude por entrega de medicamento con dolor al deglutir|refiere regurgitación y hiporexia|refiere dolor retroesternal al tragar",
  "disfagia|pérdida de peso|odinofagia|regurgitación|dolor retroesternal|hiporexia",
  ONC, ONCTX, ONCN, "Y")
G(166, "acude a control con dolor y distensión abdominal|refiere dolor pélvico y aumento del perímetro abdominal|acude por entrega de medicamento sin molestias nuevas|refiere náuseas, saciedad temprana y fatiga|refiere dolor pélvico persistente",
  "distensión abdominal|dolor pélvico|saciedad temprana|náuseas|fatiga|pérdida de peso|estreñimiento",
  ONC, ONCTX, ONCN, "Y")
G(167, "acude a control con dolor abdominal y pérdida de peso|refiere dolor epigástrico irradiado a espalda|refiere hiporexia, náuseas y debilidad|acude por manejo paliativo del dolor|refiere ictericia y prurito",
  "dolor epigástrico|dolor irradiado a la espalda|ictericia|prurito|pérdida de peso|hiporexia|heces claras",
  ONC, ONCTX, ONCN, "Y")
G(168, "acude a control sin dolor torácico reciente|refiere dolor torácico opresivo ocasional con el esfuerzo|acude por entrega de medicamento sin molestias|refiere disnea al caminar|refiere fatiga y palpitaciones",
  "disnea de esfuerzo|palpitaciones|fatiga|dolor torácico|mareo|edema de tobillos",
  "Refiere antecedente de infarto previo.|Refiere hipertensión o diabetes asociadas.|Refiere tabaquismo previo.|Refiere buena adherencia al tratamiento.|Refiere control con cardiología.",
  "en tratamiento con ácido acetilsalicílico y estatina|en tratamiento con betabloqueador|en tratamiento con inhibidor de la enzima convertidora|con tratamiento irregular",
  "dolor torácico en reposo|síncope|disnea importante|sudoración profusa|palpitaciones sostenidas|edema de piernas", "Y")
G(169, "visión borrosa progresiva|disminución de la agudeza visual con deslumbramiento|visión nublada como a través de un vidrio|dificultad para leer y conducir de noche|halos alrededor de las luces",
  "deslumbramiento|halos alrededor de luces|cambio frecuente de lentes|dificultad nocturna|visión doble con un ojo",
  "Refiere que la visión ha empeorado en el último año.|Refiere diabetes mellitus.|Refiere antecedente familiar de cataratas.|Refiere exposición solar prolongada.|Refiere uso de corticoides.",
  "No ha recibido tratamiento.|Usa lentes sin mejoría.|Se realizó valoración oftalmológica previa.",
  "dolor ocular intenso|pérdida súbita de la visión|ojo rojo|trauma ocular|náuseas con dolor ocular", dur="L")
G(170, "solicita anticoncepción de emergencia tras relación sexual sin protección|solicita pastilla de emergencia por falla del preservativo|acude por relación sexual reciente sin método anticonceptivo|solicita anticoncepción de emergencia tras olvido de pastillas|acude con temor de embarazo tras relación sexual de hace pocas horas",
  "ansiedad por posible embarazo|ciclos regulares|falla de método de barrera",
  "Refiere que la relación fue hace menos de 72 horas.|Refiere ruptura del preservativo.|Refiere olvido de dos o más pastillas.|Refiere última menstruación hace 2 semanas.|Refiere que no usa método anticonceptivo.",
  "No ha recibido tratamiento.|No ha tomado anticoncepción de emergencia previamente.",
  "embarazo conocido|sangrado vaginal|dolor pélvico|violencia sexual|alergias a medicamentos", dur="-")
G(171, "desea colocación de dispositivo intrauterino|solicita información sobre el DIU|acude para inserción de dispositivo intrauterino con prueba de embarazo negativa|desea método anticonceptivo de larga duración|acude a valoración para colocación de DIU",
  "ciclos regulares|deseo de método de larga duración|dismenorrea|menstruaciones abundantes",
  "Refiere que ya recibió consejería.|Refiere uso previo de otros métodos.|Refiere partos previos.|Refiere que la prueba de embarazo fue negativa.|Refiere ciclos regulares.",
  "No ha recibido tratamiento.|Recibió consejería previa.",
  "embarazo conocido|sangrado anormal|flujo anormal|dolor pélvico|fiebre|infección pélvica previa", dur="-")
G(172, "preocupación por posible embarazo|temor de estar embarazada por retraso menstrual|inquietud por embarazo tras relación sexual sin protección|solicita prueba de embarazo por temor|ansiedad por posible gestación",
  "retraso menstrual|náuseas|sensibilidad mamaria|ansiedad|insomnio",
  "Refiere relaciones sexuales sin protección.|Refiere fecha de última menstruación hace varias semanas.|Refiere uso irregular de anticonceptivos.|Refiere prueba casera previa.|Refiere que no desea embarazo en este momento.",
  "No ha recibido tratamiento.|Se realizó prueba casera.",
  "sangrado vaginal|dolor pélvico intenso|fiebre|síncope|ideas de hacerse daño", dur="-")
G(173, "escoliosis conocida con dolor de espalda|asimetría de hombros notada por familiares|desviación de la columna con molestia lumbar|acude a control de escoliosis sin cambios|dolor de espalda con asimetría de la espalda",
  "asimetría de hombros|dolor lumbar|fatiga postural|prominencia de escápula|rigidez",
  "Refiere que la desviación fue notada en la adolescencia.|Refiere control con ortopedia.|Refiere antecedente familiar de escoliosis.|Refiere que la molestia empeora al estar de pie.",
  "en seguimiento con ortopedia|en ejercicios posturales|sin tratamiento actual",
  "debilidad de miembros inferiores|dificultad respiratoria|pérdida de control de esfínteres|dolor nocturno intenso|progresión rápida de la curvatura", dur="Y")
G(174, "fiebre alta con cefalea y dolor retroocular|fiebre con dolor muscular y articular intenso|fiebre y erupción cutánea con malestar general|fiebre de varios días con náuseas y astenia|fiebre con cefalea y dolor de espalda",
  "cefalea intensa|dolor retroocular|mialgias|artralgias|erupción|náuseas|astenia",
  "Refiere que vive en zona con casos de dengue.|Refiere picaduras de zancudos.|Refiere vecinos con cuadro similar.|Refiere acumulación de agua en su domicilio.",
  "Tomó acetaminofén con alivio parcial.|Tomó ibuprofeno antes de consultar.|No ha recibido tratamiento.",
  "sangrado de encías o nariz|dolor abdominal intenso|vómitos persistentes|petequias|somnolencia|disminución de la diuresis", dur="A")
G(175, "pérdida de peso con hiporexia|bajo peso con poco apetito y decaimiento|disminución del peso con infecciones frecuentes|delgadez marcada con escasa ingesta de alimentos|falta de aumento de peso con irritabilidad",
  "hiporexia|decaimiento|infecciones frecuentes|irritabilidad|caída del cabello|edema leve",
  "Según refiere la madre, come muy poco.|La madre refiere dieta poco variada.|La madre refiere diarreas recurrentes.|La madre refiere dificultades económicas para la alimentación.",
  "No ha recibido tratamiento.|La madre le da multivitamínicos sin cambios.",
  "edema generalizado|diarrea persistente|fiebre|vómitos|dificultad respiratoria|somnolencia", dur="L")
G(176, "embarazo de {w} semanas con pérdida de peso e hiporexia|embarazo de {w} semanas con poca ganancia de peso|embarazo de {w} semanas con vómitos frecuentes y baja ingesta|embarazo de {w} semanas con debilidad y mareo por mala alimentación|embarazo de {w} semanas con peso materno bajo",
  "hiporexia|debilidad|mareo|náuseas|fatiga|palidez",
  "Refiere ingesta insuficiente de alimentos.|Refiere dificultades económicas para alimentarse.|Refiere náuseas y vómitos desde el inicio del embarazo.|Refiere controles prenatales irregulares.",
  "Toma ácido fólico y sulfato ferroso.|No ha recibido suplementos.",
  "sangrado vaginal|pérdida de líquido|cefalea intensa|contracciones|disminución de movimientos fetales", dur="S")
G(177, "disminución progresiva de la visión en ambos ojos|pérdida de la visión periférica|visión borrosa con dificultad para reconocer rostros|dificultad creciente para leer y caminar sin ayuda|ceguera parcial con dificultad para sus actividades",
  "visión de túnel|deslumbramiento|dificultad para leer|desorientación|accidentes por no ver obstáculos",
  "Refiere diabetes mellitus o hipertensión.|Refiere antecedente de trauma ocular.|Refiere antecedente familiar de glaucoma.|Refiere que la visión ha empeorado progresivamente.",
  "No ha recibido tratamiento.|Usa lentes sin mejoría.",
  "dolor ocular intenso|pérdida súbita total|cefalea intensa|náuseas con dolor ocular|trauma ocular", dur="L")
G(178, "disminución del deseo sexual|dificultad para mantener la erección|dolor durante las relaciones sexuales|disfunción sexual con repercusión en la pareja|disminución de la satisfacción sexual",
  "ansiedad|sequedad vaginal|dificultad con la pareja|fatiga|disminución de la libido",
  "Refiere que el problema empezó hace varios meses.|Refiere problemas de pareja.|Refiere estrés o ansiedad.|Refiere inicio de medicamentos nuevos.",
  "No ha recibido tratamiento.|Utilizó lubricantes con alivio parcial.",
  "sangrado con las relaciones|flujo anormal|fiebre|dolor pélvico intenso|violencia sexual", dur="L")
G(179, "dolor y edema en el tobillo tras una torcedura|dolor en tobillo con dificultad para apoyar el pie|inflamación de tobillo tras un mal paso|dolor lateral de tobillo con equimosis|dolor al caminar posterior a esguince",
  "edema local|equimosis|dolor a la palpación|sensación de inestabilidad|limitación al apoyo",
  "Refiere que se torció el pie jugando.|Refiere que se torció el pie al bajar un escalón.|Refiere esguinces previos.|Refiere que usaba calzado inadecuado.",
  "Se aplicó hielo con alivio parcial.|Se vendó el tobillo con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|incapacidad total para apoyar|parestesias|herida abierta|dolor óseo intenso", dur="A")
G(180, "acude a control con debilidad muscular progresiva|refiere dificultad para caminar y subir escaleras|refiere caídas frecuentes por debilidad|acude a control con limitación funcional|refiere dificultad para levantarse del suelo",
  "debilidad proximal|caídas frecuentes|fatiga|dificultad respiratoria leve|contracturas|marcha en puntillas",
  "Refiere diagnóstico desde la infancia.|Refiere seguimiento con neurología.|Refiere que la debilidad ha progresado.|Refiere uso de silla de ruedas o apoyo.",
  "en seguimiento multidisciplinario|en fisioterapia|sin tratamiento actual",
  "dificultad respiratoria|fiebre|disfagia|dolor torácico|palpitaciones", "Y")
G(181, "acude a control con dolor quemante persistente|refiere dolor tipo descarga eléctrica en una extremidad|refiere dolor neuropático con hormigueo y alodinia|acude por entrega de medicamento con dolor controlado parcialmente|refiere dolor que interrumpe el sueño",
  "alodinia|hormigueo|ardor|descargas eléctricas|insomnio|ansiedad",
  "Refiere dolor desde hace años.|Refiere antecedente de neuropatía.|Refiere que el dolor empeora por la noche.|Refiere olvido ocasional del medicamento.",
  "en tratamiento con gabapentina|en tratamiento con pregabalina|en tratamiento con amitriptilina|con tratamiento irregular",
  "debilidad nueva|pérdida de control de esfínteres|fiebre|ideas de hacerse daño|lesiones en piel", "Y")
G(182, "dolor pélvico tipo cólico|dolor en hipogastrio recurrente asociado a la menstruación|dolor pélvico crónico con exacerbaciones|dolor pélvico con irradiación a región lumbar|dolor en bajo vientre de predominio premenstrual",
  "dismenorrea|dispareunia|distensión abdominal|lumbalgia|náuseas|flujo vaginal leve",
  "Refiere ciclos menstruales regulares.|Refiere que el dolor empeora con la menstruación.|Refiere antecedente de infecciones pélvicas.|Refiere antecedente de quistes ováricos.",
  TXA, "fiebre|sangrado vaginal anormal|retraso menstrual|dolor súbito muy intenso|flujo con mal olor|vómitos", dur="B")
G(183, "embarazo de {w} semanas con crisis convulsiva|embarazo de {w} semanas con convulsiones y cefalea previa|embarazo de {w} semanas con convulsiones tónico-clónicas y presión elevada|embarazo de {w} semanas con convulsión y pérdida del conocimiento|embarazo de {w} semanas con convulsión posterior a epigastralgia",
  "cefalea intensa|visión borrosa|epigastralgia|edema|presión arterial elevada|somnolencia postcrisis",
  "Refiere antecedente de preeclampsia o hipertensión.|Refiere que la crisis fue presenciada por familiares.|Refiere controles prenatales irregulares.|Es primigesta.",
  "No ha recibido tratamiento.|Recibió atención previa de emergencia.",
  "fiebre|sangrado vaginal|pérdida de líquido|trauma abdominal|antecedente de epilepsia", dur="30 semanas|32 semanas|34 semanas|36 semanas|38 semanas")
G(184, "hinchazón en ambos tobillos|edema de miembros inferiores que aumenta al final del día|pies hinchados con sensación de pesadez|edema que deja fóvea en piernas|hinchazón de tobillos que mejora con el reposo",
  "pesadez de piernas|aumento de peso|disnea de esfuerzo|ortopnea|várices|nicturia",
  "Refiere permanecer muchas horas de pie.|Refiere consumo elevado de sal.|Refiere antecedente de hipertensión o enfermedad renal.|Refiere uso de medicamentos antihipertensivos.|Refiere calor intenso.",
  "Elevó las piernas con alivio parcial.|No ha recibido tratamiento.|Usa medias de compresión con alivio leve.",
  "disnea importante|dolor torácico|dolor unilateral de pantorrilla|orina espumosa|disminución de la orina|fiebre", dur="B")
G(185, "embarazo de {w} semanas con edema en piernas y pies|embarazo de {w} semanas con hinchazón de manos y tobillos|embarazo de {w} semanas con edema vespertino sin otras molestias|embarazo de {w} semanas con pesadez de miembros inferiores|embarazo de {w} semanas con edema que mejora con el reposo",
  "pesadez de piernas|várices|calambres|edema de manos|aumento de peso",
  "Refiere que su presión arterial ha sido normal.|Refiere permanecer muchas horas de pie.|Refiere calor intenso.|Refiere controles prenatales adecuados.",
  "Elevó las piernas con alivio parcial.|No ha recibido tratamiento.",
  "cefalea|visión borrosa|presión arterial elevada|dolor en epigastrio|disminución de movimientos fetales|edema facial", dur="26 semanas|28 semanas|30 semanas|32 semanas|34 semanas|36 semanas|38 semanas")
