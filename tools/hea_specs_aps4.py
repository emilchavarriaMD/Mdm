from hea_gen import G
TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."
CONT = "Refiere contacto con personas con cuadro similar.|Refiere asistencia a guardería o escuela con casos similares.|Refiere cambios bruscos de temperatura en los últimos días.|Refiere convivencia con familiares enfermos."

G(21, "prurito vulvar intenso con flujo blanquecino grumoso|flujo vaginal espeso, blanco, sin mal olor, con prurito|ardor y picazón vulvar con enrojecimiento|flujo vaginal en «queso cottage» con molestia al orinar|prurito vulvovaginal que empeora por la noche|dispareunia con irritación vulvar y flujo blanquecino",
  "enrojecimiento vulvar|ardor al orinar|dispareunia superficial|edema vulvar leve|fisuras vulvares|flujo sin mal olor",
  "Refiere uso reciente de antibióticos.|Refiere episodios similares previos.|Refiere diabetes mellitus.|Refiere uso de ropa interior sintética ajustada.|Refiere embarazo actual.|Refiere relaciones sexuales recientes.",
  "Se aplicó óvulos o crema vaginal sin receta con alivio parcial.|Utilizó lavados vaginales caseros sin mejoría.|No ha recibido tratamiento.",
  "fiebre|dolor pélvico|sangrado vaginal anormal|flujo con mal olor|úlceras genitales|dolor abdominal bajo", dur="A")
G(45, "dolor articular de predominio en rodillas o tobillos|dolor en articulaciones con limitación para la marcha|dolor articular que empeora con el movimiento|dolor en hombro y codo al elevar el brazo|dolor y rigidez en una articulación tras el reposo|dolor articular migratorio",
  "edema articular|rigidez matutina|limitación del movimiento|crujidos|sensación de calor local|fatiga",
  "Refiere sobrecarga o esfuerzo físico reciente.|Refiere trabajo con movimientos repetitivos.|Refiere antecedente de trauma en la articulación.|Refiere sobrepeso.|Refiere episodios similares previos.",
  TXA, "fiebre|enrojecimiento marcado de la articulación|deformidad|trauma reciente|bloqueo articular|erupción en la piel", dur="B")
G(46, "dolor abdominal difuso de intensidad moderada|dolor en hipogastrio tipo cólico|dolor abdominal con distensión y flatulencia|dolor pélvico de predominio nocturno|dolor abdominal que mejora con la evacuación|dolor en bajo vientre con náuseas",
  "náuseas|distensión abdominal|flatulencia|diarrea|estreñimiento|hiporexia|sensación de llenura|malestar general",
  "Refiere ingesta reciente de alimentos irritantes o grasosos.|Refiere estrés reciente.|Refiere cambios en el patrón de evacuación.|Refiere menstruación próxima o reciente.",
  TXA, "fiebre|vómitos persistentes|sangrado vaginal anormal|sangre en heces|dolor de aparición súbita muy intenso|pérdida de peso", dur="A")
G(47, "ardor retroesternal postprandial|acidez y regurgitación ácida con sabor amargo|ardor que sube desde el estómago hasta la garganta|dolor epigástrico con eructos frecuentes|pirosis nocturna que empeora al acostarse|sensación de reflujo con tos nocturna",
  "regurgitación ácida|eructos frecuentes|disfonía matutina|tos nocturna|sabor amargo en la boca|sensación de nudo en la garganta|náuseas",
  "Refiere comidas copiosas y tardías.|Refiere consumo frecuente de café, picantes o grasas.|Refiere sobrepeso.|Refiere tabaquismo o consumo de alcohol.|Refiere que se acuesta justo después de cenar.",
  "Tomó antiácidos con alivio parcial.|Tomó omeprazol de forma intermitente con mejoría.|No ha recibido tratamiento.",
  "dificultad para tragar|vómitos con sangre|heces negras|pérdida de peso|dolor torácico opresivo|anemia conocida", dur="B")
