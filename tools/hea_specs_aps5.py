from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
CONT = "Refiere contacto con personas con cuadro similar.|Refiere asistencia a guardería o escuela con casos similares.|Refiere cambios bruscos de temperatura en los últimos días.|Refiere convivencia con familiares enfermos."
RES = "Refiere contacto con personas con cuadro respiratorio.|Refiere cambios bruscos de temperatura en los últimos días.|Refiere exposición a polvo o humo.|Refiere asistencia a escuela o trabajo con casos similares."

G(63, "acude a control refiriendo chorro urinario débil y nicturia|refiere dificultad para iniciar la micción y sensación de vaciamiento incompleto|acude por entrega de medicamento sin molestias urinarias nuevas|refiere polaquiuria, urgencia y goteo postmiccional|refiere nicturia de 3 a 4 veces por noche",
  "chorro urinario débil|goteo postmiccional|urgencia urinaria|sensación de vaciamiento incompleto|nicturia|esfuerzo para orinar",
  "Refiere que los síntomas han empeorado en el último año.|Refiere antecedente familiar de patología prostática.|Refiere que se realizó antígeno prostático en el pasado.|Refiere buena adherencia al tratamiento.",
  "en tratamiento con tamsulosina|en tratamiento con finasteride|en tratamiento con tamsulosina y finasteride|con tratamiento irregular",
  "hematuria|fiebre|retención urinaria aguda|dolor lumbar|pérdida de peso|dolor óseo", dur="Y")
G(64, "acude a control sin molestias y con buena adherencia al tratamiento|acude a control con cifras de presión arterial elevadas|refiere cefalea occipital ocasional y toma irregular del medicamento|refiere que se le terminó el medicamento hace varios días|acude a control refiriendo mareo ocasional|acude por entrega de medicamento con presión controlada en casa",
  "cefalea occipital|mareo|zumbido de oídos|palpitaciones|fosfenos|sensación de pesadez",
  "Refiere dieta con alto contenido de sal.|Refiere que omite dosis del medicamento con frecuencia.|Refiere sedentarismo.|Refiere antecedente familiar de hipertensión.|Refiere que se toma la presión en casa con cifras variables.|Refiere consumo de alcohol o tabaco.",
  "en tratamiento con losartán 50 mg al día|en tratamiento con enalapril 10 mg dos veces al día|en tratamiento con amlodipino 5 mg al día|en tratamiento con losartán e hidroclorotiazida|con tratamiento irregular",
  "dolor torácico|disnea|alteraciones visuales|debilidad en una extremidad|dificultad para hablar|edema de miembros inferiores", dur="Y")
G(65, "episodios de sudoración, temblor y mareo|sudoración fría con palpitaciones y hambre intensa|temblor y debilidad que mejoran al comer|mareo con visión borrosa y sensación de desmayo|irritabilidad y cefalea con hambre intensa antes de las comidas",
  "temblor|sudoración fría|palpitaciones|hambre intensa|visión borrosa|irritabilidad|cefalea",
  "Refiere ayunos prolongados o comidas espaciadas.|Refiere dieta baja en calorías.|Refiere episodios similares previos.|Refiere actividad física intensa sin alimentarse.|Refiere consumo de alcohol.",
  "Mejoró al consumir alimentos o bebidas azucaradas.|No ha recibido tratamiento.",
  "pérdida del conocimiento|convulsiones|confusión|diabetes mellitus conocida|uso de insulina", dur="A")
G(66, "episodios de sudoración, temblor y mareo con glucemias bajas|hipoglucemia con confusión que mejoró con azúcar|síntomas adrenérgicos tras omitir comidas|episodios nocturnos de sudoración y cefalea matutina|glucemia baja referida en automonitoreo",
  "temblor|sudoración fría|palpitaciones|hambre intensa|confusión|cefalea matutina|irritabilidad",
  "Refiere que omitió una comida después de usar su medicamento.|Refiere cambios en la dosis de insulina o hipoglucemiante.|Refiere actividad física intensa reciente.|Refiere vómitos o diarrea previos.|Refiere consumo de alcohol.",
  "en tratamiento con insulina|en tratamiento con glibenclamida|en tratamiento con metformina y glibenclamida|en tratamiento con insulina NPH y cristalina",
  "pérdida del conocimiento|convulsiones|trauma durante el episodio|dolor torácico|vómitos persistentes", dur="Y")
