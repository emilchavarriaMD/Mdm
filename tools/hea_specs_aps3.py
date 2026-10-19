from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
CONT = "Refiere contacto con personas con cuadro similar.|Refiere asistencia a guardería o escuela con casos similares.|Refiere cambios bruscos de temperatura en los últimos días.|Refiere convivencia con familiares enfermos."

G(17, "rinorrea y tos de varios días con respiración ruidosa|tos con silbidos en el pecho y dificultad para alimentarse|congestión nasal y tos que ha progresado a respiración rápida|rinorrea hialina, tos y sibilancias audibles|dificultad para respirar con tiraje leve y rechazo de las tomas",
  "fiebre|rechazo de las tomas|irritabilidad|vómitos posteriores a la tos|respiración rápida|sibilancias|tiraje intercostal leve|disminución de la actividad",
  "Según refiere la madre, hay hermanos con cuadro respiratorio.|Según refiere la madre, asiste a guardería.|Según refiere la madre, el niño nació a término.|La madre refiere que en casa hay exposición a humo de leña o cigarrillo.",
  "La madre le administró acetaminofén con alivio parcial.|La madre realizó lavados nasales con solución salina.|No ha recibido tratamiento.",
  "cianosis|pausas respiratorias|rechazo total de las tomas|convulsiones|fiebre alta persistente|somnolencia marcada", dur="A")
G(18, "tos productiva con expectoración mucosa|tos con flemas amarillentas y molestia retroesternal|tos persistente con expectoración y ronquera|tos con expectoración blanquecina y malestar general|tos productiva de predominio matutino|tos con silbidos en el pecho y esputo mucoso",
  "expectoración mucosa|molestia retroesternal|fiebre baja|malestar general|congestión nasal|odinofagia|sibilancias leves|cefalea",
  CONT + "|Refiere tabaquismo.|Refiere exposición a humo de leña.",
  TXA, "disnea importante|dolor torácico|fiebre alta|esputo con sangre|pérdida de peso|sudoración nocturna", dur="B")
G(19, "fiebre, tos seca y malestar general|fiebre, cefalea y pérdida del olfato y del gusto|tos seca, odinofagia y mialgias|fiebre y dolor de cuerpo con congestión nasal|fatiga intensa y tos seca de varios días",
  "anosmia|ageusia|cefalea|mialgias|odinofagia|congestión nasal|diarrea|fatiga intensa|escalofríos",
  "Refiere contacto cercano con un caso confirmado de COVID-19.|Refiere asistencia a reuniones con muchas personas.|Refiere que no está vacunada/o contra COVID-19.|Refiere esquema de vacunación completo.",
  TXA, "dificultad respiratoria|dolor torácico|saturación baja referida|vómitos persistentes|confusión|cianosis", dur="A")
G(20, "nódulo indoloro en el párpado de crecimiento lento|tumefacción redondeada y firme en el borde del párpado|nódulo en párpado superior sin dolor ni enrojecimiento intenso|aumento de volumen palpebral que persiste desde hace semanas",
  "sensación de cuerpo extraño|molestia al parpadear|visión borrosa leve|lagrimeo|enrojecimiento leve del párpado|pesadez palpebral",
  "Refiere episodios previos de orzuelo.|Refiere uso de maquillaje en los párpados.|Refiere que se frota los ojos con frecuencia.|Refiere piel grasa.",
  "Aplicó compresas tibias con alivio leve.|No ha recibido tratamiento.|Se aplicó gotas oftálmicas sin mejoría.",
  "dolor intenso|fiebre|disminución de la visión|secreción purulenta|edema facial", dur="B")