G(48, "acude a control sin molestias y con buena adherencia al tratamiento antirretroviral|acude a control refiriendo toma irregular de los antirretrovirales|acude a control con pérdida de peso y diarrea intermitente|acude a control refiriendo fatiga y fiebre vespertina de varias semanas|acude por entrega de medicamentos con buena tolerancia al esquema",
  "pérdida de peso|candidiasis oral|diarrea crónica|fiebre vespertina|tos persistente|lesiones en piel|fatiga",
  "Refiere que sus cargas virales han estado indetectables.|Refiere que ha omitido dosis por trabajo o viajes.|Refiere que asiste a su clínica de seguimiento.|Refiere apoyo familiar.",
  "en tratamiento antirretroviral",
  "fiebre persistente|tos con expectoración|sudoración nocturna|diarrea de más de 2 semanas|lesiones orales|cefalea intensa", dur="Y")
G(49, "dolor y edema en el tobillo tras un movimiento de inversión del pie|dolor en tobillo con dificultad para apoyar el pie|edema y equimosis en tobillo posterior a una torcedura|dolor lateral del tobillo al caminar|inflamación del tobillo tras caída|dolor y limitación para el apoyo posterior a un esguince",
  "edema local|equimosis|dolor a la palpación|limitación para el apoyo|sensación de inestabilidad|dolor al movilizar el pie",
  "Refiere que se torció el pie jugando fútbol.|Refiere que se torció el pie al bajar un escalón.|Refiere que usaba calzado inadecuado.|Refiere esguinces previos en el mismo pie.|Refiere que cayó al caminar en terreno irregular.",
  "Se aplicó hielo local con alivio parcial.|Se vendó el tobillo con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "deformidad|incapacidad total para apoyar|parestesias|herida abierta|dolor en el hueso del tobillo a la palpación", dur="A")
G(50, "acude a control sin crisis convulsivas recientes|refiere crisis convulsivas ocasionales por omisión del medicamento|acude a control con buena adherencia al anticonvulsivante|refiere una crisis convulsiva en el último mes|acude por entrega de medicamento sin crisis recientes",
  "somnolencia|mareo|pérdida de memoria|irritabilidad|aura previa a las crisis|cefalea postcrisis",
  "Refiere que omite dosis del medicamento.|Refiere que la última crisis fue tras desvelo.|Refiere que su familia le ayuda con la toma del medicamento.|Refiere consumo de alcohol.",
  "en tratamiento con carbamazepina|en tratamiento con ácido valproico|en tratamiento con fenitoína|en tratamiento con fenobarbital|con tratamiento irregular",
  "pérdida de control de esfínteres|lesiones durante las crisis|fiebre|cefalea intensa|déficit neurológico|crisis de más de 5 minutos", dur="Y")
G(51, "prurito intenso de predominio nocturno|lesiones papulares pruriginosas en espacios interdigitales|prurito en muñecas, axilas y cintura|erupción con costras y trayectos lineales pruriginosos|prurito intenso con varios convivientes afectados",
  "lesiones por rascado|pápulas en pliegues|trayectos lineales en muñecas|costras|insomnio por el prurito|prurito en genitales",
  "Refiere que varios miembros de la familia tienen prurito.|Refiere contacto con personas con sarna.|Refiere convivencia en espacios hacinados.|Refiere que comparte ropa o cama.",
  "Se aplicó cremas con corticoides sin mejoría.|Tomó antihistamínicos sin alivio.|No ha recibido tratamiento.",
  "fiebre|pústulas con pus|dolor intenso|lesiones en cara|secreción", dur="B")
G(52, "dolor en talón al apoyar los primeros pasos de la mañana|dolor en planta del talón que mejora al caminar|dolor punzante en el talón al estar de pie por periodos prolongados|dolor en talón que empeora al final del día|talalgia con dolor a la palpación de la planta",
  "dolor matutino|dolor a la palpación del talón|rigidez plantar|dolor tras el reposo|cansancio en los pies",
  "Refiere que pasa muchas horas de pie.|Refiere sobrepeso.|Refiere calzado sin soporte.|Refiere actividad deportiva reciente.|Refiere pie plano.",
  "Utiliza plantillas con alivio parcial.|Tomó analgésicos con alivio parcial.|No ha recibido tratamiento.",
  "trauma reciente|edema marcado|fiebre|parestesias|dolor nocturno", dur="L")
G(53, "bochornos y ausencia de menstruación|sofocos, sudoración nocturna y cambios en el ciclo menstrual|insomnio y sofocos con irritabilidad|sequedad vaginal y dispareunia con cese de menstruación|sensación de calor súbito con sudoración y palpitaciones|menstruaciones irregulares con síntomas vasomotores",
  "sudoración nocturna|insomnio|irritabilidad|sequedad vaginal|dispareunia|disminución del deseo sexual|palpitaciones|dolor articular",
  "Refiere última menstruación hace más de 12 meses.|Refiere menstruaciones irregulares en el último año.|Refiere antecedente de histerectomía.|Refiere antecedente familiar de menopausia temprana.",
  "No ha recibido tratamiento hormonal.|Utiliza remedios naturales con alivio parcial.|No ha recibido tratamiento.",
  "sangrado vaginal posterior a la menopausia|dolor pélvico|pérdida de peso|dolor torácico|flujo anormal", dur="L")
G(54, "úlceras dolorosas en la boca|lesiones blanquecinas con halo rojo en mucosa oral|úlcera redondeada y dolorosa en la cara interna del labio|lesiones orales que dificultan comer y hablar|úlceras recurrentes en mucosa yugal",
  "dolor al comer|dolor al hablar|sensación de ardor|halo eritematoso|adenopatías cervicales|malestar general",
  "Refiere episodios similares previos.|Refiere estrés reciente.|Refiere mordedura accidental de la mucosa.|Refiere ingesta de alimentos ácidos o picantes.|Refiere alimentación pobre en frutas y verduras.",
  "Utilizó enjuagues de agua con sal con alivio parcial.|Se aplicó gel bucal sin receta.|No ha recibido tratamiento.",
  "fiebre alta|lesiones genitales|ojo rojo|dificultad para tragar|pérdida de peso|sangrado de encías", dur="A")
G(55, "talla baja para la edad|crecimiento por debajo de lo esperado según la madre|bajo peso y talla en relación con sus pares|retraso en el crecimiento notado en controles previos|escaso aumento de peso y de talla",
  "hiporexia|infecciones frecuentes|cansancio|retraso en el desarrollo|baja ganancia de peso|poco apetito",
  "Según refiere la madre, nació a término con peso adecuado.|Según refiere la madre, la dieta es poco variada.|La madre refiere que hay antecedente familiar de talla baja.|La madre refiere que es el último control de crecimiento realizado.",
  "No ha recibido tratamiento.|La madre le administra multivitamínicos.|Recibió suplementación previa sin cambios.",
  "diarrea crónica|vómitos frecuentes|fiebre|dificultad respiratoria|cefalea|alteración visual", dur="L")
G(56, "fiebre alta de inicio súbito con cefalea intensa y dolor retroocular|fiebre, mialgias y artralgias intensas|fiebre con erupción cutánea y dolor en cuerpo|fiebre de 2 a 3 días con malestar general y hiporexia|fiebre acompañada de dolor retroocular y astenia",
  "cefalea intensa|dolor retroocular|mialgias|artralgias|erupción cutánea|náuseas|vómitos|astenia",
  "Refiere que vive en zona con casos de dengue.|Refiere picaduras de zancudos.|Refiere vecinos con cuadro similar.|Refiere acumulación de agua en su domicilio.",
  "Tomó acetaminofén con alivio parcial.|Tomó ibuprofeno antes de consultar.|No ha recibido tratamiento.",
  "sangrado de encías o nariz|dolor abdominal intenso|vómitos persistentes|petequias|somnolencia|disminución de la diuresis", dur="A")
G(57, "fiebre sin foco aparente|fiebre intermitente con escalofríos y malestar general|fiebre de predominio vespertino con sudoración|alzas térmicas con cefalea y mialgias|fiebre persistente sin síntomas localizadores",
  "escalofríos|sudoración|cefalea|mialgias|hiporexia|malestar general|astenia",
  "Refiere que mide la temperatura con termómetro en casa.|Refiere contacto con personas enfermas.|Refiere viaje reciente.|Refiere exposición a mosquitos.",
  "Tomó acetaminofén con descenso transitorio.|Utilizó medios físicos con alivio parcial.|No ha recibido tratamiento.",
  "tos|dolor de garganta|disuria|diarrea|erupción cutánea|rigidez de cuello|sangrado", dur="A")
G(58, "dolor epigástrico urente|ardor en epigastrio que mejora con alimentos|dolor en la boca del estómago postprandial|epigastralgia con náuseas y eructos|dolor epigástrico nocturno|sensación de llenura con dolor en epigastrio",
  "náuseas|eructos|distensión abdominal|saciedad precoz|hiporexia|acidez|sabor ácido",
  "Refiere consumo frecuente de picantes, café o alcohol.|Refiere uso reciente de antiinflamatorios.|Refiere estrés o ayunos prolongados.|Refiere episodios similares previos.|Refiere tabaquismo.",
  "Tomó antiácidos con alivio parcial.|Tomó omeprazol con mejoría transitoria.|No ha recibido tratamiento.",
  "vómitos con sangre|heces negras|pérdida de peso|dificultad para tragar|fiebre|dolor abdominal intenso", dur="B")
G(59, "dolor en rodilla que aumenta al subir escaleras|dolor y crepitaciones en rodillas al caminar|rigidez matutina breve en rodillas|dolor de rodillas que mejora con el reposo|dolor bilateral de rodillas con limitación para agacharse",
  "crepitaciones|rigidez matutina breve|edema leve|limitación para flexionar|sensación de fallo de rodilla|deformidad en varo",
  "Acude a control con aumento del dolor en las últimas semanas.|Refiere sobrepeso.|Refiere trabajo que requiere estar de pie.|Refiere dificultad para subir escaleras.|Refiere que el dolor es peor al final del día.",
  "en tratamiento con acetaminofén|en tratamiento con antiinflamatorios no esteroideos a demanda|en tratamiento con diclofenaco ocasional|en fisioterapia",
  "fiebre|enrojecimiento y calor articular|bloqueos|trauma reciente|derrame articular importante", dur="Y")
G(60, "herida en la piel con sangrado|herida abierta con bordes irregulares tras un golpe|corte superficial con sangrado controlado|herida contusa tras caída|laceración con dolor y edema local",
  "dolor local|sangrado leve|edema alrededor de la herida|tierra o contaminación de la herida|limitación funcional",
  "Refiere que se lesionó con un objeto metálico.|Refiere caída reciente.|Refiere que se cortó con un machete o cuchillo.|Refiere que ocurrió durante trabajo de campo.|Refiere que no tiene vacuna antitetánica al día.",
  "Se lavó la herida con agua y jabón.|Se aplicó alcohol y gasa.|Se aplicó remedios caseros.|No ha recibido tratamiento.",
  "pérdida de movilidad|fiebre|secreción purulenta|sangrado abundante|parestesias|cuerpo extraño visible", dur="H")
G(61, "aumento de volumen en región inguinal que aparece al esfuerzo|tumoración inguinal reductible con dolor ocasional|bulto en la ingle que aumenta al toser o cargar peso|dolor inguinal con masa que desaparece al acostarse|abultamiento en la ingle con sensación de peso",
  "dolor ocasional|sensación de peso|aumento al esfuerzo|reducción espontánea al acostarse|molestia al caminar",
  "Refiere trabajo con carga de peso.|Refiere tos crónica.|Refiere estreñimiento con esfuerzo.|Refiere antecedente de hernia en familiares.",
  "No ha recibido tratamiento.|Utiliza faja con alivio parcial.",
  "dolor intenso súbito|masa irreductible|vómitos|ausencia de evacuaciones|fiebre|enrojecimiento de la piel de la masa", dur="L")
G(62, "aumento de volumen en el ombligo que sobresale al esfuerzo|abultamiento umbilical reductible|protrusión blanda en el ombligo que aumenta al llorar o toser|tumoración umbilical indolora|bulto en el ombligo con molestia ocasional",
  "molestia ocasional|aumento al llorar o toser|reducción al acostarse|sensación de tirantez",
  "Según refiere la madre, el abultamiento se notó desde las primeras semanas.|Refiere múltiples embarazos previos.|Refiere sobrepeso.|Refiere trabajo con carga de peso.",
  "No ha recibido tratamiento.|Utiliza faja o moneda con alivio parcial.",
  "dolor intenso|vómitos|enrojecimiento de la piel|masa irreductible|fiebre|distensión abdominal", dur="L")
