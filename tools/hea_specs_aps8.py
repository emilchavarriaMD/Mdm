from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
RES = "Refiere contacto con personas con cuadro respiratorio.|Refiere cambios bruscos de temperatura en los últimos días.|Refiere exposición a polvo o humo.|Refiere asistencia a escuela o trabajo con casos similares."

G(121, "rinorrea hialina, estornudos y obstrucción nasal|congestión nasal con secreción clara y dolor de garganta leve|catarro con estornudos y malestar general|obstrucción nasal con rinorrea acuosa y tos seca|rinorrea y estornudos con ojos llorosos|nariz tapada con secreción y cefalea leve",
  "odinofagia leve|tos seca|cefalea|fiebre baja|malestar general|lagrimeo|mialgias",
  RES, TXA, "fiebre alta|dolor facial|dificultad respiratoria|dolor de oído|esputo purulento|sibilancias", dur="A")
G(122, "erupción eritematosa pruriginosa|lesiones maculopapulares en tronco y extremidades|erupción diseminada con prurito|ronchas y manchas rojas en piel con picazón|exantema en cara y tronco",
  "prurito|fiebre baja|malestar general|descamación|lesiones por rascado|edema leve",
  "Refiere inicio de un medicamento nuevo.|Refiere ingesta de alimentos poco habituales.|Refiere contacto con productos químicos.|Refiere cuadro viral previo.|Refiere picadura de insectos.",
  "Tomó antihistamínico con alivio parcial.|Se aplicó crema con corticoide sin mejoría.|No ha recibido tratamiento.",
  "dificultad respiratoria|edema de labios o lengua|fiebre alta|lesiones en mucosas|ampollas|petequias", dur="A")
G(123, "puerperio de 1 semana tras parto vaginal con sangrado escaso|puerperio de 2 semanas con lactancia materna exclusiva|puerperio de 3 semanas tras cesárea con molestia en la herida|puerperio de 40 días que acude a control posparto",
  "loquios escasos|molestia en episiorrafia|molestia en herida quirúrgica|cansancio|lactancia materna exclusiva|ingurgitación mamaria",
  "Refiere parto en hospital sin complicaciones.|Refiere parto por cesárea.|Refiere que el bebé está sano y se alimenta bien.|Refiere que desea iniciar un método anticonceptivo.",
  "No ha recibido tratamiento.|Toma hierro y vitaminas.|Ya recibió control a los 7 días.",
  "fiebre|sangrado abundante|loquios malolientes|dolor abdominal intenso|dolor en pantorrilla|tristeza persistente", dur="-")
G(124, "congestión nasal, rinorrea amarillenta y dolor en región maxilar|dolor facial con obstrucción nasal y secreción espesa|cefalea frontal con congestión nasal y goteo posterior|dolor y presión en mejillas que empeora al inclinar la cabeza|secreción nasal purulenta con tos nocturna|rinorrea verdosa con dolor facial",
  "dolor maxilar|cefalea frontal|goteo posterior|tos nocturna|halitosis|hiposmia|fiebre baja",
  "Refiere cuadro gripal previo.|Refiere episodios previos de sinusitis.|Refiere antecedente de rinitis alérgica.|Refiere exposición a aire frío.",
  TXB, "fiebre alta|edema periorbitario|alteración visual|rigidez de cuello|cefalea intensa|vómitos", dur="B")
G(125, "acude a control con congestión nasal persistente|refiere secreción nasal espesa y goteo posterior de larga data|refiere dolor y presión facial recurrentes|refiere hiposmia con cefalea frontal|refiere obstrucción nasal permanente",
  "hiposmia|goteo posterior|cefalea frontal|tos crónica|halitosis|presión facial",
  "Refiere múltiples episodios de sinusitis.|Refiere antecedente de rinitis alérgica.|Refiere exposición a polvo o humo.|Refiere desviación del tabique.",
  "en tratamiento con lavados nasales|con tratamiento intermitente con antihistamínicos|en seguimiento por otorrinolaringología",
  "fiebre alta|edema periorbitario|alteración visual|sangrado nasal|cefalea intensa", dur="Y")