G(67, "mareo al cambiar de posición con visión borrosa|sensación de desmayo al ponerse de pie|mareo ortostático con debilidad|cifras de presión arterial bajas con fatiga|aturdimiento y sudoración fría al levantarse",
  "visión borrosa|debilidad|palpitaciones|sudoración fría|cefalea|náuseas|fatiga",
  "Refiere poca ingesta de líquidos.|Refiere calor intenso o ayunos prolongados.|Refiere diarrea o vómitos recientes.|Refiere uso de antihipertensivos.|Refiere episodios similares previos.",
  "Mejoró al acostarse con las piernas elevadas.|Tomó líquidos con alivio parcial.|No ha recibido tratamiento.",
  "pérdida del conocimiento|dolor torácico|sangrado digestivo|dificultad respiratoria|déficit neurológico", dur="B")
G(68, "coloración amarilla de piel y ojos|ictericia que inició en la cara y avanza a tórax y abdomen|piel amarillenta con somnolencia y succión débil|coloración amarilla en piel y escleras con buena succión|ictericia progresiva desde el segundo día de vida",
  "succión débil|somnolencia|orina oscura|heces claras|irritabilidad|poca ganancia de peso",
  "La madre refiere que nació a término por parto vaginal.|La madre refiere lactancia materna exclusiva.|La madre refiere que el bebé duerme mucho y despierta poco para alimentarse.|La madre refiere incompatibilidad de grupo sanguíneo.",
  "La madre lo expone al sol sin resultado.|No ha recibido tratamiento.|La madre le ofreció tomas más frecuentes.",
  "fiebre|rechazo total de las tomas|convulsiones|heces blancas|vómitos|hipotonía", dur="D", u="días")
G(69, "tos, rinorrea y malestar general|congestión nasal, tos y fiebre baja|tos con rinorrea y dolor de garganta|malestar general con tos y estornudos|secreción nasal con tos persistente y cefalea",
  "fiebre baja|odinofagia|cefalea|congestión nasal|estornudos|mialgias|hiporexia",
  RES, TXA, "dificultad respiratoria|fiebre alta|dolor torácico|esputo con sangre|vómitos|dolor de oído", dur="A")
G(70, "rinorrea hialina, estornudos y congestión nasal|catarro con secreción nasal clara y malestar general|obstrucción nasal con estornudos en salvas y lagrimeo|rinorrea acuosa y dolor de garganta leve|congestión nasal con tos seca y cefalea leve|estornudos con rinorrea y sensación de cuerpo cortado",
  "tos seca|odinofagia|cefalea leve|fiebre baja|malestar general|lagrimeo|ronquera|mialgias",
  RES, TXA, "dificultad respiratoria|fiebre alta|dolor de oído|dolor facial|esputo purulento|sibilancias", dur="A")
G(71, "tos productiva con expectoración amarillenta|tos con flemas, fiebre y dolor torácico al toser|tos persistente con expectoración verdosa|tos con dolor pleurítico y fiebre|tos con esputo y disnea leve",
  "fiebre|dolor torácico al toser|disnea leve|escalofríos|malestar general|expectoración purulenta|sibilancias",
  RES, TXB, "esputo con sangre|disnea importante|cianosis|confusión|sudoración nocturna|pérdida de peso", dur="A")
G(72, "ardor al orinar con aumento de la frecuencia urinaria|disuria, polaquiuria y urgencia miccional|dolor suprapúbico y orina de mal olor|ardor al orinar con goteo terminal|urgencia urinaria con sensación de vaciamiento incompleto|disuria con orina turbia",
  "dolor suprapúbico|urgencia miccional|orina turbia|orina de mal olor|tenesmo vesical|hematuria|nicturia",
  "Refiere ingesta baja de líquidos.|Refiere relaciones sexuales recientes.|Refiere episodios urinarios previos.|Refiere aseo genital inadecuado.|Refiere diabetes mellitus.",
  TXB, "fiebre|escalofríos|dolor lumbar|vómitos|secreción uretral o vaginal|hematuria macroscópica", dur="A")
