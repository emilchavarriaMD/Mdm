from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
ONC = "Refiere diagnóstico previo confirmado por biopsia.|Refiere seguimiento con oncología.|Refiere que ha recibido quimioterapia o radioterapia.|Refiere antecedente familiar de cáncer."
ONCTX = "en seguimiento oncológico|en tratamiento quimioterapéutico|en tratamiento paliativo|con cuidados de soporte"
ONCN = "fiebre alta|sangrado importante|dificultad respiratoria|dolor incontrolable|confusión|vómitos persistentes"

G(141, "acude a control con úlcera en pie|refiere herida en pie con secreción y mal olor|refiere úlcera plantar que no cicatriza|acude por curación de úlcera en pie|refiere enrojecimiento y dolor en una herida del pie",
  "secreción purulenta|mal olor|enrojecimiento perilesional|edema del pie|pérdida de sensibilidad|callosidades",
  "Refiere diabetes mellitus de larga evolución.|Refiere que camina descalzo.|Refiere pérdida de sensibilidad en los pies.|Refiere calzado inadecuado.|Refiere glucemias elevadas.",
  "en curaciones locales|en tratamiento con antibiótico|con curaciones irregulares|sin tratamiento actual",
  "fiebre|escalofríos|enrojecimiento que asciende por la pierna|crepitación|necrosis|vómitos", dur="Y")
G(142, "solicita revisión ginecológica de rutina|acude a control ginecológico anual sin molestias|solicita toma de citología cervical|solicita revisión ginecológica por inicio de vida sexual|acude a revisión ginecológica con resultados de estudios previos",
  "molestias pélvicas leves|flujo vaginal escaso|dismenorrea leve|prurito ocasional|ciclos regulares",
  "Refiere última citología hace más de un año.|Refiere ciclos menstruales regulares.|Refiere que no tiene molestias.|Refiere que desea iniciar un método de planificación.|Refiere vida sexual activa con una pareja.",
  "No ha recibido tratamiento.|Trae resultados de citología previa.",
  "flujo anormal|sangrado vaginal anormal|dolor pélvico|dispareunia|fiebre|bulto mamario", dur="-")
G(143, "retraso menstrual con sospecha de embarazo|amenorrea de varias semanas y prueba de embarazo en casa|retraso menstrual con náuseas y sensibilidad mamaria|solicita prueba de embarazo por falta de menstruación|retraso menstrual con fatiga y somnolencia",
  "náuseas|sensibilidad mamaria|fatiga|somnolencia|polaquiuria|mareo",
  "Refiere fecha de última menstruación hace varias semanas.|Refiere relaciones sexuales sin protección.|Refiere uso irregular de anticonceptivos.|Refiere prueba casera positiva.|Refiere prueba casera negativa.",
  "No ha recibido tratamiento.|Se realizó prueba de embarazo en casa.",
  "dolor pélvico intenso|sangrado vaginal|fiebre|síncope|dolor en hombro", dur="B")
G(144, "fiebre intermitente con escalofríos y sudoración|fiebre alta cíclica con cefalea y mialgias|escalofríos intensos seguidos de fiebre y sudoración|fiebre con malestar general y dolor de cuerpo|fiebre de varios días con astenia marcada",
  "escalofríos|sudoración profusa|cefalea|mialgias|náuseas|astenia|palidez",
  "Refiere que vive o viajó a una zona endémica de paludismo.|Refiere picaduras de zancudos.|Refiere casos similares en su comunidad.|Refiere episodio previo de malaria.",
  "Tomó acetaminofén con alivio parcial.|No ha recibido tratamiento.|Se automedicó con antipalúdicos incompletos.",
  "sangrado|convulsiones|ictericia|dificultad respiratoria|confusión|disminución de la diuresis", dur="A")
