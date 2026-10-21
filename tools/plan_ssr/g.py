"""Frases de grupo para el plan de SSR (se añaden después de las específicas de cada diagnóstico)."""
G = {
 "its": (["usar preservativo en todas las relaciones sexuales", "abstenerse de relaciones sexuales hasta completar el tratamiento", "informar y tratar a la pareja o parejas sexuales", "recibir consejería sobre infecciones de transmisión sexual",
          "realizar el tamizaje de VIH y sífilis con consejería", "completar el tratamiento aunque desaparezcan las molestias", "evitar duchas vaginales y productos irritantes", "reducir el número de parejas sexuales y evitar parejas nuevas sin protección",
          "acudir al control de seguimiento en la fecha indicada"],
         ["fiebre con dolor en el bajo vientre", "flujo con mal olor o con sangre", "lesiones que aumentan o duelen más", "síntomas que no ceden con el tratamiento"]),
 "mens": (["llevar un calendario menstrual con fechas y cantidad del sangrado", "acudir al control ginecológico con los estudios indicados", "descartar el embarazo si hay retraso", "mantener un peso saludable", "realizar ejercicio regular",
           "dormir lo suficiente y manejar el estrés", "comer alimentos ricos en hierro durante la menstruación", "recibir consejería sobre planificación familiar", "evitar el tabaco y el exceso de alcohol"],
          ["sangrado abundante con mareo o desmayo", "dolor pélvico intenso", "fiebre con dolor en el bajo vientre", "sangrado después de la menopausia"]),
 "emb": (["acudir a todos los controles prenatales", "tomar ácido fólico y hierro según indicación", "comer una alimentación balanceada y tomar abundante líquido", "descansar y dormir del lado izquierdo", "contar los movimientos del bebé desde que se perciben",
          "evitar el alcohol el tabaco y medicamentos sin indicación", "llevar siempre el carné prenatal", "preparar el plan de parto y el traslado al hospital", "recibir consejería sobre lactancia materna y planificación familiar posparto", "completar las vacunas del embarazo"],
         ["sangrado vaginal", "pérdida de líquido por la vagina", "dolor de cabeza intenso o visión borrosa", "disminución o ausencia de movimientos del bebé"]),
 "pue": (["acudir al control posparto en la fecha indicada", "amamantar a libre demanda", "descansar cuando el bebé duerma", "comer una alimentación nutritiva y tomar abundante líquido", "mantener la higiene de la herida o episiotomía",
          "recibir consejería sobre planificación familiar", "evitar relaciones sexuales hasta el control", "pedir apoyo para el cuidado del bebé", "usar toallas sanitarias y no tampones"],
         ["sangrado abundante o con mal olor", "fiebre o escalofríos", "dolor intenso en la herida o en el abdomen", "tristeza intensa o ideas de hacerse daño"]),
 "mam": (["realizar el autoexamen de mamas cada mes después de la menstruación", "acudir al examen clínico de mamas con el personal de salud", "realizar ecografía o mamografía según la edad e indicación", "usar un sostén cómodo con buen soporte", "reducir la cafeína",
         "mantener un peso saludable", "evitar el tabaco y el exceso de alcohol", "llevar un registro de los síntomas y el ciclo menstrual", "recibir consejería sobre los factores de riesgo"],
        ["bulto que crece o no cambia con el ciclo", "secreción por el pezón con sangre", "cambios en la piel o en el pezón", "ganglios en la axila"]),
 "ant": (["recibir consejería completa con los métodos anticonceptivos disponibles", "elegir el método con información sobre su uso y efectos", "usar preservativo además del método para prevenir infecciones", "acudir al control en la fecha indicada", "conocer los efectos esperados y los signos de alarma del método",
         "acudir si olvida o se equivoca en el uso del método", "tomar la decisión de forma libre e informada", "acudir con la pareja si lo desea", "mantener los controles ginecológicos periódicos"],
        ["retraso menstrual", "dolor abdominal o pélvico intenso", "sangrado abundante", "dolor en el pecho o en una pierna"]),
 "mas": (["acudir al control con urología", "tomar abundante líquido", "evitar el alcohol y el café en exceso", "mantener una buena higiene genital", "usar preservativo en las relaciones sexuales", "evitar el tabaco",
         "mantener una alimentación balanceada", "realizar ejercicio regular", "acudir al control en la fecha indicada"],
        ["imposibilidad de orinar", "fiebre con dolor al orinar", "sangre en la orina", "dolor intenso en los genitales"]),
 "onc": (["acudir de inmediato a la valoración especializada", "completar los estudios indicados", "llevar los resultados a todas las consultas", "evitar el tabaco y el alcohol", "mantener una alimentación nutritiva",
         "buscar apoyo emocional y familiar", "acompañarse a las citas", "mantener los controles programados", "no abandonar el seguimiento aunque no haya síntomas"],
        ["sangrado anormal", "dolor intenso", "pérdida de peso sin causa", "bulto que crece rápidamente"]),
 "sex": (["recibir consejería sobre salud sexual y reproductiva", "conversar con la pareja de forma abierta", "usar preservativo en las relaciones sexuales", "acudir al control con el personal de salud", "buscar apoyo psicológico si se necesita",
         "informarse sobre los métodos anticonceptivos", "mantener los controles ginecológicos periódicos", "conocer los servicios de apoyo disponibles"],
        ["ideas de hacerse daño", "dolor intenso al tener relaciones", "sangrado o secreción anormal", "sentirse en peligro"]),
 "gen": (["acudir al control en la fecha indicada", "mantener una alimentación balanceada", "tomar abundante líquido", "dormir de 7 a 8 horas", "evitar el tabaco y el alcohol", "recibir consejería sobre salud sexual y planificación familiar",
         "llevar los resultados a las consultas", "evitar la automedicación"],
        ["empeoramiento de los síntomas", "fiebre persistente", "dolor intenso", "dificultad para respirar"]),
}

