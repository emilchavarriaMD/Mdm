from hea_gen import G

TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXN = "No ha recibido tratamiento.|Se automedicó sin mejoría.|Utilizó remedios caseros con alivio parcial."

G(7, "dolor y hematomas posteriores a una agresión física según su relato|lesiones contusas en cara y extremidades tras un episodio de violencia física|dolor en costillas y región lumbar tras recibir golpes|malestar emocional y dolor corporal posteriores a una agresión física",
  "equimosis en brazos y espalda|dolor a la movilización|cefalea|temor a regresar a su domicilio|insomnio|edema local|llanto fácil",
  "Refiere que el agresor es una persona conocida.|Refiere episodios previos de agresión.|Refiere que no había buscado atención antes.|Se brinda espacio privado y confidencial, y se registra únicamente lo expresado por la persona.",
  "Se aplicó compresas frías con alivio parcial.|No ha recibido atención previa.|Tomó analgésicos con alivio parcial.",
  "pérdida del conocimiento|vómitos|dificultad respiratoria|deformidad de alguna extremidad|ideas de hacerse daño|uso de armas en la agresión", dur="-")
G(8, "lesiones habonosas pruriginosas de aparición brusca|ronchas generalizadas con prurito intenso|erupción urticariforme migratoria que aparece y desaparece en horas|prurito y enrojecimiento de la piel tras la exposición a un posible alérgeno|edema de labios y párpados con prurito",
  "prurito intenso|edema de párpados|ardor en la piel|enrojecimiento generalizado|estornudos|lagrimeo|lesiones que cambian de sitio en horas",
  "Refiere ingesta reciente de alimentos poco habituales.|Refiere inicio de un medicamento nuevo.|Refiere contacto reciente con un producto de limpieza.|Refiere antecedente de alergias.|Refiere picadura de insecto previa.",
  "Tomó antihistamínico con alivio parcial.|Se aplicó crema con corticoide sin mejoría.|No ha recibido tratamiento.",
  "dificultad para respirar|edema de lengua o garganta|silbidos en el pecho|fiebre|dolor abdominal|mareo o desmayo", dur="H")
G(9, "odinofagia intensa que dificulta la deglución|dolor de garganta con amígdalas aumentadas de tamaño|dolor al tragar con sensación de cuerpo extraño|garganta enrojecida y dolorosa con placas blanquecinas|dolor faríngeo que se irradia a los oídos|odinofagia con halitosis y voz apagada",
  "fiebre|malestar general|cefalea|adenopatías cervicales dolorosas|hiporexia|placas blanquecinas en amígdalas|tos leve|voz apagada",
  "Refiere contacto con personas con cuadro similar.|Refiere episodios previos de amigdalitis.|Refiere ingesta de bebidas frías antes del inicio.|Refiere asistencia a escuela o centro de trabajo con casos similares.",
  TXA + "|Realizó gárgaras con agua con sal con alivio leve.",
  "tos intensa|dificultad respiratoria|dificultad para abrir la boca|salivación excesiva|erupción en la piel|vómitos", dur="A")
G(10, "astenia, adinamia y fatiga fácil|cansancio progresivo con palidez de piel y mucosas|debilidad generalizada que limita sus actividades|mareo, cefalea y fatiga fácil|disnea de esfuerzo leve con palpitaciones",
  "palidez de piel y mucosas|mareo|cefalea|palpitaciones|caída del cabello|uñas quebradizas|disnea de esfuerzo|hiporexia|irritabilidad",
  "Refiere dieta baja en carnes y verduras.|Refiere menstruaciones abundantes.|Refiere antecedente de anemia.|Refiere embarazo o lactancia reciente.|Refiere sangrado digestivo previo.",
  "No ha recibido tratamiento.|Tomó multivitamínicos sin mejoría.|Tomó hierro sin constancia.",
  "sangrado digestivo visible|heces negras|pérdida de peso|fiebre|dolor torácico|desmayos", dur="L")
G(11, "disminución marcada del apetito con pérdida de peso|falta de apetito con rechazo a las comidas|saciedad temprana y negativa a comer|hiporexia persistente con pérdida de peso no intencionada",
  "pérdida de peso|náuseas|astenia|estado de ánimo bajo|dolor abdominal leve|distensión abdominal",
  "Refiere preocupación por su peso o su imagen corporal.|Refiere estrés o problemas familiares recientes.|Refiere que come muy poco en el día.|Refiere cambios recientes de medicación.",
  "No ha recibido tratamiento.|Tomó vitaminas sin mejoría.|Utilizó infusiones caseras sin cambios.",
  "vómitos persistentes|dolor abdominal intenso|fiebre|diarrea|dificultad para tragar|sangrado digestivo", dur="L")