G(145, "prurito intenso en cuero cabelludo|picazón de cabeza con lesiones por rascado|prurito en nuca con presencia de liendres|prurito persistente en cuero cabelludo y detrás de las orejas|comezón de cabeza con escoriaciones",
  "liendres visibles|escoriaciones|costras en nuca|adenopatías cervicales|insomnio|irritabilidad",
  "Refiere contacto con personas con piojos.|Refiere que comparte peines o gorros.|Refiere casos similares en la escuela o el hogar.|Refiere que los piojos han reaparecido.",
  "Se aplicó champú o loción antiparasitaria con alivio parcial.|Se aplicó remedios caseros sin éxito.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|dolor intenso|caída intensa del cabello|lesiones en otras zonas", dur="B")
G(146, "dolor, enrojecimiento y calor en mama|aumento de volumen doloroso en mama con eritema|mama dolorosa e indurada con fiebre|dolor mamario con zona eritematosa y caliente|mama endurecida y dolorosa con malestar general",
  "fiebre|escalofríos|malestar general|dolor al tacto|aumento de volumen mamario|secreción por el pezón",
  "Refiere que amamanta a su bebé.|Refiere grietas en el pezón.|Refiere que la mama se siente endurecida desde hace días.|Refiere antecedente de mastitis.|Refiere que usa sostén ajustado.",
  "Se aplicó compresas tibias con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "secreción purulenta|masa palpable previa|pérdida de peso|dolor abdominal|fiebre alta persistente", dur="A")
G(147, "placas blanquecinas en lengua y mucosa oral|lesiones blancas que se desprenden en la boca|ardor bucal con placas blanquecinas|sabor metálico y placas blancas en la lengua|molestia al comer con placas blanquecinas en paladar",
  "ardor bucal|dolor al comer|sabor alterado|fisuras en comisuras labiales|sequedad bucal|lengua enrojecida",
  "Refiere uso reciente de antibióticos.|Refiere uso de corticoides inhalados.|Refiere diabetes mellitus.|Refiere uso de prótesis dental.|Refiere inmunosupresión.",
  "Se aplicó enjuagues caseros sin mejoría.|Se aplicó gel oral con alivio parcial.|No ha recibido tratamiento.",
  "fiebre|dificultad para tragar|pérdida de peso|lesiones en esófago|dolor intenso", dur="B")
G(148, "embarazo de {w} semanas sin molestias que acude a control|embarazo de {w} semanas con náuseas y fatiga|embarazo de {w} semanas con movimientos fetales presentes|embarazo de {w} semanas con dolor lumbar leve|embarazo de {w} semanas que consulta por resultados de laboratorio",
  "náuseas|fatiga|dolor lumbar leve|acidez|edema leve de tobillos|insomnio",
  "Refiere controles prenatales regulares.|Refiere que es su primer embarazo.|Refiere embarazos previos sin complicaciones.|Refiere que sus ultrasonidos han sido normales.|Refiere que toma sus vitaminas.",
  "Toma ácido fólico y sulfato ferroso.|Recibió vacuna antitetánica.",
  "sangrado vaginal|pérdida de líquido|cefalea intensa|visión borrosa|contracciones regulares|disuria|disminución de movimientos fetales", dur="S")
G(149, "solicita orientación sobre la menopausia|sofocos y ciclos irregulares con deseo de orientación|inquietud por síntomas de la menopausia|solicita información sobre terapia para síntomas climatéricos|dudas sobre cuidados en la menopausia",
  "sofocos|sudoración nocturna|insomnio|sequedad vaginal|irritabilidad|dolor articular",
  "Refiere última menstruación hace varios meses.|Refiere ciclos irregulares desde hace un año.|Refiere antecedente familiar de menopausia temprana.|Refiere que desea conocer opciones de manejo.",
  "No ha recibido tratamiento.|Utiliza remedios naturales.",
  "sangrado vaginal posmenopáusico|dolor pélvico|dolor torácico|pérdida de peso|bulto mamario", dur="-")
G(150, "necesidad de orientación sobre métodos de planificación familiar|solicita información sobre anticonceptivos|solicita consejería anticonceptiva tras parto reciente|solicita orientación sobre planificación familiar para espaciar embarazos|desea conocer opciones de anticoncepción",
  "ciclos menstruales regulares|lactancia materna|vida sexual activa|deseo de espaciar embarazos|temor a efectos secundarios",
  "Refiere que no utiliza métodos anticonceptivos actualmente.|Refiere uso previo de preservativo.|Refiere uso previo de pastillas con olvidos frecuentes.|Refiere que desea esperar antes de otro embarazo.|Refiere que su pareja está de acuerdo.",
  "No ha recibido consejería previa.|Recibió orientación en consulta anterior.",
  "posibilidad de embarazo|sangrado anormal|dolor pélvico|flujo anormal|fiebre", dur="-")
G(151, "secreción genital anormal|flujo uretral o vaginal con molestias al orinar|úlcera genital o lesiones en la zona genital|dolor al orinar con secreción genital|molestia genital tras relaciones sexuales sin protección|prurito genital con secreción",
  "disuria|dispareunia|úlceras genitales|prurito genital|dolor pélvico|adenopatías inguinales",
  "Refiere relaciones sexuales sin protección.|Refiere nueva pareja sexual.|Refiere pareja con síntomas similares.|Refiere antecedente de infecciones de transmisión sexual.",
  "No ha recibido tratamiento.|Se automedicó con antibiótico sin mejoría.|Utilizó remedios caseros sin mejoría.",
  "fiebre|dolor pélvico intenso|dolor testicular|erupción en palmas o plantas|pérdida de peso", dur="A")
G(152, "utiliza anticonceptivo inyectable trimestral y acude a su control|acude a aplicación de anticonceptivo inyectable|acude a control del método inyectable con sangrado irregular|refiere amenorrea tras uso de anticonceptivo inyectable|acude por inyección trimestral con buena tolerancia",
  "sangrado irregular|amenorrea|cefalea leve|aumento de peso|mastalgia|acné",
  "Refiere que su última dosis fue hace 3 meses.|Refiere uso del método desde hace más de un año.|Refiere buena tolerancia al método.|Refiere que desea continuar con el método.",
  "Recibe anticonceptivo inyectable.|Recibe acetato de medroxiprogesterona trimestral.",
  "posibilidad de embarazo|sangrado abundante|dolor pélvico|cefalea intensa|dolor en pantorrilla", dur="-")
G(153, "dolor durante las relaciones sexuales|disminución del deseo sexual|dificultad para lograr o mantener la erección|ausencia de satisfacción sexual|sequedad con molestias durante el coito",
  "sequedad vaginal|ansiedad|dificultad en la pareja|disminución del deseo|dolor pélvico|fatiga",
  "Refiere que el problema empezó hace varios meses.|Refiere problemas de pareja.|Refiere estrés o ansiedad.|Refiere inicio de medicamentos nuevos.|Refiere antecedente de parto reciente.",
  "No ha recibido tratamiento.|Utilizó lubricantes con alivio parcial.",
  "sangrado con las relaciones|flujo anormal|fiebre|dolor pélvico intenso|violencia sexual", dur="L")
G(154, "dolor en cara anterior de rodilla|dolor rotuliano al subir escaleras|dolor anterior de rodilla al correr|dolor retropatelar con crepitación|dolor al arrodillarse o agacharse",
  "crepitaciones|dolor al subir escaleras|sensación de fallo|edema leve|rigidez tras estar sentado",
  "Refiere actividad deportiva frecuente.|Refiere sobrepeso.|Refiere trabajo con flexión repetida de rodillas.|Refiere trauma previo en la rodilla.",
  TXA + "|Utiliza rodillera con alivio parcial.", "bloqueo articular|fiebre|edema importante|trauma agudo|deformidad", dur="B")
G(155, "embarazo de {w} semanas con sangrado vaginal escaso y dolor pélvico|embarazo de {w} semanas con sangrado vaginal rojo oscuro y cólicos leves|embarazo de {w} semanas con manchado y dolor en hipogastrio|embarazo de {w} semanas con sangrado tras esfuerzo físico|embarazo de {w} semanas con sangrado vaginal intermitente",
  "dolor tipo cólico en hipogastrio|dolor lumbar|manchado vaginal|sangrado rojo oscuro|molestia pélvica",
  "Refiere antecedente de abortos previos.|Refiere esfuerzo físico previo al sangrado.|Refiere relaciones sexuales recientes.|Refiere embarazo confirmado con prueba.|Refiere que desea conservar el embarazo.",
  "Se le recomendó reposo.|No ha recibido tratamiento.|Acude a primera valoración.",
  "fiebre|salida de tejido|dolor abdominal intenso|salida de líquido|mareo o síncope|coágulos grandes", dur="6 semanas|7 semanas|8 semanas|9 semanas|10 semanas|11 semanas|12 semanas|14 semanas")
G(156, "amenorrea de varias semanas con náuseas|amenorrea con sensibilidad mamaria y fatiga|amenorrea con prueba de embarazo positiva|ausencia de menstruación con vómitos matutinos|amenorrea y somnolencia con sospecha de embarazo",
  "náuseas matutinas|vómitos|sensibilidad mamaria|fatiga|somnolencia|polaquiuria",
  "Refiere fecha de última menstruación hace varias semanas.|Refiere prueba casera positiva.|Refiere relaciones sexuales sin protección.|Refiere que desea confirmar el embarazo.",
  "No ha recibido tratamiento.|Se realizó prueba de embarazo en casa.",
  "sangrado vaginal|dolor pélvico intenso|fiebre|síncope|vómitos persistentes", dur="B")
G(157, "odinofagia intensa con fiebre y dificultad para tragar|dolor de garganta intenso con amígdalas con exudado|fiebre alta con odinofagia y adenopatías cervicales|odinofagia intensa sin tos|dolor de garganta con placas purulentas en amígdalas",
  "fiebre alta|exudado amigdalino|adenopatías cervicales dolorosas|cefalea|halitosis|náuseas|dolor abdominal",
  "Refiere contacto con personas con faringitis.|Refiere episodios previos de amigdalitis.|Refiere asistencia a escuela o guardería con casos similares.|Refiere que no tiene tos.",
  TXA, "tos|rinorrea|dificultad respiratoria|erupción en la piel|trismus|salivación excesiva", dur="A")
G(158, "cansancio fácil, palidez y mareo|astenia con palidez de piel y mucosas|fatiga progresiva con caída del cabello|palpitaciones y disnea de esfuerzo con palidez|ganas de comer hielo con cansancio y uñas quebradizas",
  "palidez|mareo|caída del cabello|uñas quebradizas|pica|cefalea|palpitaciones|disnea de esfuerzo",
  "Refiere dieta pobre en carnes y verduras.|Refiere menstruaciones abundantes.|Refiere embarazo o lactancia reciente.|Refiere antecedente de anemia.|Refiere parasitosis.",
  "No ha recibido tratamiento.|Tomó hierro de forma irregular.|Tomó multivitamínicos sin mejoría.",
  "sangrado digestivo|heces negras|pérdida de peso|fiebre|dolor torácico|desmayos", dur="L")
G(159, "acude a control sin dolor torácico reciente|refiere dolor opresivo en el pecho con el esfuerzo|refiere episodios de dolor precordial que ceden con el reposo|acude a control con disnea de esfuerzo|refiere dolor torácico opresivo al subir escaleras",
  "disnea de esfuerzo|palpitaciones|sudoración|dolor irradiado al brazo izquierdo|fatiga|mareo",
  "Refiere hipertensión o diabetes asociadas.|Refiere tabaquismo previo.|Refiere que usa nitroglicerina con alivio.|Refiere antecedente familiar de cardiopatía.|Refiere que ha tenido más episodios en la última semana.",
  "en tratamiento con nitratos|en tratamiento con ácido acetilsalicílico y atorvastatina|en tratamiento con betabloqueador|con tratamiento irregular",
  "dolor torácico en reposo prolongado|síncope|disnea importante|sudoración profusa|palpitaciones sostenidas|edema de piernas", dur="Y")
G(160, "acude a control sin palpitaciones recientes|refiere palpitaciones irregulares ocasionales|refiere mareo con latidos rápidos|acude por entrega de medicamento sin molestias|refiere palpitaciones con disnea leve",
  "palpitaciones|mareo|disnea leve|fatiga|dolor torácico leve|sensación de latidos irregulares",
  "Refiere control con cardiología.|Refiere consumo de café o estimulantes.|Refiere que sus electrocardiogramas previos fueron alterados.|Refiere estrés.",
  "en tratamiento con betabloqueador|en tratamiento con amiodarona|en anticoagulación|con tratamiento irregular",
  "síncope|dolor torácico opresivo|disnea importante|sangrado|déficit neurológico|edema de piernas", dur="Y")
G(161, "dolor e inflamación en varias articulaciones|dolor articular con rigidez matutina prolongada|edema y calor en articulaciones de manos y rodillas|dolor poliarticular simétrico con fatiga|artritis con limitación para la movilización",
  "rigidez matutina|edema articular|calor local|fatiga|fiebre baja|limitación del movimiento",
  "Refiere antecedente familiar de enfermedades reumáticas.|Refiere cuadro viral previo.|Refiere que ha tenido episodios similares.|Refiere que le cuesta realizar actividades diarias.",
  TXA, "fiebre alta|erupción en piel|ojo rojo|úlceras orales|dolor torácico|trauma reciente", dur="B")
G(162, "solicita orientación sobre salud sexual|dudas sobre prácticas sexuales seguras|solicita información sobre prevención de infecciones de transmisión sexual|desea resolver dudas sobre su sexualidad|solicita orientación sobre protección en las relaciones sexuales",
  "inquietud sobre infecciones de transmisión sexual|dudas sobre anticoncepción|temor a embarazo|inicio reciente de vida sexual",
  "Refiere que no ha recibido orientación previa.|Refiere nueva pareja sexual.|Refiere relaciones sexuales sin protección.|Refiere que desea conocer métodos de protección.",
  "No ha recibido orientación previa.|Recibió orientación previa en la escuela.",
  "secreción genital|úlceras genitales|dolor al orinar|dolor pélvico|fiebre", dur="-")
G(163, "dolor en pantorrillas al caminar que cede con el reposo|claudicación intermitente de miembros inferiores|frialdad y palidez de los pies|dolor en pierna al caminar corta distancia|disminución de pulsos distales con dolor",
  "frialdad de los pies|palidez|calambres|disminución del vello|dolor en reposo|úlceras en pie",
  "Refiere tabaquismo.|Refiere diabetes mellitus.|Refiere hipertensión arterial.|Refiere dislipidemia.|Refiere que camina cada vez menos distancia.",
  "en tratamiento con cilostazol|en tratamiento con ácido acetilsalicílico y estatina|con tratamiento irregular|sin tratamiento actual",
  "dolor en reposo intenso|cambios de coloración negra|úlcera sin cicatrizar|dolor súbito con palidez|fiebre", dur="Y")
G(164, "dolor en hombro al elevar el brazo|dolor en hombro con limitación para peinarse|dolor nocturno en hombro|dolor en cara lateral del hombro tras esfuerzo|dolor en hombro que empeora con movimientos repetitivos",
  "limitación de la elevación del brazo|dolor nocturno|dolor irradiado al brazo|chasquidos|debilidad del brazo|rigidez",
  "Refiere movimientos repetitivos por su trabajo.|Refiere cargar peso con el brazo.|Refiere actividad deportiva reciente.|Refiere trauma previo en el hombro.",
  TXA, "fiebre|deformidad|pérdida de fuerza importante|trauma reciente|dolor torácico|enrojecimiento del hombro", dur="B")