G(22, "dolor dental al masticar y con el frío o lo dulce|odontalgia con cavidad visible en una pieza|dolor dental intermitente que empeora al ingerir alimentos dulces|pieza dental con cavidad y sensibilidad|dolor dental nocturno que cede parcialmente con analgésicos",
  "sensibilidad a lo frío y lo caliente|mal sabor de boca|halitosis|fractura de una pieza dental|dolor al cepillado|edema de encía leve",
  "Refiere higiene bucal irregular.|Refiere alto consumo de azúcares.|Refiere que no acude al odontólogo desde hace años.|Refiere antecedente de caries múltiples.",
  TXA, "fiebre|edema facial|dificultad para abrir la boca|dificultad para tragar|salida de pus", dur="B")
G(23, "cefalea holocraneana de intensidad moderada|cefalea opresiva bilateral que empeora al final del día|cefalea frontal con sensación de peso|dolor de cabeza pulsátil de predominio temporal|cefalea occipital con tensión cervical|dolor de cabeza intermitente que cede con analgésicos",
  "tensión en cuello y hombros|fotofobia|náuseas|mareo|fatiga|insomnio|sensación de presión en la cabeza",
  "Refiere estrés laboral o familiar.|Refiere pocas horas de sueño.|Refiere uso prolongado de pantallas.|Refiere que ha omitido comidas.|Refiere consumo bajo de agua.|Refiere antecedente familiar de migraña.",
  TXA + "|Descansó en un lugar oscuro con alivio parcial.", "fiebre|vómitos en proyectil|déficit motor|alteraciones visuales|rigidez de cuello|pérdida del conocimiento|trauma craneal reciente", dur="A")
G(24, "enrojecimiento, calor y dolor en la piel de una extremidad|placa eritematosa caliente, dolorosa y bien delimitada en pierna|aumento de volumen y eritema en miembro inferior con dolor al tacto|eritema de bordes elevados con dolor y edema local|piel de pierna enrojecida, caliente y tensa|dolor y enrojecimiento que avanzan de forma progresiva",
  "calor local|edema del miembro|fiebre|escalofríos|dolor al caminar|adenopatías inguinales dolorosas|malestar general",
  "Refiere pequeña herida o grieta entre los dedos previa.|Refiere picadura de insecto en la zona.|Refiere antecedente de insuficiencia venosa.|Refiere diabetes mellitus.|Refiere episodios similares previos.|Refiere pie de atleta.",
  TXB, "dificultad respiratoria|vómitos|ampollas con sangre|dolor desproporcionado|confusión|fiebre alta persistente", dur="A")
G(25, "sensación de oído tapado con hipoacusia|disminución de la audición con sensación de plenitud ótica|oído tapado y molestia leve que dificulta oír|hipoacusia leve y comezón en el conducto auditivo",
  "prurito en el oído|acúfenos|autofonía|mareo leve|molestia al manipular el oído",
  "Refiere uso de hisopos en el oído.|Refiere uso de audífonos con frecuencia.|Refiere haber entrado al agua recientemente.|Refiere episodios previos de cerumen.",
  "Se aplicó gotas caseras sin mejoría.|Se limpió el oído con hisopo sin resultado.|No ha recibido tratamiento.",
  "dolor intenso|secreción por el oído|fiebre|vértigo intenso|sangrado|trauma ótico", dur="B")
G(26, "dolor lumbar que se irradia a glúteo y cara posterior de la pierna|lumbalgia con dolor tipo corriente que baja por el miembro inferior|dolor lumbar intenso con parestesias hacia el pie|dolor en nalga y pierna que empeora al sentarse o toser|dolor lumbar irradiado con sensación de adormecimiento",
  "parestesias en el miembro inferior|dolor al toser|limitación para inclinarse|debilidad leve en el pie|rigidez lumbar|dolor nocturno",
  "Refiere que cargó un objeto pesado antes del inicio.|Refiere trabajo con posturas prolongadas o carga de peso.|Refiere episodios similares previos.|Refiere sedentarismo.|Refiere sobrepeso.",
  TXA + "|Aplicó calor local con alivio parcial.", "pérdida del control de esfínteres|debilidad progresiva de la pierna|adormecimiento en silla de montar|fiebre|pérdida de peso", dur="B")
