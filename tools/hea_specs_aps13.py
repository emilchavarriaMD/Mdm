from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer.|Refiere que acude a entrega de medicamentos y control."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte|en espera de tratamiento"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"
CRON = "Refiere buena adherencia al tratamiento.|Refiere que ha omitido dosis del medicamento.|Refiere control con especialista.|Refiere que sus últimos exámenes fueron estables."
VIR = "Refiere contacto con personas con cuadro similar.|Refiere asistencia a escuela o guardería con casos similares.|Refiere que no está vacunada/o.|Refiere casos similares en su comunidad."

G(241, "dolor ocular intenso con fotofobia|ojo rojo doloroso con lagrimeo y visión borrosa|dolor ocular con sensación de cuerpo extraño y secreción|disminución de la visión con dolor y enrojecimiento|ojo rojo con fotofobia y dolor al parpadear",
  "fotofobia|lagrimeo|visión borrosa|secreción|blefarospasmo|sensación de cuerpo extraño",
  "Refiere uso de lentes de contacto.|Refiere trauma ocular reciente.|Refiere contacto con material vegetal.|Refiere conjuntivitis previa.|Refiere herpes labial previo.",
  "Se aplicó gotas oftálmicas sin receta sin mejoría.|Se lavó con infusiones caseras.|No ha recibido tratamiento.",
  "pérdida de visión|trauma penetrante|fiebre|cefalea intensa|vómitos", dur="A")
G(242, "peso bajo al nacer con dificultad para alimentarse|bebé de bajo peso con succión débil|recién nacido pequeño con poca ganancia de peso|control de recién nacido con peso bajo|lactante con bajo peso con tomas frecuentes y escasas",
  "succión débil|poca ganancia de peso|somnolencia|llanto débil|hipotermia leve|ictericia",
  "La madre refiere que nació antes de término.|La madre refiere control prenatal irregular.|La madre refiere lactancia materna a libre demanda.|La madre refiere que nació con menos de 2500 g.",
  "No ha recibido tratamiento.|La madre le ofrece lactancia materna a libre demanda.",
  "fiebre|cianosis|dificultad respiratoria|convulsiones|vómitos persistentes|rechazo total de las tomas", dur="D", u="días")
G(243, "acude a control con visión borrosa|refiere disminución de la agudeza visual|acude con retinopatía conocida|refiere moscas volantes|acude por seguimiento oftalmológico",
  "visión borrosa|moscas volantes|dificultad nocturna|escotomas|visión distorsionada",
  "Refiere diabetes mellitus de larga evolución.|Refiere hipertensión arterial.|Refiere control con oftalmología.|Refiere que sus glucemias han sido altas.",
  "en seguimiento oftalmológico|con tratamiento láser previo|sin tratamiento actual",
  "pérdida súbita de visión|dolor ocular|cortina oscura|destellos luminosos|trauma ocular", "Y")
G(244, "erupción maculopapular con fiebre baja|exantema que inicia en la cara y se extiende al cuerpo|erupción con adenopatías retroauriculares|exantema fino con malestar general|erupción rosada con artralgias",
  "adenopatías retroauriculares|fiebre baja|artralgias|conjuntivitis|odinofagia|malestar general",
  VIR, TXN, "fiebre alta|dificultad respiratoria|convulsiones|hemorragias|rigidez de cuello|embarazo", dur="A")
