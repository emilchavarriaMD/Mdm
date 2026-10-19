from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer.|Refiere que acude a entrega de medicamentos y control."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte|en espera de tratamiento"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"
CRON = "Refiere buena adherencia al tratamiento.|Refiere que ha omitido dosis del medicamento.|Refiere control con especialista.|Refiere que sus últimos exámenes fueron estables."
VIR = "Refiere que vive en zona con casos similares.|Refiere picaduras de zancudos.|Refiere vecinos con cuadro similar.|Refiere viaje reciente a zona endémica."

G(186, "acude a control con cansancio y palpitaciones|refiere disnea de esfuerzo y edema de miembros inferiores|acude por seguimiento sin molestias nuevas|refiere estreñimiento crónico y dificultad para tragar|refiere palpitaciones y mareo",
  "palpitaciones|disnea de esfuerzo|edema de miembros inferiores|estreñimiento crónico|disfagia|síncope",
  "Refiere que vive o vivió en zona endémica de Chagas.|Refiere control con cardiología.|Refiere antecedente de picadura de chinche.|Refiere electrocardiograma previo alterado.",
  "en seguimiento cardiológico|con tratamiento irregular|en tratamiento con benznidazol|sin tratamiento actual",
  "síncope|dolor torácico|disnea importante|fiebre|edema generalizado", "Y")
G(187, "acude a control con temblor y lentitud de movimientos|refiere rigidez y dificultad para caminar|refiere caídas por inestabilidad|acude por entrega de medicamento con temblor en reposo|refiere dificultad para iniciar la marcha",
  "temblor en reposo|bradicinesia|rigidez|inestabilidad postural|marcha arrastrando los pies|estreñimiento",
  CRON, "en tratamiento con levodopa/carbidopa|en tratamiento con pramipexol|con tratamiento irregular|sin tratamiento actual",
  "caídas con lesiones|alucinaciones|disfagia importante|fiebre|confusión", "Y")
G(188, "acude a control con dolor en piernas al caminar|refiere claudicación y frialdad de pies|refiere dolor en reposo en miembros inferiores|refiere úlcera en pie de lenta cicatrización|acude por entrega de medicamento sin molestias nuevas",
  "claudicación|frialdad de pies|palidez|úlceras|disminución del vello|dolor nocturno",
  "Refiere tabaquismo.|Refiere diabetes mellitus.|Refiere hipertensión arterial.|Refiere dislipidemia.",
  "en tratamiento con ácido acetilsalicílico|en tratamiento con cilostazol|con tratamiento irregular|sin tratamiento actual",
  "dolor súbito con palidez|cambio de color negruzco|fiebre|úlcera sin cicatrizar|dolor intenso en reposo", "Y")
G(189, "erupción pruriginosa con fiebre baja|exantema maculopapular con conjuntivitis|erupción en tronco y extremidades con artralgias|prurito intenso con erupción y malestar general|erupción con dolor articular y cefalea",
  "conjuntivitis|artralgias|fiebre baja|cefalea|mialgias|edema de manos y pies",
  VIR, TXA, "fiebre alta|dolor abdominal intenso|vómitos persistentes|sangrado|déficit neurológico|dificultad respiratoria", dur="A")
G(190, "fiebre alta con dolor articular intenso|poliartralgias incapacitantes con fiebre|fiebre, erupción y dolor articular en manos y pies|dolor articular con edema y rigidez matutina|fiebre de inicio súbito con artralgias y cefalea",
  "artralgias intensas|edema articular|erupción cutánea|cefalea|mialgias|náuseas|rigidez matutina",
  VIR, TXA, "sangrado|dolor abdominal intenso|vómitos persistentes|somnolencia|dificultad respiratoria|confusión", dur="A")
G(191, "acude a control con edema y orina espumosa|refiere astenia, náuseas y prurito|acude por seguimiento de función renal sin molestias nuevas|refiere disminución de la orina y edema de miembros inferiores|refiere cansancio y falta de apetito",
  "edema|orina espumosa|náuseas|prurito|astenia|disminución de la diuresis|calambres",
  "Refiere control con nefrología.|Refiere hipertensión arterial o diabetes asociadas.|Refiere que sus exámenes de creatinina están elevados.|Refiere dieta con restricción de sal.",
  "en tratamiento conservador|en hemodiálisis|en tratamiento antihipertensivo|con tratamiento irregular",
  "dificultad respiratoria|dolor torácico|anuria|confusión|vómitos persistentes|fiebre", "Y")