G(27, "enrojecimiento ocular con secreción amarillenta|ojo rojo con legañas que pegan los párpados al despertar|secreción mucopurulenta con sensación de arenilla|ojo rojo con lagrimeo y párpados adheridos por las mañanas|enrojecimiento y secreción amarillenta en uno o ambos ojos",
  "legañas matutinas|sensación de arenilla|ardor ocular|prurito|edema palpebral|lagrimeo|fotofobia leve",
  "Refiere contacto con personas con conjuntivitis.|Refiere uso de lentes de contacto.|Refiere exposición a polvo o humo.|Refiere que se frotó los ojos con las manos sucias.",
  "Se aplicó gotas oftálmicas sin receta con alivio parcial.|Se lavó los ojos con infusiones caseras.|No ha recibido tratamiento.",
  "disminución de la visión|dolor ocular intenso|fotofobia marcada|trauma ocular|fiebre", dur="A")
G(28, "enrojecimiento ocular con ardor y lagrimeo|ojo rojo con sensación de cuerpo extraño|prurito ocular intenso con enrojecimiento|enrojecimiento en ambos ojos con secreción acuosa|ojo rojo con párpados edematosos|molestia ocular con ardor y enrojecimiento",
  "lagrimeo|prurito|ardor|sensación de cuerpo extraño|fotofobia leve|edema palpebral|secreción acuosa",
  "Refiere contacto con personas con cuadro similar.|Refiere exposición a polvo, humo o polen.|Refiere antecedente de alergias.|Refiere uso de lentes de contacto.",
  "Se aplicó lágrimas artificiales con alivio parcial.|Se lavó con infusiones caseras sin mejoría.|No ha recibido tratamiento.",
  "disminución de la visión|dolor ocular intenso|trauma ocular|secreción purulenta abundante|fiebre", dur="A")
G(29, "dificultad para evacuar con heces duras y secas|evacuaciones cada 3 a 4 días con esfuerzo|distensión abdominal y sensación de evacuación incompleta|heces en bolitas con dolor al defecar|estreñimiento persistente con malestar abdominal",
  "dolor al defecar|distensión abdominal|sensación de evacuación incompleta|esfuerzo excesivo|flatulencia|sangrado escaso rojo brillante|hiporexia",
  "Refiere dieta baja en fibra y escaso consumo de agua.|Refiere sedentarismo.|Refiere cambios recientes de rutina o de dieta.|Refiere uso de analgésicos o hierro.|Refiere que retiene las ganas de evacuar.",
  "Se automedicó con laxantes con alivio transitorio.|Tomó té de hierbas con alivio parcial.|No ha recibido tratamiento.",
  "vómitos|sangre mezclada con las heces|pérdida de peso|dolor abdominal intenso|fiebre|heces negras", dur="B")
G(31, "dolor y contractura muscular en cuello y hombros|dolor en espalda alta con sensación de tensión muscular|dolor muscular localizado con limitación para mover la zona|contractura dolorosa en región lumbar|dolor y rigidez en trapecio",
  "limitación de movimientos|dolor a la palpación|rigidez|cefalea tensional|sensación de peso|dolor nocturno al cambiar de posición",
  "Refiere postura sentada prolongada.|Refiere que cargó peso o realizó esfuerzo físico.|Refiere que durmió en mala posición.|Refiere estrés laboral.|Refiere exposición a aire frío.",
  TXA + "|Aplicó calor local con alivio parcial.", "fiebre|debilidad en las extremidades|parestesias|trauma reciente|pérdida de peso|dolor torácico", dur="A")
G(32, "dolor lumbar tipo cólico que se irradia a la región inguinal|cólico en flanco con náuseas y vómitos|dolor lumbar intenso de inicio súbito con ardor al orinar|dolor en fosa renal con inquietud y sudoración|dolor tipo cólico que baja hacia genitales",
  "náuseas|vómitos|hematuria|disuria|polaquiuria|inquietud|sudoración fría",
  "Refiere ingesta baja de líquidos.|Refiere antecedente de litiasis renal.|Refiere episodios similares previos.|Refiere antecedente familiar de cálculos.",
  TXA, "fiebre|escalofríos|anuria|dolor abdominal difuso|traumatismo lumbar|hematuria macroscópica abundante", dur="H")