G(245, "dolor súbito en pantorrilla|dolor intenso en pantorrilla con sensación de chasquido|dolor súbito en tendón de Aquiles|dolor súbito con incapacidad para apoyar|dolor en pantorrilla al caminar con equimosis",
  "chasquido audible|equimosis|edema|incapacidad para apoyar|debilidad para ponerse de puntillas",
  "Refiere que ocurrió durante actividad deportiva.|Refiere que ocurrió al correr o saltar.|Refiere uso previo de quinolonas.|Refiere que sintió un golpe en la pierna.",
  "Se aplicó hielo con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "edema marcado de toda la pierna|fiebre|dificultad respiratoria|deformidad|frialdad o palidez del pie", dur="H")
G(246, "fiebre alta con erupción maculopapular|exantema con conjuntivitis y tos|fiebre, coriza y manchas en la boca|erupción que inicia en la cara y desciende|fiebre con tos y ojos rojos",
  "tos|coriza|conjuntivitis|manchas blanquecinas en la mucosa oral|erupción descendente|malestar general",
  VIR, TXN, "dificultad respiratoria|convulsiones|somnolencia marcada|diarrea intensa|rechazo de alimentos|otalgia", dur="A")
G(247, "acude a control con lesiones violáceas en piel|refiere lesiones nodulares en piel y mucosas|refiere edema de miembros inferiores con lesiones cutáneas|acude por entrega de antirretrovirales con lesiones en piel|refiere tos, fiebre y lesiones violáceas",
  "lesiones violáceas|edema de piernas|tos|pérdida de peso|fiebre|lesiones orales",
  "Refiere diagnóstico de VIH.|Refiere seguimiento con infectología.|Refiere que ha omitido dosis de antirretrovirales.|Refiere crecimiento progresivo de las lesiones.",
  "en tratamiento antirretroviral|en tratamiento quimioterapéutico|con tratamiento irregular|en seguimiento especializado",
  "disnea importante|hemoptisis|fiebre alta|dolor intenso|sangrado digestivo", "Y")
G(248, "edema en párpados y cara|hinchazón facial con orina oscura|edema periorbitario con presión elevada|orina color té con edema|edema matutino en cara con disminución de la orina",
  "orina oscura|hipertensión arterial|cefalea|disminución de la diuresis|fatiga|dolor lumbar",
  "Refiere infección de garganta o piel hace semanas.|Refiere que la orina ha cambiado de color.|Refiere edema que predomina por la mañana.|Refiere antecedente de infección estreptocócica.",
  "No ha recibido tratamiento.|Tomó diuréticos caseros sin mejoría.",
  "dificultad respiratoria|convulsiones|anuria|cefalea intensa|confusión", dur="A")
G(249, "edema en párpados, cara y piernas|hinchazón progresiva con orina espumosa|edema generalizado con aumento de peso|edema matutino en cara y vespertino en piernas|edema con orina espumosa y fatiga",
  "orina espumosa|aumento de peso|fatiga|disminución del apetito|ascitis|infecciones frecuentes",
  "Refiere edema de varias semanas de evolución.|Refiere que el edema ha progresado.|Refiere antecedente de infecciones recientes.|Refiere antecedente familiar de enfermedad renal.",
  TXN, "dificultad respiratoria|fiebre|dolor abdominal intenso|disminución marcada de la orina|dolor en pantorrilla", dur="B")
G(250, "fiebre alta con tos y dificultad respiratoria|tos seca, fiebre y disnea progresiva|fiebre, malestar general y falta de aire|dificultad respiratoria con fiebre y dolor torácico|fiebre con tos y saturación baja referida",
  "tos seca|disnea|dolor torácico|mialgias|diarrea|fatiga intensa|escalofríos",
  "Refiere contacto cercano con casos respiratorios graves.|Refiere viaje reciente.|Refiere enfermedad crónica asociada.|Refiere que no está vacunada/o.",
  "Tomó acetaminofén con alivio parcial.|No ha recibido tratamiento.",
  "cianosis|confusión|dolor torácico intenso|esputo con sangre|somnolencia|dificultad para hablar", dur="A")
G(251, "síntomas premenstruales con dolor mamario, distensión e irritabilidad|sensibilidad mamaria e hinchazón abdominal antes de la menstruación|irritabilidad y cefalea los días previos a la regla|cambios de ánimo y fatiga premenstrual|molestias premenstruales con acné y distensión",
  "dolor mamario|distensión abdominal|irritabilidad|cefalea|cambios de ánimo|antojos|edema leve",
  "Refiere que los síntomas ocurren una semana antes de la menstruación.|Refiere que mejoran al iniciar el sangrado.|Refiere ciclos regulares.|Refiere estrés laboral o familiar.",
  TXN, "ideas de hacerse daño|sangrado entre ciclos|fiebre|dolor pélvico intenso|retraso menstrual", dur="L")
G(252, "dolor en muñeca del lado del pulgar|dolor al agarrar objetos con el pulgar|dolor en muñeca con edema leve|dolor al hacer movimientos repetitivos de la mano|dolor en base del pulgar con limitación",
  "edema leve|dolor al apretar|chasquidos|limitación del movimiento|dolor al levantar al bebé",
  "Refiere movimientos repetitivos por su trabajo.|Refiere uso prolongado del celular o computadora.|Refiere cargar a su bebé con frecuencia.|Refiere trauma previo en la muñeca.",
  TXA + "|Utilizó férula con alivio parcial.", "fiebre|deformidad|parestesias intensas|trauma reciente|enrojecimiento intenso", dur="B")
G(253, "dolor en el cuello con limitación para girar la cabeza|cuello rígido y doloroso al despertar|dolor cervical con la cabeza desviada hacia un lado|dolor y contractura cervical tras mala posición|tortícolis con dolor al mover el cuello",
  "rigidez cervical|contractura|limitación del giro|dolor irradiado al hombro|cefalea|dolor al movimiento",
  "Refiere que durmió en mala posición.|Refiere exposición al aire frío.|Refiere esfuerzo físico reciente.|Refiere postura prolongada frente a computadora.",
  TXA + "|Aplicó calor local con alivio parcial.", "fiebre|rigidez con cefalea intensa|déficit neurológico|trauma cervical|dificultad para tragar", dur="A")
G(254, "dolor en región glútea|dolor profundo en nalga al sentarse|dolor glúteo con irradiación a muslo|dolor en región glútea tras inyección o esfuerzo|dolor y sensibilidad en nalga",
  "dolor al sentarse|dolor al caminar|irradiación al muslo|contractura|sensación de masa",
  "Refiere inyección reciente en la zona.|Refiere esfuerzo físico.|Refiere sedentarismo.|Refiere trauma previo.",
  TXA, "fiebre|enrojecimiento marcado|debilidad de pierna|pérdida de control de esfínteres|masa creciente", dur="B")
G(255, "dificultad para dormir con somnolencia diurna|sueño invertido con somnolencia durante el día|insomnio nocturno y sueño diurno|trastorno de horario de sueño por turnos de trabajo|dificultad para despertar y para dormir en horarios habituales",
  "somnolencia diurna|dificultad de concentración|irritabilidad|cefalea|fatiga",
  "Refiere trabajo en turnos nocturnos.|Refiere viaje reciente con cambio de horario.|Refiere uso de pantallas por la noche.|Refiere horarios de sueño irregulares.",
  TXN, "ideas de hacerse daño|ronquidos con pausas respiratorias|dolor nocturno|consumo de alcohol|episodios de dormirse de forma súbita", dur="L")
G(256, "desviación de la comisura labial|caída de un lado de la cara de inicio brusco|dificultad para cerrar un ojo y sonreír|parálisis facial con dolor retroauricular|asimetría facial al despertar",
  "dolor retroauricular|ojo seco|alteración del gusto|hiperacusia|lagrimeo|babeo",
  "Refiere exposición a aire frío.|Refiere cuadro viral previo.|Refiere diabetes mellitus.|Refiere episodio similar previo.",
  "No ha recibido tratamiento.|Se aplicó remedios caseros sin mejoría.",
  "debilidad de extremidades|dificultad para hablar|cefalea intensa|trauma craneal|vesículas en el oído|fiebre", dur="A")
G(257, "dolor facial tipo descarga eléctrica|dolor lancinante en mejilla desencadenado al masticar|dolor facial paroxístico de segundos de duración|dolor intenso al lavarse la cara o cepillarse|crisis de dolor facial unilateral",
  "dolor desencadenado por el tacto|dolor al masticar|dolor al hablar|dolor al viento frío|espasmos faciales",
  "Refiere episodios similares previos.|Refiere que el dolor es unilateral.|Refiere que tiene miedo de comer por el dolor.|Refiere dolor dental sin causa.",
  TXA, "debilidad facial|pérdida de sensibilidad|fiebre|alteraciones visuales|trauma facial", dur="B")
G(258, "mareo y visión borrosa al ponerse de pie|sensación de desvanecimiento al levantarse|palpitaciones y sudoración al cambiar de posición|mareo con debilidad al estar de pie|visión borrosa y aturdimiento al incorporarse",
  "visión borrosa|palpitaciones|sudoración|debilidad|náuseas|fatiga",
  "Refiere poca ingesta de líquidos.|Refiere diabetes mellitus.|Refiere uso de antihipertensivos.|Refiere episodios similares previos.|Refiere reposo prolongado.",
  "Mejoró al sentarse o acostarse.|No ha recibido tratamiento.",
  "pérdida del conocimiento|dolor torácico|déficit neurológico|dificultad respiratoria|sangrado digestivo", dur="B")
G(259, "menstruaciones abundantes con coágulos|sangrado menstrual abundante con duración prolongada|sangrado menstrual con uso de más de 6 compresas al día|menstruaciones muy abundantes con mareo|sangrado menstrual intenso con dolor pélvico",
  "coágulos|dismenorrea|mareo|fatiga|palidez|dolor pélvico",
  "Refiere ciclos regulares pero abundantes.|Refiere antecedente de anemia.|Refiere antecedente familiar de miomas.|Refiere uso de anticonceptivos.",
  "No ha recibido tratamiento.|Tomó antiinflamatorios con alivio parcial.|Tomó hierro de forma irregular.",
  "fiebre|dolor abdominal intenso|embarazo conocido|sangrado entre ciclos|pérdida de peso", dur="L")
G(260, "inflamación y dolor en el párpado|párpado enrojecido, caliente y doloroso|edema palpebral con enrojecimiento|párpado inflamado con secreción|aumento de volumen palpebral con dolor al parpadear",
  "edema palpebral|enrojecimiento|secreción|lagrimeo|sensación de cuerpo extraño|dolor al parpadear",
  "Refiere pequeña herida o picadura en el párpado.|Refiere conjuntivitis previa.|Refiere que se frota los ojos.|Refiere sinusitis reciente.",
  "Se aplicó compresas tibias con alivio parcial.|Se aplicó gotas oftálmicas sin receta.|No ha recibido tratamiento.",
  "fiebre alta|dolor al mover el ojo|disminución de la visión|edema facial|proptosis", dur="A")
G(261, "acude a control sin molestias específicas|refiere cansancio y aumento de peso|acude por seguimiento de alteración metabólica|acude con resultados de laboratorio alterados|refiere sed y poliuria",
  "fatiga|aumento de peso|sed intensa|poliuria|intolerancia al frío|mareo",
  "Refiere control con endocrinología.|Refiere antecedente familiar de enfermedad metabólica.|Refiere dieta desordenada.|Refiere sedentarismo.",
  "en seguimiento con dieta|en tratamiento específico|con tratamiento irregular|sin tratamiento actual",
  "vómitos|dolor abdominal|confusión|dificultad respiratoria|pérdida del conocimiento", "Y")
G(262, "irritabilidad y dolor mamario antes de la menstruación|cambios de ánimo y distensión abdominal premenstrual|tristeza, irritabilidad y fatiga antes de la regla|dolor mamario, cefalea y antojos previos a la menstruación|síntomas emocionales intensos en la semana previa a la menstruación",
  "irritabilidad|dolor mamario|cambios de ánimo|distensión abdominal|cefalea|antojos|fatiga",
  "Refiere que los síntomas ocurren una semana antes de la menstruación.|Refiere que los síntomas mejoran al iniciar el sangrado.|Refiere ciclos regulares.|Refiere estrés laboral o familiar.",
  TXN, "ideas de hacerse daño|sangrado entre ciclos|fiebre|dolor pélvico intenso|retraso menstrual", dur="L")
G(263, "dolor en muslo posterior tras esfuerzo|dolor súbito en cara posterior del muslo|dolor y sensibilidad muscular tras sprint|dolor muscular en pierna tras actividad deportiva|dolor y equimosis en músculo tras estiramiento brusco",
  "equimosis|edema|dolor al estirar|dolor al contraer|sensación de desgarro|limitación para correr",
  "Refiere actividad deportiva reciente.|Refiere que sintió un tirón.|Refiere que no calentó antes del ejercicio.|Refiere lesión previa en la misma zona.",
  "Se aplicó hielo con alivio parcial.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|imposibilidad para caminar|fiebre|parestesias|edema marcado de la pierna", dur="A")
G(264, "excoriaciones en rodillas y codos|raspones con dolor y escozor|abrasiones superficiales tras una caída|heridas superficiales por roce|excoriaciones con sangrado leve",
  "escozor|sangrado leve|enrojecimiento|tierra en las heridas|dolor al contacto",
  "Refiere caída en la calle.|Refiere caída en bicicleta.|Refiere caída jugando.|Refiere que ocurrió hace pocas horas.|Refiere que su vacuna antitetánica no está actualizada.",
  "Se lavó con agua y jabón.|Se aplicó alcohol o yodo.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|dolor intenso|deformidad|sangrado importante|herida profunda", dur="H")
G(265, "dolor y edema en pie tras traumatismo|dolor en pie con dificultad para apoyar|pie hinchado y doloroso tras una caída|dolor en tobillo y pie tras un golpe|equimosis y dolor en pie al caminar",
  "edema|equimosis|dolor al apoyar|dolor a la palpación|limitación de la movilidad",
  "Refiere caída reciente.|Refiere que se golpeó con un objeto.|Refiere accidente deportivo.|Refiere que se torció el pie.",
  "Se aplicó hielo con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|herida abierta|incapacidad para apoyar|parestesias|palidez del pie", dur="A")
G(266, "tos con expectoración de más de 2 semanas|tos crónica con sudoración nocturna y pérdida de peso|tos productiva con fiebre vespertina|tos con esputo y cansancio persistente|tos con expectoración y hiporexia",
  "sudoración nocturna|pérdida de peso|fiebre vespertina|hiporexia|astenia|dolor torácico",
  "Refiere contacto con personas con tuberculosis.|Refiere tos de más de 15 días.|Refiere tabaquismo.|Refiere condiciones de hacinamiento.|Refiere diabetes o VIH.",
  TXN, "esputo con sangre|disnea importante|dolor torácico intenso|confusión|fiebre alta", dur="L")
G(267, "herida en la pierna de lenta cicatrización|úlcera en miembro inferior con secreción|úlcera en pierna con dolor|úlcera con bordes irregulares en pierna|herida en pierna que no cicatriza",
  "secreción|mal olor|edema de pierna|dolor|várices|piel pigmentada alrededor",
  "Refiere várices de larga evolución.|Refiere diabetes mellitus.|Refiere que la herida inició tras un golpe.|Refiere que se aplica remedios caseros.",
  "Se realizó curaciones caseras con mejoría parcial.|Se aplicó pomadas sin mejoría.|No ha recibido tratamiento.",
  "fiebre|dolor intenso|necrosis|secreción purulenta abundante|pérdida de pulsos", dur="L")
G(268, "dolor y enrojecimiento en el borde del dedo gordo del pie|dolor y edema en el borde de la uña|uña incarnada con secreción|dolor al caminar por uña encarnada|enrojecimiento y supuración periungueal",
  "secreción purulenta|edema periungueal|dolor al calzado|tejido de granulación|enrojecimiento",
  "Refiere corte de uñas en forma curva.|Refiere uso de calzado estrecho.|Refiere episodios previos.|Refiere trauma previo en el dedo.",
  "Realizó baños de agua tibia con alivio parcial.|Se manipuló la uña sin mejoría.|No ha recibido tratamiento.",
  "fiebre|extensión del enrojecimiento|diabetes mellitus|dolor intenso en reposo|pérdida de sensibilidad", dur="B")
G(269, "erupción pruriginosa con fiebre baja|vesículas pruriginosas en distintas etapas|erupción vesicular que inició en tronco y cara|ampollas pequeñas con costras y prurito|vesículas diseminadas con malestar general",
  "prurito intenso|fiebre baja|malestar general|costras|hiporexia|irritabilidad",
  VIR + "|Refiere contacto con personas con varicela.", TXN, "dificultad respiratoria|fiebre alta|lesiones infectadas|confusión|rigidez de cuello|vómitos persistentes", dur="A")
G(270, "mordedura de serpiente|dolor y edema tras mordedura de serpiente|mordedura con dos orificios punzantes y sangrado|edema progresivo tras mordedura|dolor intenso, edema y equimosis posteriores a mordedura",
  "dolor intenso|edema progresivo|equimosis|sangrado local|náuseas|mareo|sangrado de encías",
  "Refiere que la mordedura ocurrió hace pocas horas.|Refiere que vio la serpiente.|Refiere mordedura en pie o mano.|Refiere que le colocaron torniquete.",
  "Se aplicó remedios caseros o torniquete.|Se lavó la herida con agua.|No ha recibido tratamiento.",
  "sangrado profuso|dificultad respiratoria|ptosis palpebral|síncope|vómitos|disminución de la orina", dur="H")
G(271, "lesiones elevadas, rugosas e indoloras en dorso de manos|verrugas en manos con superficie áspera|lesiones verrugosas en dedos de crecimiento lento|verrugas plantares dolorosas al caminar|lesiones rugosas múltiples en manos",
  "superficie áspera|dolor a la presión|puntos negros|aumento de número de lesiones|sangrado al roce",
  "Refiere hábito de morderse las uñas.|Refiere contacto con personas con verrugas.|Refiere uso de duchas públicas.|Refiere que las lesiones aumentan.",
  "Se aplicó remedios caseros sin mejoría.|Se aplicó productos sin receta sin cambios.|No ha recibido tratamiento.",
  "fiebre|dolor intenso|sangrado importante|cambio de color|ulceración", dur="L")
G(272, "lesiones vesiculares y pustulosas en piel|erupción con pústulas umbilicadas|fiebre seguida de lesiones en piel|lesiones cutáneas dolorosas con adenopatías|exantema vesiculopustuloso en genitales y extremidades",
  "fiebre|adenopatías|cefalea|mialgias|dolor en lesiones|lesiones en mucosas",
  "Refiere contacto cercano con un caso sospechoso.|Refiere contacto sexual reciente.|Refiere viaje reciente.|Refiere que no tiene vacuna previa.",
  TXN, "dificultad respiratoria|lesiones oculares|confusión|fiebre alta persistente|dolor intenso al tragar", dur="A")
G(273, "embarazo de {w} semanas con vómitos frecuentes|embarazo de {w} semanas con náuseas y vómitos que impiden comer|embarazo de {w} semanas con vómitos repetidos y pérdida de peso|embarazo de {w} semanas con vómitos matutinos persistentes|embarazo de {w} semanas con vómitos y debilidad",
  "náuseas intensas|pérdida de peso|debilidad|mareo|sialorrea|sed|boca seca",
  "Refiere náuseas desde el primer mes de embarazo.|Refiere que no tolera alimentos ni líquidos.|Refiere vómitos 5 o más veces al día.|Es primigesta.",
  "Se automedicó con antieméticos sin mejoría.|No ha recibido tratamiento.|Toma líquidos en pequeñas cantidades.",
  "sangrado vaginal|fiebre|dolor abdominal intenso|ictericia|signos de deshidratación|vómitos con sangre", dur="6 semanas|7 semanas|8 semanas|9 semanas|10 semanas|12 semanas|14 semanas")