G(12, "disminución del apetito de varios días|poco deseo de comer con saciedad rápida|rechazo a algunos alimentos con comidas incompletas|hiporexia con sensación de llenura",
  "fatiga|náuseas ocasionales|distensión abdominal|pérdida leve de peso|estreñimiento|cefalea",
  "Refiere que sus horarios de comida son irregulares.|Refiere estrés laboral o familiar.|Refiere que el cuadro inició tras un cuadro gripal.|Refiere cambios recientes en su rutina.",
  TXN, "vómitos|fiebre|diarrea|dolor abdominal intenso|pérdida de peso importante", dur="B")
G(13, "dolor, rigidez e inflamación en articulaciones pequeñas de manos|rigidez matutina de más de una hora en manos y muñecas|dolor y edema simétrico en articulaciones de manos y pies|dolor articular persistente con limitación para tareas finas",
  "rigidez matutina|edema articular|fatiga|deformidad leve de dedos|limitación para cerrar el puño|dolor nocturno|nódulos subcutáneos",
  "Acude a control, con agudización reciente de los síntomas.|Refiere que la rigidez matutina ha empeorado en el último mes.|Refiere dificultad para tareas cotidianas como abrir frascos.|Refiere que dejó de tomar su tratamiento hace varias semanas.",
  "en tratamiento con metotrexato semanal|en tratamiento con antiinflamatorios no esteroideos a demanda|en tratamiento con prednisona en dosis baja|con tratamiento irregular",
  "fiebre|dolor torácico|disnea|ojo rojo doloroso|lesiones en piel|pérdida de peso", dur="Y")
G(14, "dolor articular de predominio mecánico que mejora con el reposo|dolor en rodillas y caderas al caminar con crepitaciones|dolor articular con rigidez matinal breve|dolor en articulaciones de manos con nódulos en las interfalángicas|dolor que empeora al subir escaleras o al final del día",
  "rigidez matutina breve|crepitaciones|limitación de la movilidad|edema articular leve|deformidad de las articulaciones|sensación de fallo en la rodilla",
  "Acude a control con dolor que ha aumentado en las últimas semanas.|Refiere sobrepeso y actividad física intensa en el pasado.|Refiere trabajo que implica cargar peso.|Refiere dificultad para caminar largas distancias.",
  "en tratamiento con acetaminofén a demanda|en tratamiento con antiinflamatorios no esteroideos con alivio parcial|con tratamiento irregular|en fisioterapia",
  "fiebre|enrojecimiento de la articulación|bloqueos articulares|trauma reciente|pérdida de peso", dur="Y")
G(15, "tos nocturna con silbidos en el pecho|disnea y sibilancias de predominio nocturno|opresión torácica y tos tras ejercicio o exposición al polvo|crisis de tos y sibilancias que ceden con salbutamol|disnea leve con sibilancias",
  "sibilancias|tos seca|opresión torácica|disnea de esfuerzo|despertares nocturnos por tos|rinorrea|estornudos",
  "Acude a control, sin crisis recientes.|Refiere uso ocasional de inhalador de rescate.|Refiere exposición a polvo y humo.|Refiere antecedente familiar de asma.|Refiere que los síntomas empeoran con el cambio de clima.",
  "en tratamiento con salbutamol inhalado a demanda|en tratamiento con budesonida inhalada|en tratamiento con salbutamol y esteroide inhalado|con tratamiento irregular",
  "fiebre|dificultad respiratoria importante|cianosis|hospitalizaciones recientes|uso de inhalador más de 3 veces por semana", dur="Y")
G(16, "exacerbación de tos y disnea con sibilancias de pocos días|crisis asmática con opresión torácica y sibilancias|disnea progresiva con tos nocturna que no cede con el inhalador|sibilancias y dificultad respiratoria tras exposición a un desencadenante",
  "sibilancias audibles|opresión torácica|tos seca persistente|uso frecuente de salbutamol|despertares nocturnos|dificultad para hablar frases largas",
  "Refiere cuadro gripal previo.|Refiere exposición a humo o polvo.|Refiere que dejó de usar su inhalador de control.|Refiere cambios de clima recientes.",
  "en tratamiento con salbutamol inhalado, con alivio parcial|con uso irregular de su inhalador de control|en tratamiento con nebulizaciones, con alivio transitorio",
  "fiebre|dolor torácico|cianosis|esputo purulento|dificultad para hablar|somnolencia", dur="Y")