G(33, "diarrea y vómitos con sed intensa y sequedad de mucosas|evacuaciones líquidas y vómitos con disminución de la orina|diarrea con vómitos y decaimiento|vómitos frecuentes con intolerancia a la vía oral y boca seca|diarrea abundante con mareo y debilidad",
  "sed intensa|boca seca|mareo|debilidad|disminución de la diuresis|calambres|llanto sin lágrimas|ojos hundidos",
  "Refiere ingesta reciente de alimentos o agua de dudosa procedencia.|Refiere contacto con personas con diarrea.|Refiere calor intenso y poca ingesta de líquidos.|Refiere que ha tolerado poco la vía oral.",
  "Ha tomado suero oral con alivio parcial.|Ha tomado líquidos en pequeñas cantidades.|No ha recibido tratamiento.",
  "sangre en las heces|fiebre alta|dolor abdominal intenso|alteración del estado de conciencia|convulsiones|ausencia de orina por más de 8 horas", dur="A")
G(34, "enrojecimiento en la zona del pañal con lesiones húmedas|eritema en nalgas y genitales con lesiones satélite|lesiones eritematosas con descamación en región del pañal|zona del pañal enrojecida y dolorosa con irritación|eritema en pliegues inguinales y glúteos con pequeñas pústulas",
  "irritabilidad al cambio de pañal|llanto al contacto|descamación|pápulas satélite|lesiones erosionadas",
  "Según refiere la madre, usa pañales desechables que cambia con poca frecuencia.|Según refiere la madre, hay antecedente de diarrea reciente.|Según refiere la madre, ha cambiado de marca de pañal.|La madre refiere uso de toallitas húmedas con alcohol.",
  "La madre aplicó crema con óxido de zinc con alivio parcial.|La madre aplicó talco sin mejoría.|No ha recibido tratamiento.",
  "fiebre|lesiones en otras partes del cuerpo|rechazo del alimento|sangrado|diarrea persistente", dur="A", u="meses")
G(35, "lesiones eritematosas y pruriginosas en la piel|placas secas, descamativas y pruriginosas en pliegues|eritema con vesículas y prurito intenso|piel seca con prurito que empeora por la noche|lesiones liquenificadas por rascado crónico|erupción eccematosa en manos con descamación",
  "prurito intenso|descamación|resequedad de la piel|vesículas|costras|liquenificación|ardor local",
  "Refiere contacto con jabones, detergentes o productos químicos.|Refiere antecedente de atopia o rinitis.|Refiere estrés reciente.|Refiere que las lesiones empeoran con el calor o el sudor.|Refiere episodios similares previos.",
  "Se aplicó crema hidratante con alivio parcial.|Se aplicó crema con corticoide con mejoría transitoria.|Tomó antihistamínico con alivio leve.|No ha recibido tratamiento.",
  "fiebre|secreción purulenta|dolor intenso|lesiones en mucosas|compromiso de otros miembros de la familia", dur="B")
G(36, "lesión circular pruriginosa con borde elevado y centro más claro|placas anulares eritematosas y descamativas|lesión pruriginosa en forma de anillo que ha crecido de forma progresiva|manchas redondeadas con borde activo y prurito|lesión descamativa en cuero cabelludo con caída del cabello|prurito y descamación en ingle",
  "prurito|descamación|crecimiento centrífugo de la lesión|alopecia local|eritema|lesiones satélite",
  "Refiere contacto con mascotas.|Refiere sudoración abundante y humedad en la zona.|Refiere contacto con personas con lesiones similares.|Refiere uso de ropa ajustada.",
  "Se aplicó crema antimicótica sin mejoría.|Se aplicó crema con corticoide con mejoría transitoria.|No ha recibido tratamiento.",
  "fiebre|dolor intenso|secreción purulenta|lesiones en uñas|diabetes mellitus", dur="B")