# frases adicionales por grupo (se suman a las de arriba para que haya más variedad)
MAS_M = {
 "its": ["evitar el contacto íntimo si hay lesiones visibles", "mantener la higiene genital con agua y jabón suave", "usar ropa interior de algodón", "evitar compartir toallas y ropa interior", "acudir al control aunque ya no haya molestias", "evitar el alcohol y las drogas antes de las relaciones", "dialogar con la pareja sobre el cuidado y la protección", "conocer los signos de las infecciones de transmisión sexual", "llevar un registro de los síntomas y de la fecha de inicio"],
 "mens": ["tomar abundante líquido durante los días de sangrado", "evitar el ayuno prolongado y las dietas extremas", "llevar una alimentación rica en frutas y verduras", "evitar el consumo de tabaco", "realizar actividad física moderada varias veces por semana", "registrar los medicamentos que usa", "mantener horarios regulares de comida y sueño", "acudir al control con los resultados de los estudios", "conocer qué es un ciclo menstrual normal"],
 "emb": ["evitar el esfuerzo físico intenso", "evitar los viajes largos sin valoración", "mantener una buena higiene bucal", "usar ropa y calzado cómodos", "evitar el contacto con personas con enfermedades infecciosas", "lavarse las manos con frecuencia", "realizar ejercicios suaves como caminar", "evitar las comidas crudas o poco cocidas", "acudir acompañada a las consultas", "conocer los signos de trabajo de parto"],
 "pue": ["comer cinco veces al día en porciones pequeñas", "mantener una buena hidratación", "realizar ejercicios del piso pélvico", "mantener la higiene de las mamas antes de amamantar", "evitar levantar objetos pesados", "evitar el estreñimiento con fibra y líquidos", "descansar en posición cómoda para amamantar", "aceptar la ayuda de familiares", "consultar sobre el estado de ánimo si hay tristeza persistente"],
 "mam": ["conocer cómo es una mama normal en cada etapa del ciclo", "evitar el tabaco", "evitar el exceso de grasas en la alimentación", "realizar ejercicio al menos tres veces por semana", "mantener los controles periódicos con el personal de salud", "evitar el calor excesivo sobre la mama si hay dolor", "acudir a control si hay antecedentes familiares de cáncer de mama", "evitar medicamentos sin indicación", "mantener una buena postura"],
 "ant": ["conocer cuánto tarda en actuar el método elegido", "usar el método de forma constante y correcta", "guardar el método en un lugar adecuado", "conocer la fecha en que debe reponer el método", "mantener la comunicación con la pareja sobre la planificación", "acudir al servicio de salud ante cualquier duda", "saber que puede cambiar de método cuando lo desee", "evitar suspender el método sin consejería", "conocer los métodos de barrera"],
 "mas": ["evitar el uso de ropa muy ajustada", "evitar el tabaco y el exceso de alcohol", "mantener una alimentación balanceada", "evitar el sedentarismo", "mantener el peso adecuado", "evitar el consumo excesivo de sal y azúcar", "acudir a revisión periódica", "evitar aguantar las ganas de orinar", "conocer los signos de alarma urinarios"],
 "onc": ["acudir a las citas de seguimiento con puntualidad", "llevar un cuaderno con las preguntas para el equipo médico", "conversar con la familia sobre lo que se siente", "mantener una buena hidratación", "evitar el consumo de tabaco", "dormir lo suficiente", "conocer los servicios de apoyo disponibles", "realizar ejercicio suave si lo permite el médico", "mantener los vínculos con amigos y familiares"],
 "sex": ["conocer los derechos sexuales y reproductivos", "poner límites claros en las relaciones", "no aceptar presión ni violencia en las relaciones", "recibir información fiable sobre sexualidad", "buscar acompañamiento de una persona de confianza", "mantener una vida sexual segura y consentida", "hablar de los temores y las dudas con el personal de salud", "conocer dónde acudir en caso de violencia", "evitar el alcohol y las drogas en situaciones de riesgo"],
 "gen": ["mantener horarios regulares de sueño", "realizar ejercicio regular", "mantener un peso saludable", "mantener una buena higiene personal", "mantener las vacunas al día", "evitar el estrés excesivo", "acudir a revisión si cambian los síntomas", "no tomar medicamentos sin indicación", "mantener una dieta rica en frutas y verduras"],
}
MAS_A = {
 "its": ["fiebre con escalofríos", "dolor al orinar", "dolor durante las relaciones", "inflamación de los ganglios de la ingle", "sangrado fuera de la menstruación"],
 "mens": ["cansancio extremo o palidez", "dolor que no cede con las medidas indicadas", "retraso con prueba de embarazo positiva", "sangrado con fiebre", "desmayo"],
 "emb": ["fiebre alta", "vómitos que impiden tomar líquidos", "dolor al orinar", "hinchazón repentina de cara y manos", "dolor en una pierna con hinchazón"],
 "pue": ["dolor en una pierna con hinchazón", "salida de pus por la herida", "dificultad para respirar", "bulto doloroso en la mama", "ánimo muy bajo con dificultad para cuidar al bebé"],
 "mam": ["retracción del pezón", "enrojecimiento de la piel de la mama", "mama que cambia de forma", "ganglios en el cuello o la axila", "dolor que persiste tras la menstruación"],
 "ant": ["dolor intenso de cabeza", "problemas de visión", "retraso menstrual con el método", "fiebre con dolor pélvico", "dolor en una pierna con hinchazón"],
 "mas": ["fiebre con escalofríos", "dolor en la espalda baja", "orina con mal olor y turbia", "hinchazón de los testículos", "secreción por el pene o la vagina"],
 "onc": ["sangrado que no cede", "hinchazón de las piernas", "tos persistente", "dolor de huesos", "fatiga extrema"],
 "sex": ["pensamientos de hacerse daño", "lesiones en los genitales", "miedo a regresar a casa", "dolor pélvico intenso", "sangrado después de una agresión"],
 "gen": ["decaimiento marcado", "vómitos persistentes", "sangrado que no cede", "confusión", "dolor en el pecho"],
}
for _g, _v in MAS_M.items():
    G[_g] = (list(dict.fromkeys(G[_g][0] + _v)), list(dict.fromkeys(G[_g][1] + MAS_A[_g])))

