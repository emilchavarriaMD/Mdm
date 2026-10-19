from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
NEUR = "fiebre|déficit neurológico|pérdida del conocimiento|alteraciones visuales|convulsiones|vómitos persistentes"

G(105, "distensión abdominal y flatulencia|sensación de llenura con gases y eructos|distensión abdominal que empeora después de comer|flatulencia abundante con cólicos leves|abdomen distendido con borborigmos",
  "eructos|cólicos leves|estreñimiento|diarrea ocasional|hiporexia|saciedad temprana",
  "Refiere ingesta de leguminosas o lácteos antes del inicio.|Refiere dieta rica en grasas.|Refiere estrés reciente.|Refiere comer con rapidez.",
  TXN, "fiebre|vómitos|pérdida de peso|sangre en heces|dolor abdominal intenso|ictericia", dur="B")
G(106, "hormigueo en manos|parestesias en manos y dedos que empeoran por la noche|adormecimiento y hormigueo en pies|sensación de corriente en brazos|adormecimiento de los dedos al sostener objetos",
  "debilidad al sujetar objetos|despertares nocturnos por hormigueo|dolor en muñeca|calambres|sensación de quemazón",
  "Refiere trabajo con movimientos repetitivos de las manos.|Refiere diabetes mellitus.|Refiere postura prolongada del cuello.|Refiere uso prolongado de computadora.",
  TXN, "debilidad de una extremidad|dificultad para hablar|pérdida del equilibrio|pérdida de control de esfínteres|alteración visual", dur="B")
G(107, "calambres musculares en piernas|calambres nocturnos en pantorrillas|contracturas dolorosas en miembros inferiores|espasmos musculares con debilidad|calambres tras esfuerzo físico",
  "debilidad muscular|parestesias|fatiga|sudoración abundante|sed intensa|poliuria",
  "Refiere sudoración abundante y poca ingesta de líquidos.|Refiere actividad física intensa.|Refiere vómitos o diarrea previos.|Refiere uso de diuréticos.|Refiere dieta pobre en frutas.",
  "Tomó suero oral con alivio parcial.|Aumentó la ingesta de líquidos con alivio.|No ha recibido tratamiento.",
  "palpitaciones|debilidad intensa|orina oscura|confusión|fiebre|pérdida del conocimiento", dur="B")
G(108, "alteraciones del comportamiento|irritabilidad y conducta agresiva|cambios del comportamiento con aislamiento|inquietud psicomotriz con dificultad para concentrarse|conducta desafiante en casa y en la escuela",
  "irritabilidad|aislamiento|insomnio|inquietud|bajo rendimiento escolar|agresividad|ansiedad",
  "Según refiere un familiar, los cambios iniciaron hace varios meses.|Refiere conflictos familiares recientes.|Refiere bajo rendimiento escolar o laboral.|Refiere consumo de alcohol o sustancias.|Refiere pérdida de un familiar cercano.",
  "No ha recibido tratamiento.|Recibió orientación psicológica previa.|Está en seguimiento.",
  "ideas de hacerse daño|alucinaciones|conducta violenta hacia otros|consumo de drogas|fiebre", dur="L")
G(109, "acude a control sin dolor óseo|refiere dolor en espalda y articulaciones con densitometría alterada|acude por resultado de densitometría con osteopenia|refiere dolor lumbar crónico leve|acude a control con aporte de calcio irregular",
  "dolor óseo|disminución de la talla|dolor lumbar|fatiga|calambres|fracturas previas",
  "Refiere menopausia.|Refiere antecedente familiar de osteoporosis.|Refiere poca exposición solar.|Refiere consumo bajo de lácteos.|Refiere tabaquismo.",
  "en tratamiento con calcio y vitamina D|con uso irregular de calcio|en seguimiento con densitometría",
  "fractura reciente|dolor óseo intenso|pérdida de peso|fiebre|inmovilidad prolongada", dur="Y")