G(192, "acude a control con palpitaciones y cansancio|refiere dolor torácico leve con el esfuerzo|refiere disnea de esfuerzo y edema|acude por entrega de medicamento sin molestias|refiere mareo y palpitaciones",
  "palpitaciones|disnea de esfuerzo|edema de miembros inferiores|fatiga|mareo|dolor torácico leve",
  "Refiere hipertensión arterial.|Refiere control con cardiología.|Refiere antecedente familiar de cardiopatía.|Refiere que sus electrocardiogramas previos fueron alterados.",
  "en tratamiento antihipertensivo|en tratamiento con diurético|con tratamiento irregular|sin tratamiento actual",
  "síncope|dolor torácico opresivo|disnea importante|palpitaciones sostenidas|edema generalizado", "Y")
G(193, "embarazo de {w} semanas con diabetes gestacional en control|embarazo de {w} semanas con hipotiroidismo en tratamiento|embarazo de {w} semanas con glucemias elevadas en tamizaje|embarazo de {w} semanas con enfermedad endocrina conocida|embarazo de {w} semanas con alteración metabólica en seguimiento",
  "poliuria|polidipsia|fatiga|aumento de peso|visión borrosa|palpitaciones",
  "Refiere diabetes previa al embarazo.|Refiere tamizaje alterado para diabetes gestacional.|Refiere control con endocrinología.|Refiere antecedente familiar de diabetes.",
  "En dieta y ejercicio.|En tratamiento con insulina.|En tratamiento con levotiroxina.",
  "sangrado vaginal|pérdida de líquido|cefalea intensa|vómitos persistentes|disminución de movimientos fetales", dur="S")
G(194, "acude a control con buena adherencia al tratamiento|refiere alucinaciones auditivas ocasionales|acude con insomnio y aislamiento|refiere desconfianza y alteraciones del pensamiento|acude por entrega de medicamento sin alteraciones nuevas",
  "alucinaciones auditivas|ideas delirantes|aislamiento social|insomnio|abandono del autocuidado|irritabilidad",
  "Refiere control con psiquiatría.|Refiere que dejó el medicamento por temporadas.|Refiere apoyo familiar.|Refiere hospitalizaciones previas.",
  "en tratamiento con risperidona|en tratamiento con haloperidol|en tratamiento con olanzapina|con tratamiento irregular",
  "ideas de hacerse daño|ideas de dañar a otros|rigidez muscular con fiebre|conducta violenta|consumo de sustancias", "Y")
G(195, "fiebre alta con cefalea y dolor lumbar|fiebre con ictericia y vómitos|fiebre con escalofríos y dolor muscular|fiebre, náuseas y coloración amarilla de piel|fiebre alta con postración",
  "ictericia|vómitos|dolor lumbar|mialgias|hemorragia gingival|cefalea",
  "Refiere que viajó a zona endémica.|Refiere que no está vacunada/o contra fiebre amarilla.|Refiere picaduras de zancudos.|Refiere casos similares en su comunidad.",
  "Tomó acetaminofén con alivio parcial.|No ha recibido tratamiento.",
  "sangrado importante|oliguria|confusión|convulsiones|dificultad respiratoria", dur="A")