MAS2_M = {
 "its": ["evitar las relaciones sexuales con parejas que tengan síntomas", "conocer el estado de salud de la pareja", "guardar los preservativos lejos del calor", "no usar dos preservativos a la vez", "evitar compartir juguetes sexuales sin protección", "acudir a control con la pareja cuando se indique", "realizar la prueba de VIH una vez al año si hay riesgo", "recibir información sobre la vacuna contra el VPH"],
 "mens": ["evitar los analgésicos sin indicación durante la menstruación", "consultar antes de cambiar de método anticonceptivo", "evitar el exceso de ejercicio extenuante", "mantener una buena higiene durante la menstruación", "cambiar la toalla sanitaria cada 4 a 6 horas", "conocer los cambios normales según la edad", "llevar el registro del ciclo en una aplicación o cuaderno", "mantener una buena hidratación"],
 "emb": ["evitar el consumo de alcohol tabaco y drogas", "evitar la exposición a sustancias tóxicas", "mantener la higiene de manos y de alimentos", "evitar la cafeína en exceso", "usar el cinturón de seguridad bajo el abdomen", "asistir a las charlas de preparación para el parto", "tener lista la bolsa para el hospital", "conocer el centro de salud más cercano"],
 "pue": ["evitar el uso de biberones y chupones al inicio de la lactancia", "extraer manualmente la leche si hay congestión", "dormir cuando el bebé duerma", "limitar las visitas los primeros días", "mantener una postura cómoda al amamantar", "alimentarse con proteínas y frutas", "usar medias o ropa cómoda si hay hinchazón de piernas", "caminar suavemente a diario"],
 "mam": ["mantener el sostén limpio y seco", "evitar golpes en las mamas", "evitar fumar", "mantener actividad física", "mirar y palpar las mamas frente al espejo", "anotar los cambios que note entre un mes y otro", "acudir a la consulta ante cualquier duda", "comer más frutas y verduras"],
 "ant": ["tener siempre una barrera de respaldo a mano", "revisar la fecha de vencimiento del método", "no compartir el método con otras personas", "acudir al control aunque no tenga molestias", "pedir información sobre cambios de método", "conocer cómo actuar ante un olvido", "informarse sobre el método para después del parto", "hablar sobre el método con su pareja"],
 "mas": ["tomar agua de forma regular", "mantener una buena higiene de manos", "evitar el calor excesivo en los genitales", "evitar baños muy calientes", "revisar los testículos y el pene una vez al mes", "orinar al terminar las relaciones sexuales", "acudir al control con laboratorios", "evitar el estreñimiento"],
 "onc": ["pedir al equipo médico información sencilla sobre la enfermedad", "organizar el calendario de citas", "tener una persona de apoyo en cada consulta", "evitar el contacto con personas con infecciones", "descansar entre actividades", "mantener una higiene bucal cuidadosa", "comer en porciones pequeñas con más frecuencia", "informarse en fuentes confiables"],
 "sex": ["no tomar decisiones bajo presión", "hablar con alguien de confianza", "conocer la anticoncepción de emergencia", "conocer el número de ayuda de la comunidad", "cuidar el descanso y la alimentación", "llevar un registro de lo ocurrido si desea hacerlo", "acudir al control de seguimiento", "tener un plan de seguridad"],
 "gen": ["mantener la actividad social", "limitar la cafeína", "mantener los controles preventivos", "evitar el sedentarismo", "tomar agua de forma regular", "mantener la higiene personal", "pedir ayuda si los síntomas empeoran", "llevar el carné de salud"],
}
MAS2_A = {
 "its": ["dolor al orinar que no cede", "fiebre alta", "dolor durante las relaciones", "inflamación de la ingle"],
 "mens": ["sangrado que empapa más de una toalla por hora", "mareo", "dolor que no cede", "fiebre con dolor en el vientre"],
 "emb": ["dolor intenso en el vientre", "fiebre alta", "hinchazón repentina", "convulsiones"],
 "pue": ["fiebre", "sangrado abundante", "dolor intenso en la herida", "dolor en una pierna"],
 "mam": ["bulto nuevo", "secreción con sangre", "cambios en la piel", "dolor de una sola mama"],
 "ant": ["dolor intenso de cabeza", "dolor en el pecho", "sangrado abundante", "retraso menstrual"],
 "mas": ["dolor intenso", "fiebre", "sangre en la orina", "imposibilidad de orinar"],
 "onc": ["sangrado", "pérdida de peso", "dolor persistente", "falta de aire"],
 "sex": ["pensamientos de hacerse daño", "dolor intenso", "sangrado", "miedo a regresar a casa"],
 "gen": ["fiebre", "dolor intenso", "vómitos persistentes", "confusión"],
}
for _g, _v in MAS2_M.items():
    G[_g] = (list(dict.fromkeys(G[_g][0] + _v)), list(dict.fromkeys(G[_g][1] + MAS2_A[_g])))