G(110, "enrojecimiento y costras en el borde de los párpados|prurito y descamación en el borde palpebral|ardor ocular con costras al despertar|párpados enrojecidos con escamas|sensación de arenilla con enrojecimiento palpebral",
  "prurito palpebral|ardor|lagrimeo|escamas en pestañas|pérdida de pestañas|sensación de cuerpo extraño",
  "Refiere piel grasa o dermatitis seborreica.|Refiere uso de maquillaje en los párpados.|Refiere frotamiento ocular frecuente.|Refiere episodios similares previos.",
  "Se aplicó compresas tibias con alivio parcial.|Se aplicó gotas lubricantes con alivio leve.|No ha recibido tratamiento.",
  "disminución de la visión|dolor ocular intenso|fiebre|edema facial|secreción purulenta abundante", dur="B")
G(111, "enrojecimiento ocular con ardor|ojo rojo con sensación de cuerpo extraño|molestia ocular con fotofobia|ardor y lagrimeo en un ojo|ojo rojo con visión borrosa leve",
  "fotofobia|lagrimeo|ardor|sensación de arenilla|visión borrosa leve|dolor leve",
  "Refiere uso de lentes de contacto.|Refiere exposición a polvo o humo.|Refiere uso prolongado de pantallas.|Refiere trauma ocular leve.",
  "Se aplicó lágrimas artificiales con alivio parcial.|Se aplicó gotas oftálmicas sin receta.|No ha recibido tratamiento.",
  "pérdida de la visión|dolor ocular intenso|trauma penetrante|halos alrededor de las luces|fiebre", dur="A")
G(112, "visión de moscas volantes|manchas flotantes y destellos luminosos en un ojo|visión de puntos o telarañas en el campo visual|moscas volantes de aparición reciente|destellos luminosos con sombras en el campo visual",
  "destellos luminosos|sombra en el campo visual|visión borrosa|miopía|cefalea|molestia ocular",
  "Refiere miopía moderada.|Refiere diabetes mellitus.|Refiere hipertensión arterial.|Refiere trauma ocular previo.|Refiere cirugía ocular previa.",
  "No ha recibido tratamiento.|Se realizó valoración oftalmológica previa.",
  "pérdida súbita de la visión|dolor ocular|cortina oscura en el campo visual|trauma reciente|cefalea intensa", dur="B")
G(113, "vértigo desencadenado por cambios de posición de la cabeza|sensación de giro al acostarse o girar en la cama|vértigo breve con náuseas|inestabilidad con sensación de giro al agacharse|mareo rotatorio de segundos de duración",
  "náuseas|sudoración|inestabilidad|acúfenos|hipoacusia|vómitos",
  "Refiere episodios previos.|Refiere cuadro gripal reciente.|Refiere trauma craneal previo.|Refiere que los episodios aparecen al acostarse.",
  "Tomó dimenhidrinato con alivio parcial.|No ha recibido tratamiento.",
  NEUR, dur="B")
G(114, "vértigo intenso y continuo con náuseas y vómitos|sensación de giro persistente con imposibilidad de caminar|vértigo súbito con inestabilidad severa|mareo rotatorio continuo de horas de evolución|vértigo con nistagmo y vómitos",
  "náuseas|vómitos|inestabilidad|sudoración|acúfenos|hipoacusia",
  "Refiere cuadro viral previo.|Refiere episodio similar previo.|Refiere que no puede levantarse sin ayuda.|Refiere antecedente de hipertensión.",
  "Tomó dimenhidrinato sin alivio.|No ha recibido tratamiento.",
  "debilidad de un lado del cuerpo|dificultad para hablar|diplopía|cefalea intensa|pérdida del conocimiento|dolor torácico", dur="H")
G(115, "evacuaciones diarreicas con moco|diarrea con moco, pujo y tenesmo|dolor abdominal con deposiciones blandas y moco|diarrea intermitente con flatulencia|evacuaciones con moco y cólico abdominal",
  "pujo|tenesmo|cólico abdominal|flatulencia|náuseas|hiporexia|pérdida de peso",
  "Refiere consumo de agua no tratada.|Refiere contacto con personas con diarrea.|Refiere antecedente de parasitosis.|Refiere ingesta de verduras mal lavadas.",
  TXN, "sangre en las heces|fiebre alta|deshidratación|vómitos persistentes|dolor abdominal intenso", dur="B")