G(126, "embarazo de {w} semanas por fecha de última menstruación que acude a control prenatal|embarazo de {w} semanas con control prenatal sin molestias|embarazo de {w} semanas con náuseas y fatiga leve|embarazo de {w} semanas con movimientos fetales presentes|embarazo de {w} semanas con lumbalgia leve",
  "náuseas|fatiga|lumbalgia leve|acidez|movimientos fetales presentes|edema leve de miembros inferiores|insomnio",
  "Refiere controles prenatales previos al día.|Refiere que es su primer embarazo.|Refiere embarazos previos sin complicaciones.|Refiere que trae resultados de ultrasonido.",
  "Toma ácido fólico y sulfato ferroso.|Recibió vacuna antitetánica.",
  "sangrado vaginal|pérdida de líquido|cefalea intensa|visión borrosa|contracciones regulares|disuria|disminución de movimientos fetales", dur="8 semanas|12 semanas|16 semanas|20 semanas|24 semanas|28 semanas|32 semanas|36 semanas")
G(127, "dolor abdominal tipo cólico que mejora con la evacuación|dolor abdominal con alternancia de diarrea y estreñimiento|distensión abdominal y cólicos recurrentes|dolor abdominal con moco en las heces|cólico abdominal postprandial con urgencia para evacuar",
  "distensión abdominal|flatulencia|diarrea|estreñimiento|moco en las heces|urgencia evacuatoria|sensación de evacuación incompleta",
  "Refiere que los síntomas empeoran con el estrés.|Refiere episodios similares desde hace años.|Refiere intolerancia a algunos alimentos.|Refiere ansiedad.",
  TXN, "sangre en heces|pérdida de peso|fiebre|anemia|despertares nocturnos por diarrea|antecedente familiar de cáncer de colon", dur="L")
G(128, "prurito y descamación entre los dedos de los pies|piel macerada y fisurada en espacios interdigitales|prurito, mal olor y descamación en plantas|lesiones descamativas en pie con picazón|grietas dolorosas entre los dedos del pie",
  "mal olor|maceración|fisuras|descamación|ampollas pequeñas|prurito",
  "Refiere uso de calzado cerrado por muchas horas.|Refiere sudoración excesiva en los pies.|Refiere uso de duchas públicas.|Refiere humedad frecuente en los pies.|Refiere diabetes mellitus.",
  "Se aplicó crema antimicótica con mejoría parcial.|Se aplicó talco sin mejoría.|No ha recibido tratamiento.",
  "fiebre|dolor intenso|secreción purulenta|enrojecimiento que asciende por la pierna|lesiones en uñas", dur="B")
G(129, "tos seca persistente|tos irritativa de predominio nocturno|tos seca con cosquilleo en la garganta|tos de varios días que empeora al acostarse|tos con carraspeo y ronquera leve|tos seca en accesos",
  "cosquilleo en la garganta|ronquera|congestión nasal|goteo posterior|carraspeo|odinofagia leve",
  "Refiere cuadro gripal previo.|Refiere exposición a humo o polvo.|Refiere tabaquismo.|Refiere reflujo ácido.|Refiere antecedente de rinitis alérgica.|Refiere uso de enalapril.",
  TXA + "|Tomó infusiones calientes con alivio parcial.", "fiebre|disnea|esputo con sangre|dolor torácico|pérdida de peso|sibilancias", dur="B")
G(130, "prurito generalizado sin lesiones primarias|prurito intenso que empeora por la noche|picazón en todo el cuerpo con piel seca|prurito con lesiones por rascado|comezón difusa sin erupción visible",
  "piel seca|lesiones por rascado|insomnio|ardor leve|enrojecimiento|descamación fina",
  "Refiere uso de jabones agresivos.|Refiere baños con agua muy caliente.|Refiere inicio de medicamentos nuevos.|Refiere diabetes mellitus o enfermedad renal.|Refiere estrés reciente.",
  "Se aplicó crema hidratante con alivio parcial.|Tomó antihistamínico con alivio parcial.|No ha recibido tratamiento.",
  "ictericia|fiebre|pérdida de peso|erupción diseminada|dificultad respiratoria|sudoración nocturna", dur="B")