G(196, "dolor intenso, deformidad y aumento de volumen en antebrazo|dolor intenso en brazo con limitación del movimiento tras una caída|dolor, edema e impotencia funcional tras traumatismo|deformidad visible en miembro tras un golpe|dolor intenso y crepitación en el hueso afectado",
  "deformidad|edema|equimosis|impotencia funcional|parestesias|dolor a la movilización",
  "Refiere caída con apoyo de la mano.|Refiere accidente de tránsito.|Refiere caída de una altura.|Refiere trauma durante actividad deportiva.|Refiere que ocurrió hace pocas horas.",
  "Se inmovilizó con férula improvisada.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "herida abierta con hueso expuesto|pérdida de pulso o frialdad distal|pérdida de sensibilidad|pérdida del conocimiento|sangrado importante", dur="H")
G(197, "lesiones dolorosas en encías y mucosa oral|vesículas y úlceras en boca con fiebre|dolor intenso al comer con encías inflamadas|úlceras múltiples en mucosa oral con sialorrea|fiebre y lesiones dolorosas en la boca",
  "fiebre|sialorrea|adenopatías cervicales|halitosis|rechazo de alimentos|irritabilidad|encías sangrantes",
  "Refiere contacto con personas con herpes labial.|Refiere episodio similar previo.|La madre refiere que el niño rechaza los alimentos.|Refiere estrés o cuadro viral previo.",
  "Se aplicó gel oral con alivio parcial.|Tomó acetaminofén con alivio parcial.|No ha recibido tratamiento.",
  "dificultad para tragar|signos de deshidratación|fiebre alta persistente|lesiones en ojos|lesiones genitales", dur="A")
G(198, "disminución súbita de la visión en un ojo|pérdida repentina de la visión en un ojo con manchas oscuras|visión borrosa súbita con moscas volantes|sombra oscura en el campo visual de un ojo|pérdida de visión indolora en un ojo",
  "moscas volantes|destellos luminosos|sombra oscura|visión borrosa|dolor ocular ausente",
  "Refiere diabetes mellitus.|Refiere hipertensión arterial.|Refiere que ocurrió al despertar.|Refiere trauma ocular previo.",
  "No ha recibido tratamiento.|Acude de forma inmediata a valoración.",
  "dolor ocular|trauma reciente|cefalea intensa|déficit neurológico|ojo rojo", dur="H")
G(199, "coloración amarilla de piel y ojos|ictericia con orina oscura y heces claras|ictericia, náuseas y fatiga intensa|dolor en hipocondrio derecho con ictericia|coloración amarilla con astenia y hiporexia",
  "orina oscura|heces claras|náuseas|vómitos|astenia|hiporexia|dolor en hipocondrio derecho",
  "Refiere contacto sexual sin protección.|Refiere contacto con personas con hepatitis.|Refiere uso de agujas compartidas.|Refiere procedimientos con instrumentos no estériles.",
  TXN, "sangrado|confusión|somnolencia|fiebre alta|vómitos persistentes", dur="B")
G(200, "acude a control sin molestias digestivas|refiere fatiga y dolor en hipocondrio derecho|acude por entrega de medicamento con buena tolerancia|refiere hiporexia y malestar abdominal|acude con control de pruebas hepáticas",
  "fatiga|dolor en hipocondrio derecho|hiporexia|náuseas|ictericia ocasional|distensión abdominal",
  "Refiere control con hepatología.|Refiere que sus transaminasas estaban elevadas.|Refiere buena adherencia al tratamiento.|Refiere antecedente familiar de hepatitis B.",
  "en tratamiento antiviral|en seguimiento sin tratamiento|con tratamiento irregular",
  "ictericia importante|sangrado digestivo|ascitis|confusión|fiebre|vómitos persistentes", "Y")
G(201, "ictericia, orina oscura y cansancio|coloración amarilla con astenia intensa|fatiga y náuseas con ictericia|orina oscura y heces claras con hiporexia|malestar general con ictericia",
  "orina oscura|heces claras|náuseas|hiporexia|dolor abdominal leve|astenia",
  "Refiere uso de agujas compartidas.|Refiere transfusiones o procedimientos previos.|Refiere contacto con personas con hepatitis.|Refiere tatuajes o piercings recientes.",
  TXN, "sangrado|confusión|somnolencia|fiebre alta|vómitos persistentes", dur="B")
G(202, "acude a control sin molestias específicas|refiere fatiga y malestar abdominal|acude por entrega de medicamento con buena tolerancia|refiere dolor en hipocondrio derecho y astenia|acude con resultados de carga viral",
  "fatiga|dolor en hipocondrio derecho|hiporexia|náuseas|prurito|distensión abdominal",
  "Refiere control con hepatología.|Refiere buena adherencia al tratamiento.|Refiere que su carga viral estaba detectable.|Refiere antecedente de transfusiones.",
  "en tratamiento antiviral|en seguimiento sin tratamiento|con tratamiento irregular",
  "ictericia importante|sangrado digestivo|ascitis|confusión|fiebre", "Y")
G(203, "dolor quemante en un hemitórax seguido de vesículas|vesículas agrupadas con dolor ardiente en un dermatoma|ardor y hormigueo en un lado del tórax con erupción vesicular|erupción vesicular dolorosa unilateral|dolor intenso en la piel previo a la aparición de lesiones",
  "ardor|hiperestesia|vesículas agrupadas|costras|fiebre baja|malestar general|prurito",
  "Refiere antecedente de varicela.|Refiere estrés reciente.|Refiere edad avanzada o inmunosupresión.|Refiere dolor previo a la aparición de las lesiones.",
  "Se aplicó cremas caseras sin mejoría.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "lesiones en ojo|parálisis facial|fiebre alta|lesiones diseminadas|confusión", dur="A")
G(204, "acude a control con perfil de lípidos alterado|acude con colesterol elevado sin síntomas|acude por seguimiento de hipercolesterolemia|acude por entrega de medicamento sin molestias|acude con resultados de laboratorio con LDL elevado",
  "xantomas|sobrepeso|sedentarismo|molestias abdominales leves",
  "Refiere dieta rica en grasas.|Refiere antecedente familiar de colesterol alto.|Refiere sedentarismo.|Refiere que sus lípidos estaban elevados en el último control.|Refiere tabaquismo.",
  "en tratamiento con atorvastatina|en tratamiento con simvastatina|con dieta y ejercicio|con tratamiento irregular",
  "dolor torácico|debilidad muscular|dolor muscular intenso|orina oscura|déficit neurológico", "Y")
G(205, "acude a control con perfil lipídico alterado|acude con colesterol y triglicéridos elevados sin síntomas|acude por seguimiento de dislipidemia mixta|acude por entrega de medicamento sin molestias|acude con resultados de laboratorio alterados",
  "sobrepeso|sedentarismo|dolor abdominal leve|xantomas",
  "Refiere dieta rica en grasas y carbohidratos.|Refiere antecedente familiar de dislipidemia.|Refiere sedentarismo.|Refiere diabetes asociada.|Refiere consumo de alcohol.",
  "en tratamiento con atorvastatina|en tratamiento con atorvastatina y fibrato|con dieta y ejercicio|con tratamiento irregular",
  "dolor torácico|dolor abdominal intenso|dolor muscular intenso|déficit neurológico|orina oscura", "Y")
G(206, "embarazo de {w} semanas con cifras de presión arterial elevadas|embarazo de {w} semanas con presión arterial alta en control prenatal|embarazo de {w} semanas con cefalea y presión elevada|embarazo de {w} semanas con edema leve y presión elevada|embarazo de {w} semanas con presión arterial en seguimiento",
  "cefalea|edema leve|mareo|acúfenos|fosfenos|aumento de peso",
  "Refiere que sus cifras previas eran normales.|Refiere antecedente de hipertensión en embarazo previo.|Refiere controles prenatales regulares.|Es primigesta.|Refiere antecedente familiar de hipertensión.",
  "No ha recibido tratamiento antihipertensivo.|En vigilancia con control de presión.|En tratamiento con metildopa.",
  "convulsiones|visión borrosa|dolor en epigastrio|sangrado vaginal|pérdida de líquido|disminución de movimientos fetales", dur="24 semanas|28 semanas|30 semanas|32 semanas|34 semanas|36 semanas|38 semanas")
G(207, "acude a control con triglicéridos elevados|acude con perfil lipídico alterado sin síntomas|acude por seguimiento de hipertrigliceridemia|acude por entrega de medicamento sin molestias|acude con resultados de laboratorio con triglicéridos altos",
  "sobrepeso|dolor abdominal leve|sedentarismo",
  "Refiere dieta rica en carbohidratos y azúcares.|Refiere consumo de alcohol.|Refiere sedentarismo.|Refiere diabetes mellitus.|Refiere antecedente familiar de dislipidemia.",
  "en tratamiento con fenofibrato|con dieta y ejercicio|con tratamiento irregular",
  "dolor abdominal intenso|vómitos|fiebre|dolor torácico|xantomas eruptivos", "Y")