G(73, "vesículas agrupadas y dolorosas en labio|ardor y hormigueo previos a la aparición de vesículas en la boca|lesiones vesiculosas con costra en la comisura labial|vesículas dolorosas en base eritematosa en región perioral|ampollas pequeñas agrupadas en labio superior",
  "ardor previo|prurito local|dolor al contacto|costras melicéricas|adenopatía cervical|malestar general|fiebre baja",
  "Refiere episodios similares previos.|Refiere exposición solar intensa antes del inicio.|Refiere estrés reciente.|Refiere cuadro gripal previo.|Refiere contacto con personas con lesiones similares.",
  "Se aplicó crema antiviral sin receta con alivio parcial.|Se aplicó remedios caseros sin mejoría.|No ha recibido tratamiento.",
  "lesiones oculares|lesiones genitales|fiebre alta|dificultad para comer|erupción generalizada", dur="A")
G(74, "evacuaciones líquidas abundantes con náuseas|diarrea acuosa con cólico abdominal|deposiciones líquidas de 5 a 6 veces al día con vómitos|diarrea con malestar general y fiebre baja|evacuaciones blandas frecuentes con dolor abdominal|vómitos y diarrea de inicio súbito",
  "náuseas|vómitos|cólico abdominal|fiebre baja|hiporexia|astenia|mialgias",
  "Refiere contacto con personas con diarrea.|Refiere ingesta de alimentos de la calle.|Refiere que en casa varias personas presentan síntomas similares.|Refiere consumo de agua no tratada.",
  "Ha tomado suero oral con alivio parcial.|Se automedicó con antidiarreicos sin mejoría.|No ha recibido tratamiento.",
  "sangre en las heces|fiebre alta|deshidratación importante|dolor abdominal intenso|vómitos persistentes|decaimiento marcado", dur="A")
G(75, "enrojecimiento, calor y dolor alrededor de una herida en pierna|herida con secreción purulenta y eritema perilesional|herida postraumática con dolor creciente y edema|herida que no cicatriza con secreción de mal olor|dolor y calor local en herida de varios días",
  "secreción purulenta|calor local|edema perilesional|mal olor|fiebre|adenopatías regionales|dolor creciente",
  "Refiere herida por trauma hace varios días.|Refiere que se lavó la herida solo con agua.|Refiere que se manipuló la herida con las manos sucias.|Refiere que no tiene vacuna antitetánica actualizada.|Refiere diabetes mellitus.",
  TXB, "fiebre alta|escalofríos|dolor desproporcionado|crepitación|ampollas|pérdida de sensibilidad", dur="A")
G(76, "fiebre alta, mialgias y malestar general|fiebre con escalofríos, tos y dolor de cuerpo|cefalea intensa, mialgias y odinofagia|fiebre de inicio súbito con tos seca y fatiga intensa|fiebre, congestión nasal y dolor articular|fiebre con astenia marcada y tos",
  "escalofríos|tos seca|odinofagia|cefalea|mialgias|artralgias|astenia|congestión nasal",
  RES + "|Refiere que no se ha vacunado contra influenza.", TXA, "dificultad respiratoria|dolor torácico|confusión|vómitos persistentes|fiebre de más de 5 días|esputo con sangre", dur="A")
G(77, "pesadez, edema y dolor en miembros inferiores al final del día|várices dolorosas con edema vespertino|calambres nocturnos y sensación de peso en las piernas|edema de tobillos con cambios de coloración de la piel|dolor en piernas que mejora al elevarlas",
  "várices visibles|edema vespertino|calambres nocturnos|prurito en piernas|hiperpigmentación|sensación de calor|úlceras en tobillo",
  "Acude a control con aumento de los síntomas.|Refiere trabajo con muchas horas de pie.|Refiere antecedente de várices familiares.|Refiere sobrepeso.|Refiere múltiples embarazos.",
  "en tratamiento con medias de compresión|con uso irregular de medias elásticas|con tratamiento flebotónico ocasional|sin tratamiento actual",
  "dolor unilateral súbito de la pantorrilla|enrojecimiento intenso|fiebre|úlcera abierta|dificultad respiratoria", dur="Y")
