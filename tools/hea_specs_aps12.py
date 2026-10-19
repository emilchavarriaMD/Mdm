from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer.|Refiere que acude a entrega de medicamentos y control."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte|en espera de tratamiento"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"
CRON = "Refiere buena adherencia al tratamiento.|Refiere que ha omitido dosis del medicamento.|Refiere control con especialista.|Refiere que sus últimos exámenes fueron estables."

G(208, "lesiones con costras color miel|costras amarillentas sobre lesiones en la piel|lesiones superficiales con secreción y costras melicéricas|erupción con costras en cara o extremidades|ampollas rotas con costras amarillentas",
  "prurito|ardor|secreción serosa|adenopatías regionales|lesiones por rascado|fiebre baja",
  "Refiere lesión previa por picadura o rascado.|Refiere contacto con personas con lesiones similares.|Refiere asistencia a escuela o guardería con casos similares.|Refiere dermatitis previa.",
  "Se aplicó pomada antibiótica con alivio parcial.|Se aplicó remedios caseros sin mejoría.|No ha recibido tratamiento.",
  "fiebre alta|dolor intenso|lesiones extensas|edema facial|orina oscura|compromiso del estado general", dur="A")
G(209, "escape de orina al toser, reír o estornudar|pérdida involuntaria de orina con el esfuerzo|goteo de orina al levantar peso|escape de orina al hacer ejercicio|humedad en la ropa interior tras esfuerzos",
  "uso de toallas protectoras|escape al subir escaleras|urgencia leve|sensación de vergüenza|limitación de actividades",
  "Refiere múltiples partos vaginales.|Refiere menopausia.|Refiere sobrepeso.|Refiere tos crónica.|Refiere cirugía pélvica previa.",
  "No ha recibido tratamiento.|Realizó ejercicios de Kegel con alivio parcial.",
  "dolor al orinar|sangre en la orina|fiebre|incontinencia fecal|retención urinaria", dur="L")
