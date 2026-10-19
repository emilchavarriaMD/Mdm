from hea_gen import G

TXA = "Se automedicó con acetaminofén con alivio parcial.|Tomó ibuprofeno con alivio transitorio.|Tomó analgésicos sin mejoría.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."
TXB = "Se automedicó con antibiótico sin mejoría.|Tomó antiinflamatorios con alivio parcial.|No ha recibido tratamiento.|Utilizó remedios caseros sin mejoría."

G(1, "aumento de volumen doloroso en la piel|lesión nodular eritematosa, caliente y dolorosa|tumoración cutánea fluctuante con dolor pulsátil|lesión dolorosa con eritema y punto blanquecino central|nódulo doloroso que ha crecido de forma progresiva",
  "calor y eritema local|dolor que se intensifica al tacto|salida espontánea de material purulento|alzas térmicas no cuantificadas|malestar general|dolor que dificulta el descanso|induración alrededor de la lesión",
  "Refiere pequeña herida o rascado previo en la zona.|Refiere episodios similares en el pasado.|Refiere que se manipuló la lesión.|Refiere diabetes mellitus.|Refiere haber compartido objetos de aseo personal.|Refiere que la lesión inició como una espinilla.",
  "Se aplicó compresas tibias sin mejoría.|Se automedicó con analgésico oral con alivio parcial.|Se aplicó pomada antibiótica sin alivio.|No ha recibido tratamiento.",
  "fiebre|escalofríos|traumatismo previo en la zona|lesiones similares en otras partes del cuerpo|secreción fétida|dolor al movilizar la articulación vecina")
G(2, "lesión elevada, roja y dolorosa centrada en un folículo piloso|nódulo doloroso con punta amarillenta en zona de roce|lesión pustulosa dolorosa de crecimiento progresivo|nódulo eritematoso e indurado en axila, cuello o glúteo|lesión dolorosa en nuca con drenaje espontáneo reciente",
  "calor local|dolor al roce de la ropa|induración perilesional|salida de material purulento|prurito previo a la lesión|aumento de tamaño progresivo",
  "Refiere afeitado reciente de la zona.|Refiere episodios similares en el pasado.|Refiere sudoración abundante y roce constante con la ropa.|Refiere haberse manipulado la lesión.|Refiere diabetes mellitus.",
  "Se aplicó compresas tibias con alivio parcial.|Se automedicó con antibiótico oral sin mejoría.|No ha recibido tratamiento.",
  "fiebre|escalofríos|malestar general|lesiones similares en otras zonas|dificultad para movilizar la zona", dur="A")
G(3, "lesión cutánea con eritema, calor y dolor|erosiones con costras amarillentas y eritema|pústulas dolorosas agrupadas en la piel|lesión supurativa con halo eritematoso|área de piel enrojecida y dolorosa con secreción purulenta",
  "calor local|prurito|secreción purulenta|costras melicéricas|dolor al tacto|edema perilesional|adenopatía regional dolorosa",
  "Refiere pequeña herida previa en la zona.|Refiere picadura o rascado previo.|Refiere contacto con personas con lesiones similares.|Refiere humedad y roce constante en la zona.",
  TXB, "fiebre|escalofríos|lesiones similares en otras zonas|secreción fétida|dificultad para movilizar la zona")
G(4, "dolor dental intenso y continuo|odontalgia pulsátil que se irradia a oído y sien|dolor dental que aumenta con la masticación|aumento de volumen doloroso en la encía junto a una pieza dental|dolor dental espontáneo que se exacerba por la noche",
  "sensibilidad a lo frío y a lo caliente|edema facial leve|mal sabor de boca|dolor a la percusión de la pieza|dificultad para masticar|fiebre baja|halitosis",
  "Refiere caries extensa en la pieza afectada.|Refiere antecedente de tratamiento dental incompleto.|Refiere que no ha acudido al odontólogo.|Refiere fractura previa de la pieza dental.",
  "Se automedicó con ibuprofeno con alivio transitorio.|Utilizó clavo de olor sin mejoría.|Se automedicó con antibiótico sin mejoría.|No ha recibido tratamiento.",
  "fiebre alta|dificultad para abrir la boca|dificultad para tragar|dificultad respiratoria|edema que se extienda al cuello|traumatismo reciente en la boca")
G(5, "odontalgia que cedió parcialmente tras la salida espontánea de material purulento|aumento de volumen en la encía con fístula que drena pus|dolor dental previo seguido de salida de secreción por la encía|dolor dental con alivio posterior al drenaje espontáneo",
  "sabor desagradable en la boca|fístula en la encía|edema facial leve|dolor a la masticación|halitosis|sensibilidad a la percusión",
  "Refiere caries extensa en la pieza afectada.|Refiere que el dolor había sido intenso en los días previos.|Refiere episodios similares previos.|Refiere que no ha acudido al odontólogo.",
  "Se automedicó con analgésico con alivio parcial.|Se automedicó con antibiótico sin mejoría.|No ha recibido tratamiento.",
  "fiebre|dificultad para tragar|dificultad para abrir la boca|edema que se extienda al cuello|dificultad respiratoria", dur="A")
G(6, "malestar emocional intenso posterior a un evento de violencia sexual según su relato|ansiedad, llanto fácil y temor tras referir violencia sexual reciente|dolor genital y malestar emocional posteriores a una agresión sexual referida|insomnio y miedo persistente desde un evento de abuso sexual relatado|dificultad para dormir y sobresaltos tras haber sufrido violencia sexual",
  "dolor genital|ansiedad intensa|llanto fácil|temor a represalias|dolor en hipogastrio|sangrado genital escaso|sensación de culpa",
  "Refiere que el agresor es una persona conocida.|Refiere que es la primera vez que busca atención.|Refiere que aún no ha contado lo sucedido a su familia.|Acude acompañada/o por un familiar.|Se brinda espacio privado y confidencial, y se registra únicamente lo expresado por la persona.",
  "No ha recibido atención previa.|Acude por primera vez a valoración.",
  "ideas de hacerse daño|pérdida del conocimiento|sangrado abundante|lesiones visibles en otras partes del cuerpo", dur="-")