G(131, "visión borrosa de lejos|dificultad para ver el pizarrón o carteles|molestia ocular con cefalea al leer|entrecierra los ojos para ver de lejos|visión borrosa con cefalea frontal al final del día",
  "cefalea frontal|fatiga visual|ardor ocular|lagrimeo|entrecerrar los ojos|dificultad para leer",
  "Refiere uso prolongado de pantallas.|Refiere que no se ha hecho examen visual hace años.|Refiere antecedente familiar de miopía.|Refiere que usa lentes que ya no le sirven.",
  "No ha recibido tratamiento.|Usa lentes con graduación antigua.",
  "pérdida súbita de visión|dolor ocular|destellos luminosos|diplopía|trauma ocular", dur="L")
G(132, "dificultad para pronunciar algunos sonidos|lenguaje poco claro para su edad|vocabulario reducido para su edad|dificultad para formar frases completas|habla con sustitución de sonidos",
  "tartamudeo|poca comprensión de su lenguaje por otras personas|retraso en el vocabulario|dificultad en la escuela|timidez al hablar",
  "La madre refiere que habla poco comparado con otros niños.|La madre refiere antecedente familiar de retraso del lenguaje.|La madre refiere infecciones de oído frecuentes.|La madre refiere uso excesivo de pantallas.",
  "No ha recibido terapia de lenguaje.|Recibió orientación previa sin continuidad.",
  "pérdida de habilidades previas|hipoacusia|convulsiones|dificultad para comprender órdenes|fiebre", dur="L")
G(133, "cansancio y disnea de esfuerzo posteriores a COVID-19|fatiga persistente tras la infección por COVID-19|disnea al subir escaleras después de haber tenido COVID-19|tos persistente y fatiga tras COVID-19|dificultad para concentrarse y cansancio posteriores a COVID-19",
  "fatiga|disnea de esfuerzo|dificultad para concentrarse|palpitaciones|dolor articular|pérdida del olfato|tos persistente|insomnio",
  "Refiere que tuvo COVID-19 hace varias semanas.|Refiere que no ha recuperado su capacidad de trabajo.|Refiere que requirió hospitalización por COVID-19.|Refiere cuadro leve de COVID-19 en casa.",
  "No ha recibido tratamiento.|Ha tomado vitaminas sin mejoría.",
  "fiebre|dolor torácico|saturación baja referida|hemoptisis|edema de piernas|síncope", dur="L")