G(210, "lesiones vesiculares dolorosas en región genital|vesículas agrupadas en genitales con ardor|úlceras superficiales dolorosas en zona genital o anal|ardor y hormigueo genital seguidos de vesículas|lesiones dolorosas en genitales con adenopatías inguinales",
  "ardor genital|disuria|adenopatías inguinales dolorosas|fiebre baja|malestar general|dolor al roce",
  "Refiere relaciones sexuales sin protección.|Refiere episodios similares previos.|Refiere pareja con lesiones similares.|Refiere estrés reciente.",
  "Se aplicó crema antiséptica sin mejoría.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "fiebre alta|retención urinaria|cefalea intensa|rigidez de cuello|lesiones diseminadas", dur="A")
G(211, "diarrea con moco y sangre|evacuaciones con sangre, fiebre y dolor abdominal|diarrea disentérica con pujo y tenesmo|deposiciones líquidas con moco y estrías de sangre|diarrea con fiebre y cólico abdominal intenso",
  "fiebre|pujo|tenesmo|dolor abdominal tipo cólico|náuseas|vómitos|deshidratación leve",
  "Refiere ingesta de alimentos en la calle.|Refiere consumo de agua no tratada.|Refiere contacto con personas con diarrea.|Refiere ingesta de carnes mal cocidas.",
  "Ha tomado suero oral con alivio parcial.|Se automedicó con antibiótico sin mejoría.|No ha recibido tratamiento.",
  "deshidratación importante|fiebre alta persistente|confusión|dolor abdominal intenso|sangrado abundante", dur="A")
G(212, "dificultad para conciliar el sueño|despertares nocturnos frecuentes con dificultad para volver a dormir|sueño no reparador con somnolencia diurna|despertar temprano con imposibilidad para volver a dormir|insomnio con ansiedad y cansancio diurno",
  "somnolencia diurna|irritabilidad|dificultad para concentrarse|ansiedad|cefalea matutina|cansancio",
  "Refiere estrés laboral o familiar.|Refiere consumo de café en la tarde.|Refiere uso de pantallas antes de dormir.|Refiere preocupaciones económicas.|Refiere trabajo por turnos.",
  "Tomó infusiones relajantes con alivio parcial.|Se automedicó con antihistamínicos sin mejoría.|No ha recibido tratamiento.",
  "ideas de hacerse daño|ronquidos con pausas respiratorias|tristeza persistente|consumo de alcohol|dolor nocturno", dur="L")
G(213, "acude a control con edema y disminución de la orina|refiere astenia, náuseas y prurito|acude por seguimiento sin molestias nuevas|refiere orina espumosa y cansancio|refiere hiporexia y calambres",
  "edema|orina espumosa|náuseas|prurito|astenia|calambres|disminución de la diuresis",
  "Refiere control con nefrología.|Refiere hipertensión o diabetes asociadas.|Refiere que sus exámenes de creatinina están elevados.|Refiere dieta con restricción de sal.",
  "en tratamiento conservador|en hemodiálisis|en tratamiento antihipertensivo|con tratamiento irregular",
  "dificultad respiratoria|dolor torácico|anuria|confusión|vómitos persistentes|fiebre", "Y")
G(214, "dolor en hombro con limitación del movimiento|dolor en hombro tras una caída|dolor en hombro al elevar el brazo|dolor persistente en hombro que impide dormir sobre ese lado|dolor y debilidad del hombro tras esfuerzo",
  "limitación de la elevación|dolor nocturno|chasquidos|debilidad del brazo|rigidez|edema leve",
  "Refiere trauma previo en el hombro.|Refiere movimientos repetitivos por su trabajo.|Refiere actividad deportiva reciente.|Refiere cargar objetos pesados.",
  TXA, "deformidad|fiebre|pérdida de fuerza importante|dolor torácico|parestesias|trauma reciente", dur="B")
G(215, "acude a control con aumento de volumen en una extremidad|refiere edema persistente en brazo o pierna|refiere pesadez y tensión en el miembro afectado|acude con edema que no cede con el reposo|refiere piel engrosada y edema en una extremidad",
  "pesadez del miembro|piel engrosada|dolor leve|limitación del movimiento|infecciones recurrentes|edema asimétrico",
  "Refiere cirugía o radioterapia previa.|Refiere episodios de celulitis.|Refiere uso de medias de compresión.|Refiere aumento de volumen progresivo.",
  "en tratamiento con medias de compresión|en fisioterapia|con tratamiento irregular|sin tratamiento actual",
  "fiebre|enrojecimiento intenso|dolor súbito|úlceras|dificultad respiratoria", "Y")
G(216, "dolor y edema en muñeca tras una torcedura|dolor en muñeca tras caída con apoyo de la mano|dolor y limitación del movimiento en muñeca|inflamación de la muñeca con dolor al sostener objetos|dolor en articulación tras un movimiento forzado",
  "edema local|equimosis|dolor a la movilización|limitación para agarrar|sensación de inestabilidad",
  "Refiere caída apoyando la mano.|Refiere esfuerzo repetitivo.|Refiere torcedura durante deporte.|Refiere que ocurrió hace pocos días.",
  "Se aplicó hielo con alivio parcial.|Se inmovilizó con venda.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|parestesias|incapacidad para mover los dedos|herida abierta|dolor óseo intenso", dur="A")
G(217, "lesiones pequeñas, redondeadas, color piel, con umbilicación|pápulas perladas con depresión central|pápulas firmes y brillantes que se han multiplicado|lesiones cutáneas indoloras de crecimiento lento|pequeñas pápulas umbilicadas en tronco o pliegues",
  "prurito leve|múltiples lesiones|diseminación por rascado|eritema alrededor|lesiones en pliegues",
  "Refiere contacto con personas con lesiones similares.|Refiere asistencia a piscinas o guarderías.|Refiere dermatitis atópica.|Refiere contacto sexual reciente.",
  "No ha recibido tratamiento.|Se aplicó remedios caseros sin cambios.",
  "fiebre|dolor intenso|secreción purulenta|lesiones grandes|compromiso ocular", dur="L")
G(218, "mordedura de animal|herida por mordedura de perro con dolor y sangrado|mordedura de gato con dolor y eritema|mordedura reciente con heridas punzantes|lesión por mordedura con edema local",
  "dolor local|sangrado|edema|eritema|desgarro de piel|temor por rabia",
  "Refiere que fue mordida/o por perro.|Refiere que fue mordida/o por gato.|Refiere que el animal no estaba vacunado.|Refiere que el animal es desconocido.|Refiere que ocurrió hace pocas horas.",
  "Se lavó la herida con agua y jabón.|Se aplicó alcohol o remedios caseros.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|pérdida de movilidad|sangrado profuso|lesiones en cara o cuello|animal con comportamiento extraño", dur="H")
G(219, "acude a control por nódulo mamario benigno conocido|refiere nódulo mamario sin cambios|acude por seguimiento de fibroadenoma|acude con ultrasonido mamario previo|refiere nódulo móvil e indoloro en mama",
  "dolor leve cíclico|nódulo móvil|aumento de tamaño leve|sensibilidad premenstrual",
  "Refiere biopsia previa benigna.|Refiere ultrasonido de seguimiento.|Refiere antecedente familiar de patología mamaria.|Refiere que no ha cambiado de tamaño.",
  "en seguimiento clínico|en vigilancia con ultrasonido|sin tratamiento actual",
  "crecimiento rápido|secreción sanguinolenta por el pezón|cambios en la piel|retracción del pezón|adenopatía axilar", "Y")
G(220, "acude a control con dolor y dificultad para tragar|refiere odinofagia persistente y sensación de masa|refiere cambios en la voz y dolor de oído|acude por entrega de medicamento con dolor controlado|refiere disfagia y pérdida de peso",
  "disfagia|odinofagia|otalgia refleja|cambios en la voz|pérdida de peso|masa cervical",
  ONC, ONCTX, ONCN, "Y")
G(221, "acude a control con flujo vaginal y dolor pélvico|refiere sangrado vaginal anormal|refiere dispareunia y secreción sanguinolenta|acude por entrega de medicamento sin molestias nuevas|refiere dolor pélvico persistente",
  "sangrado vaginal|flujo con mal olor|dispareunia|dolor pélvico|pérdida de peso|molestia al orinar",
  ONC, ONCTX, ONCN, "Y")
G(222, "acude a control con prurito y lesión vulvar|refiere lesión ulcerada o nodular en vulva|refiere dolor y sangrado en la zona vulvar|acude por entrega de medicamento sin molestias nuevas|refiere prurito vulvar persistente",
  "prurito vulvar|lesión ulcerada|sangrado vulvar|dolor local|adenopatías inguinales|secreción",
  ONC, ONCTX, ONCN, "Y")
G(223, "acude a control con dolor y sangrado anal|refiere cambios en el hábito intestinal con sangrado|refiere masa dolorosa en región anal|acude por entrega de medicamento sin molestias nuevas|refiere dolor al evacuar y pérdida de peso",
  "sangrado rectal|dolor anal|tenesmo|cambios en las heces|pérdida de peso|prurito anal",
  ONC, ONCTX, ONCN, "Y")
G(224, "acude a control con flujo vaginal y dolor pélvico|refiere sangrado vaginal postcoital|refiere sangrado vaginal anormal y dolor lumbar|acude por entrega de medicamento sin molestias nuevas|refiere flujo sanguinolento con mal olor",
  "sangrado postcoital|flujo con mal olor|dolor pélvico|dolor lumbar|pérdida de peso|dispareunia",
  ONC + "|Refiere citologías previas alteradas.", ONCTX, ONCN, "Y")
G(225, "acude a control con lesión en pene|refiere lesión ulcerada en glande|refiere secreción y mal olor en la zona genital|acude por entrega de medicamento sin molestias nuevas|refiere dolor y sangrado en pene",
  "lesión ulcerada|secreción maloliente|dolor local|adenopatías inguinales|sangrado|fimosis",
  ONC, ONCTX, ONCN, "Y")
G(226, "movimientos oculares rítmicos|movimientos involuntarios de los ojos con visión borrosa|oscilopsia con mareo|movimientos oculares repetitivos de larga data|mareo con movimientos oculares anormales",
  "visión borrosa|mareo|oscilopsia|inestabilidad|cefalea|estrabismo",
  "Refiere que los movimientos oculares son de larga data.|Refiere trauma craneal previo.|Refiere antecedente familiar de alteraciones oculares.|Refiere uso de medicamentos anticonvulsivantes.",
  "No ha recibido tratamiento.|Se realizó valoración oftalmológica previa.",
  "pérdida de visión|cefalea intensa|déficit neurológico|vómitos|diplopía de inicio súbito", dur="L")
G(227, "acude a control con aumento de peso|refiere aumento progresivo de peso con fatiga|refiere dificultad para bajar de peso|acude con dolor articular y sobrepeso|refiere somnolencia diurna y ronquidos",
  "fatiga|dolor articular|disnea de esfuerzo|ronquidos|hiperfagia|aumento de la circunferencia abdominal",
  "Refiere dieta rica en azúcares y grasas.|Refiere sedentarismo.|Refiere antecedente familiar de obesidad.|Refiere intentos previos fallidos de perder peso.|Refiere diabetes o hipertensión asociadas.",
  "con dieta y ejercicio|en control nutricional|sin tratamiento actual|con tratamiento irregular",
  "dolor torácico|disnea importante|pausas respiratorias durante el sueño|edema de piernas|síncope", "Y")
G(228, "aumento de volumen doloroso en el borde del párpado|nódulo rojo y doloroso en el párpado|bulto con punto amarillo en el borde palpebral|dolor y enrojecimiento localizado del párpado|inflamación dolorosa del párpado con lagrimeo",
  "lagrimeo|sensación de cuerpo extraño|dolor al parpadear|punto purulento|edema palpebral",
  "Refiere episodios previos de orzuelo.|Refiere que se frota los ojos con frecuencia.|Refiere uso de maquillaje.|Refiere blefaritis previa.",
  "Se aplicó compresas tibias con alivio parcial.|Se aplicó gotas oftálmicas sin mejoría.|No ha recibido tratamiento.",
  "disminución de la visión|fiebre|dolor ocular intenso|edema facial|ojo rojo", dur="A")
G(229, "acude a control sin dolor óseo|refiere dolor lumbar y disminución de la talla|acude con densitometría con osteoporosis|refiere dolor óseo difuso|acude por entrega de medicamento sin molestias",
  "dolor lumbar|disminución de la talla|dolor óseo|fracturas previas|cifosis",
  "Refiere menopausia.|Refiere antecedente de fractura.|Refiere antecedente familiar de osteoporosis.|Refiere consumo bajo de calcio.|Refiere tabaquismo.",
  "en tratamiento con calcio y vitamina D|en tratamiento con alendronato|con tratamiento irregular|sin tratamiento actual",
  "fractura reciente|dolor óseo intenso|caída reciente|pérdida de peso|inmovilidad prolongada", "Y")
G(230, "embarazo de {w} semanas con sangrado vaginal|embarazo de {w} semanas con sangrado vaginal escaso y dolor leve|embarazo de {w} semanas con manchado vaginal|embarazo de {w} semanas con sangrado rojo oscuro intermitente|embarazo de {w} semanas con sangrado vaginal tras relación sexual",
  "dolor pélvico leve|manchado|cólicos leves|dolor lumbar|mareo",
  "Refiere antecedente de abortos previos.|Refiere embarazo confirmado por prueba.|Refiere relaciones sexuales recientes.|Refiere esfuerzo físico previo.|Es primigesta.",
  "Se le recomendó reposo.|No ha recibido tratamiento.|Acude a primera valoración.",
  "fiebre|salida de tejido|dolor abdominal intenso|mareo o síncope|coágulos grandes|salida de líquido", dur="6 semanas|7 semanas|8 semanas|10 semanas|12 semanas|14 semanas|28 semanas|34 semanas")
G(231, "desviación del dedo gordo del pie hacia afuera|prominencia dolorosa en la base del dedo gordo del pie|deformidad en dedos del pie con dolor al usar calzado|callosidades dolorosas con deformidad en el pie|dolor y juanete en el primer dedo del pie",
  "dolor al calzado|callosidades|edema local|enrojecimiento sobre la prominencia|dificultad para caminar",
  "Refiere uso de calzado estrecho o con tacón.|Refiere antecedente familiar de juanetes.|Refiere trabajo de pie.|Refiere pie plano.",
  "Utilizó plantillas con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "fiebre|úlcera|herida infectada|pérdida de sensibilidad|dolor intenso súbito", dur="L")
G(232, "quemadura en antebrazo con dolor y ampollas|quemadura por líquido caliente con enrojecimiento|quemadura superficial con ardor|quemadura en mano con ampollas|quemadura con dolor intenso y piel enrojecida",
  "ampollas|ardor|dolor intenso|enrojecimiento|edema local",
  "Refiere contacto con agua caliente.|Refiere contacto con aceite caliente.|Refiere quemadura con fuego.|Refiere que ocurrió hace pocas horas.|Refiere quemadura con plancha.",
  "Se aplicó agua fría con alivio parcial.|Se aplicó cremas caseras o pasta dental.|No ha recibido tratamiento.",
  "quemadura extensa|quemadura en cara o genitales|fiebre|dificultad respiratoria|lesiones profundas sin dolor", dur="H")
G(233, "visión doble|diplopía con desviación de un ojo|visión doble al mirar hacia un lado|caída del párpado con diplopía|dificultad para mover un ojo con visión doble",
  "ptosis palpebral|desviación ocular|cefalea|mareo|dolor ocular|visión borrosa",
  "Refiere diabetes mellitus.|Refiere hipertensión arterial.|Refiere trauma craneal previo.|Refiere que el inicio fue brusco.",
  "No ha recibido tratamiento.|Acude de forma inmediata a valoración.",
  "debilidad de extremidades|dificultad para hablar|cefalea intensa|pérdida de conocimiento|fiebre", dur="A")
G(234, "dolor abdominal intermitente con náuseas|dolor periumbilical tipo cólico|prurito anal nocturno|evacuaciones blandas con moco y dolor abdominal|hiporexia con dolor abdominal y distensión|expulsión de parásitos en heces",
  "prurito anal|expulsión de parásitos|distensión abdominal|náuseas|hiporexia|palidez|bruxismo",
  "Refiere que camina descalzo.|Refiere consumo de agua no tratada.|Refiere que no se lava las manos con frecuencia.|Refiere antecedente de parasitosis.|La madre refiere que el niño juega con tierra.",
  "No ha recibido antiparasitarios recientemente.|Tomó antiparasitario con mejoría transitoria.|No ha recibido tratamiento.",
  "fiebre alta|vómitos persistentes|sangre en heces|dolor abdominal intenso|pérdida de peso importante", dur="B")
G(235, "dolor y sangrado de encías|encías inflamadas y sangrantes al cepillado|dolor gingival con mal aliento|movilidad dental con dolor al masticar|encías enrojecidas y dolorosas",
  "halitosis|encías sangrantes|movilidad dental|dolor al masticar|edema gingival|sabor desagradable",
  "Refiere higiene bucal deficiente.|Refiere tabaquismo.|Refiere que no acude al odontólogo.|Refiere diabetes mellitus.|Refiere uso de prótesis dentales.",
  "Realizó enjuagues con sal con alivio parcial.|Se automedicó con analgésicos.|No ha recibido tratamiento.",
  "fiebre|edema facial|dificultad para abrir la boca|salida de pus|pérdida de varias piezas dentales", dur="B")
G(236, "picadura de alacrán con dolor intenso|dolor, hormigueo y adormecimiento tras picadura de alacrán|picadura de alacrán con edema local|picadura reciente con dolor ardiente|dolor irradiado y sialorrea tras picadura",
  "hormigueo|adormecimiento local|sialorrea|inquietud|edema local|sudoración",
  "Refiere que la picadura ocurrió hace pocas horas.|Refiere picadura en mano o pie.|Refiere que vio al alacrán.|Refiere picadura durante la noche.",
  "Se lavó el área con agua y jabón.|Se aplicó hielo con alivio parcial.|No ha recibido tratamiento.",
  "dificultad respiratoria|convulsiones|vómitos|taquicardia intensa|sialorrea abundante|somnolencia", dur="H")
G(237, "acude a control con dolor y rigidez en cinturas|refiere dolor en hombros y caderas con rigidez matutina|refiere dificultad para levantar los brazos|acude por entrega de medicamento sin molestias nuevas|refiere fatiga y dolor muscular proximal",
  "rigidez matutina|dolor en hombros y caderas|fatiga|fiebre baja|pérdida de peso|dolor al levantarse",
  "Refiere control con reumatología.|Refiere que mejora con corticoides.|Refiere buena adherencia al tratamiento.|Refiere que los síntomas aparecieron en edad avanzada.",
  "en tratamiento con prednisona|en tratamiento con prednisona en reducción|con tratamiento irregular|sin tratamiento actual",
  "cefalea temporal intensa|alteración visual|fiebre alta|debilidad muscular marcada|claudicación mandibular", "Y")
G(238, "embarazo de {w} semanas con cifras de presión arterial elevadas|embarazo de {w} semanas con cefalea y edema|embarazo de {w} semanas con visión borrosa y presión elevada|embarazo de {w} semanas con epigastralgia y cefalea|embarazo de {w} semanas con presión arterial alta y proteinuria",
  "cefalea|edema|visión borrosa|epigastralgia|fosfenos|aumento de peso rápido",
  "Refiere antecedente de hipertensión en embarazo previo.|Refiere antecedente familiar de preeclampsia.|Es primigesta.|Refiere controles prenatales irregulares.",
  "No ha recibido tratamiento antihipertensivo.|En tratamiento con metildopa.|En vigilancia con control de presión.",
  "convulsiones|sangrado vaginal|pérdida de líquido|dolor en hipocondrio derecho|oliguria|disminución de movimientos fetales", dur="28 semanas|30 semanas|32 semanas|34 semanas|36 semanas|38 semanas")
G(239, "dolor e inflamación en el pene|enrojecimiento y edema del prepucio con dolor|dolor al retraer el prepucio|prepucio inflamado con secreción|dificultad para retraer el prepucio con dolor",
  "edema del prepucio|secreción bajo el prepucio|dolor al orinar|prurito local|dolor durante las erecciones",
  "Refiere higiene genital deficiente.|Refiere episodios previos de balanitis.|Refiere diabetes mellitus.|Refiere relaciones sexuales recientes.",
  "Se aplicó crema con corticoide sin mejoría.|Se aplicó crema antibiótica sin alivio.|No ha recibido tratamiento.",
  "fiebre|retención urinaria|secreción uretral|úlceras genitales|sangrado", dur="A")
G(240, "pápulas pruriginosas|pápulas excoriadas en extremidades con prurito intenso|lesiones papulares con costras hemáticas|prurito intenso con pápulas en brazos y piernas|pápulas rojizas pruriginosas recurrentes",
  "prurito intenso|costras hemáticas|lesiones por rascado|hiperpigmentación|insomnio",
  "Refiere picaduras de insectos.|Refiere antecedente de atopia.|Refiere episodios similares previos.|Refiere calor o sudoración.",
  "Se aplicó cremas con corticoide con alivio parcial.|Tomó antihistamínicos con alivio parcial.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|dolor intenso|lesiones en mucosas|ampollas", dur="B")