G(116, "acude a control con hormigueo y ardor en los pies|refiere pérdida de sensibilidad en manos y pies|refiere dolor quemante en miembros inferiores|acude con debilidad distal y calambres|refiere adormecimiento con dolor nocturno en pies",
  "ardor en los pies|pérdida de sensibilidad|debilidad distal|calambres|dolor nocturno|dificultad para la marcha",
  "Refiere diabetes mellitus de larga evolución.|Refiere consumo de alcohol.|Refiere uso de medicamentos neurotóxicos.|Refiere que los síntomas han progresado.",
  "en tratamiento con gabapentina|en tratamiento con complejo B|en seguimiento neurológico|sin tratamiento actual",
  "heridas que no cicatrizan|debilidad rápidamente progresiva|dificultad respiratoria|pérdida de control de esfínteres|fiebre", dur="Y")
G(117, "ardor al orinar y aumento de la frecuencia urinaria|dolor perineal con disuria y urgencia miccional|dolor suprapúbico con chorro urinario débil|fiebre, dolor perineal y molestias urinarias|goteo postmiccional con malestar pélvico",
  "dolor perineal|fiebre|escalofríos|chorro débil|urgencia|nicturia|dolor al eyacular",
  "Refiere episodios urinarios previos.|Refiere relaciones sexuales sin protección.|Refiere sedentarismo o ciclismo frecuente.|Refiere antecedente de patología prostática.",
  TXB, "retención urinaria|fiebre alta|sangre en la orina|dolor lumbar intenso|secreción uretral", dur="A")
G(118, "quemadura solar con ampollas|enrojecimiento intenso y dolor en piel tras exposición solar|piel ardiente con ampollas en hombros y espalda|dolor y ardor en piel tras largas horas al sol|quemadura solar con descamación",
  "ardor|dolor al contacto|ampollas|prurito|escalofríos|cefalea|fiebre baja",
  "Refiere exposición solar prolongada sin protector.|Refiere que estuvo en la playa o al aire libre.|Refiere trabajo al aire libre.|Refiere uso de medicamentos fotosensibilizantes.",
  "Se aplicó gel de sábila con alivio parcial.|Se aplicó crema hidratante con alivio.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "fiebre alta|mareo intenso|vómitos|confusión|ampollas extensas|dificultad para beber líquidos", dur="A")
G(119, "dolor cervical irradiado al brazo|dolor en cuello con hormigueo en la mano|dolor cervical con debilidad del brazo|cervicalgia con parestesias en dedos|dolor en cuello y hombro irradiado al antebrazo",
  "hormigueo en la mano|debilidad del brazo|rigidez cervical|dolor nocturno|dolor al toser|contractura trapecio",
  "Refiere postura prolongada frente a computadora.|Refiere cargar peso en un hombro.|Refiere trauma previo en cuello.|Refiere dormir en mala posición.",
  TXA, "pérdida de fuerza importante|fiebre|pérdida de control de esfínteres|dolor torácico|trauma reciente", dur="B")
G(120, "acude a control con estornudos y prurito nasal|refiere congestión nasal y rinorrea hialina recurrente|refiere estornudos en salvas por las mañanas|acude con prurito ocular y nasal estacional|refiere obstrucción nasal con lagrimeo|refiere síntomas nasales tras exposición al polvo",
  "estornudos en salvas|prurito nasal|prurito ocular|lagrimeo|congestión nasal|rinorrea hialina|tos nocturna",
  "Refiere que los síntomas empeoran con el polvo o el cambio de clima.|Refiere antecedente familiar de alergias.|Refiere contacto con mascotas.|Refiere síntomas estacionales.",
  "en tratamiento con loratadina|en tratamiento con cetirizina|con uso intermitente de antihistamínicos|con lavados nasales con solución salina",
  "fiebre|secreción amarillenta|dolor facial|dificultad respiratoria|sangrado nasal", dur="Y")