G(134, "traumatismo craneal reciente con cefalea|golpe en la cabeza con dolor y aumento de volumen local|caída con trauma en cabeza y mareo|trauma craneal leve sin pérdida del conocimiento|cefalea y náuseas tras golpe en la cabeza",
  "cefalea|mareo|náuseas|aumento de volumen local|herida en cuero cabelludo|somnolencia|vómito único",
  "Refiere caída desde su propia altura.|Refiere accidente de tránsito.|Refiere golpe durante el juego.|Refiere que ocurrió hace pocas horas.|Refiere agresión física.",
  "Se aplicó hielo local.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "pérdida del conocimiento|vómitos repetidos|convulsiones|salida de líquido por oídos o nariz|alteración visual|confusión", dur="H")
G(135, "dolor y aumento de volumen tras un golpe|contusión con edema y dolor localizado|dolor y hematoma tras traumatismo|dolor local con limitación del movimiento tras trauma|dolor intenso con equimosis posterior a una caída",
  "edema local|equimosis|dolor al movimiento|limitación funcional|sensibilidad local",
  "Refiere caída reciente.|Refiere accidente deportivo.|Refiere golpe con un objeto.|Refiere accidente laboral.",
  "Se aplicó hielo con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|pérdida de sensibilidad|herida abierta|imposibilidad de mover la zona|fiebre|sangrado importante", dur="A")
G(136, "aumento de volumen abdominal progresivo|sensación de masa en abdomen con distensión|pesadez pélvica y aumento del perímetro abdominal|masa abdominal palpable por la paciente|distensión abdominal con saciedad temprana",
  "saciedad temprana|dolor leve|estreñimiento|polaquiuria|pérdida de peso|fatiga",
  "Refiere que el aumento de volumen ha progresado.|Refiere antecedente familiar de neoplasias.|Refiere que no ha tenido estudios de imagen recientes.|Refiere ciclos menstruales irregulares.",
  "No ha recibido tratamiento.|Se realizó ultrasonido previo.",
  "fiebre|vómitos|ictericia|pérdida de peso importante|sangrado digestivo|sangrado vaginal anormal", dur="L")
G(137, "flujo vaginal amarillento con prurito y ardor|flujo vaginal abundante con mal olor|secreción vaginal blanca grisácea con prurito|ardor y enrojecimiento vulvar con flujo espeso|flujo vaginal verdoso espumoso con irritación|flujo vaginal con dispareunia",
  "mal olor|prurito vulvar|ardor al orinar|dispareunia|enrojecimiento vulvar|molestia pélvica leve",
  "Refiere relaciones sexuales sin protección.|Refiere uso reciente de antibióticos.|Refiere uso de lavados vaginales.|Refiere episodios similares previos.|Refiere cambio reciente de pareja.|Refiere uso de ropa interior sintética.",
  "Se aplicó óvulos sin receta con alivio parcial.|Utilizó lavados vaginales sin mejoría.|No ha recibido tratamiento.",
  "fiebre|dolor pélvico|sangrado vaginal anormal|úlceras genitales|dolor abdominal bajo", dur="A")
G(138, "lesiones verrugosas en región genital|verrugas en pene, vulva o región perianal|aumento de volumen blando con aspecto de coliflor en genitales|lesiones papilomatosas indoloras en zona genital|crecimiento de pequeñas verrugas genitales de forma progresiva",
  "prurito leve|molestia al roce|sangrado ocasional de las lesiones|aumento progresivo de las lesiones|lesiones múltiples",
  "Refiere relaciones sexuales sin protección.|Refiere nueva pareja sexual.|Refiere pareja con lesiones similares.|Refiere antecedente de infecciones de transmisión sexual.",
  "No ha recibido tratamiento.|Se aplicó remedios caseros sin mejoría.|Se aplicó productos sin receta sin mejoría.",
  "fiebre|dolor intenso|secreción uretral o vaginal|úlceras genitales|pérdida de peso", dur="L")
G(139, "ardor, enrojecimiento y prurito vulvar|edema y dolor vulvar con ardor al orinar|enrojecimiento vulvar con sensación de quemazón|vulva edematosa y dolorosa con prurito|irritación vulvar con flujo escaso",
  "ardor al orinar|dispareunia|flujo escaso|fisuras vulvares|edema vulvar|dolor al sentarse",
  "Refiere uso de jabones o productos perfumados.|Refiere uso de ropa ajustada.|Refiere uso reciente de antibióticos.|Refiere relaciones sexuales recientes.|Refiere diabetes mellitus.",
  "Se aplicó crema con corticoide con alivio parcial.|Se aplicó óvulos o crema vaginal sin receta.|No ha recibido tratamiento.",
  "fiebre|úlceras genitales|sangrado vaginal|dolor pélvico|flujo con mal olor", dur="A")
G(140, "lesión elevada en piel de mejilla de crecimiento lento|lesión pigmentada que ha cambiado de tamaño|nódulo cutáneo indoloro de aparición reciente|mancha en piel con bordes irregulares|lesión en piel que sangra al roce",
  "sangrado al roce|prurito local|cambio de color|costra|crecimiento progresivo|ulceración leve",
  "Refiere exposición solar crónica.|Refiere antecedente familiar de cáncer de piel.|Refiere que la lesión creció en los últimos meses.|Refiere que se rasca la lesión con frecuencia.",
  "No ha recibido tratamiento.|Se aplicó pomadas caseras sin cambios.",
  "dolor intenso|fiebre|adenopatías|pérdida de peso|lesiones similares en otras zonas", dur="L")