G(78, "sangrado menstrual abundante con coágulos|dolor pélvico y menstruaciones prolongadas|sensación de pesadez pélvica y aumento del flujo menstrual|aumento del perímetro abdominal con ciclos abundantes|dolor hipogástrico y polaquiuria|acude a control de ultrasonido con hallazgo de miomas",
  "menstruaciones abundantes|coágulos|dismenorrea|polaquiuria|estreñimiento|fatiga|dispareunia|aumento del volumen abdominal",
  "Refiere ciclos regulares pero abundantes.|Refiere antecedente familiar de miomatosis.|Refiere que el ultrasonido reportó miomas.|Refiere anemia en controles previos.|Refiere que no ha tenido embarazos.",
  "en vigilancia sin tratamiento específico|con tratamiento hormonal previo|con hierro por anemia|en tratamiento sintomático con antiinflamatorios",
  "sangrado entre menstruaciones|pérdida de peso|fiebre|dolor pélvico intenso súbito|sangrado posmenopáusico", dur="Y")
G(79, "acude a control refiriendo astenia y palidez|refiere sangrado de encías y moretones fáciles|refiere fiebre recurrente e infecciones frecuentes|acude a control con dolor óseo y fatiga|acude por entrega de medicamento sin molestias nuevas",
  "astenia|palidez|dolor óseo|petequias|infecciones frecuentes|pérdida de peso|sudoración nocturna|adenopatías",
  "Refiere control con hematología.|Refiere quimioterapia previa.|Refiere que sus últimos exámenes fueron normales.|Refiere hospitalizaciones previas.",
  "en seguimiento hematológico|en tratamiento quimioterapéutico|en tratamiento de mantenimiento|con tratamiento irregular",
  "fiebre alta|sangrado importante|dificultad respiratoria|cefalea intensa|confusión", dur="Y")
G(80, "dolor lumbar de intensidad moderada|lumbalgia que empeora con los movimientos y al estar de pie|dolor en región lumbar con rigidez matutina|dolor lumbar tras levantar un objeto pesado|dolor lumbar que mejora con el reposo|lumbalgia mecánica con limitación para agacharse",
  "rigidez lumbar|contractura muscular|limitación de movimientos|dolor a la palpación|dolor al cambiar de posición|irradiación a glúteos",
  "Refiere que cargó peso o realizó esfuerzo físico.|Refiere trabajo con posturas prolongadas.|Refiere sedentarismo.|Refiere episodios similares previos.|Refiere sobrepeso.|Refiere que durmió en mala posición.",
  TXA + "|Aplicó calor local con alivio parcial.", "fiebre|pérdida del control de esfínteres|debilidad de los miembros inferiores|dolor nocturno intenso|trauma reciente|pérdida de peso", dur="A")
G(81, "acude a control por malformación congénita conocida|refiere seguimiento por anomalía congénita desde el nacimiento|acude a revisión de malformación sin síntomas nuevos|acude a valoración por alteración congénita identificada en ultrasonido|seguimiento de defecto congénito sin síntomas nuevos",
  "dificultad para alimentarse|retraso del desarrollo|infecciones respiratorias frecuentes|limitación funcional|molestias locales",
  "La madre refiere que la alteración fue notada al nacer.|La madre refiere control con especialista.|La madre refiere antecedentes familiares de malformaciones.|La madre refiere control prenatal completo.",
  "No ha recibido tratamiento.|Recibió valoración especializada previa.|Está en seguimiento.",
  "fiebre|dificultad respiratoria|cianosis|vómitos persistentes|convulsiones", dur="-")
G(82, "sensación de giro de objetos con náuseas|vértigo rotatorio de segundos de duración al cambiar de posición|mareo con sensación de inestabilidad al caminar|sensación de movimiento del entorno con sudoración|vértigo episódico con náuseas y vómitos|mareo intenso con sensación de pérdida del equilibrio",
  "náuseas|vómitos|sudoración|acúfenos|hipoacusia|inestabilidad al caminar|cefalea",
  "Refiere que los síntomas aparecen al girar la cabeza o acostarse.|Refiere episodios similares previos.|Refiere cuadro gripal previo.|Refiere pocas horas de sueño o estrés.|Refiere poca ingesta de líquidos.",
  "Tomó dimenhidrinato con alivio parcial.|Descansó en reposo con alivio.|No ha recibido tratamiento.",
  "pérdida del conocimiento|debilidad de un lado del cuerpo|dificultad para hablar|diplopía|cefalea intensa|fiebre", dur="A")