G(37, "pérdida de peso progresiva con hiporexia|disminución del peso y de la masa muscular|ropa que le queda holgada con cansancio|pérdida de peso no intencionada con astenia|bajo peso con ingesta insuficiente de alimentos",
  "hiporexia|astenia|debilidad|caída del cabello|palidez|apatía|diarrea ocasional",
  "Refiere ingesta insuficiente por problemas económicos.|Refiere dieta monótona y poco variada.|Refiere antecedente de parasitosis.|Refiere estrés o duelo reciente.",
  "No ha recibido tratamiento.|Tomó multivitamínicos sin mejoría.|Ha cambiado su dieta sin resultado.",
  "fiebre|sudoración nocturna|tos persistente|vómitos|diarrea crónica|dificultad para tragar", dur="L")
G(38, "acude a control sin molestias y con cifras de glucemia adecuadas|refiere poliuria, polidipsia y pérdida de peso en las últimas semanas|acude a control con cifras de glucemia elevadas|refiere hormigueo en los pies y visión borrosa|acude a control con glucemias en ayunas elevadas por poca adherencia a la dieta|acude a control refiriendo buena adherencia al tratamiento",
  "poliuria|polidipsia|polifagia|visión borrosa|parestesias en pies|fatiga|infecciones frecuentes",
  "Refiere que no ha realizado actividad física regular.|Refiere dieta con alto consumo de carbohidratos.|Refiere que omite dosis del medicamento con frecuencia.|Refiere antecedente familiar de diabetes.|Refiere que realiza automonitoreo de glucosa.",
  "en tratamiento con metformina 850 mg dos veces al día|en tratamiento con metformina y glibenclamida|en tratamiento con insulina NPH|en tratamiento con metformina y dieta|con tratamiento irregular",
  "dolor torácico|heridas que no cicatrizan|vómitos|dolor abdominal|pérdida del conocimiento|episodios de hipoglucemia", dur="Y")
G(39, "evacuaciones líquidas abundantes con dolor abdominal tipo cólico|diarrea acuosa con náuseas y malestar general|evacuaciones líquidas de 4 a 6 veces al día|deposiciones blandas y frecuentes con dolor abdominal|diarrea con vómitos y fiebre baja|evacuaciones diarreicas con moco",
  "dolor abdominal tipo cólico|náuseas|vómitos|fiebre|moco en las heces|pujo y tenesmo|hiporexia|sed",
  "Refiere ingesta de alimentos en la calle.|Refiere consumo de agua no tratada.|Refiere contacto con personas con diarrea.|Refiere viaje reciente.|Refiere ingesta reciente de lácteos o mariscos.",
  "Ha tomado suero oral con alivio parcial.|Se automedicó con antidiarreicos sin mejoría.|No ha recibido tratamiento.",
  "sangre en las heces|fiebre alta|deshidratación importante|dolor abdominal intenso|vómitos persistentes|heces negras", dur="A")
G(40, "ronquera y voz apagada|disfonía con tos seca|pérdida parcial de la voz tras esfuerzo vocal|voz ronca con carraspeo persistente|voz quebrada con odinofagia leve",
  "carraspeo|tos seca|odinofagia leve|sensación de cuerpo extraño en la garganta|fatiga vocal",
  "Refiere uso intenso de la voz por su trabajo.|Refiere cuadro gripal previo.|Refiere que grita con frecuencia.|Refiere tabaquismo.|Refiere reflujo ácido.",
  "Ha guardado reposo vocal con alivio parcial.|Tomó infusiones calientes sin mejoría.|No ha recibido tratamiento.",
  "dificultad para respirar|dificultad para tragar|estridor|fiebre|pérdida de peso|hemoptisis", dur="B")
