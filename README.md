# MDm – Expedientes MdM (Honduras)

**Versión 1.2**

Programa de escritorio para Windows (Python + **Tkinter** + SQLite) que registra pacientes de brigadas
médicas con tres fichas vinculadas por un único expediente: **Ficha Integral**, **Atención Primaria
en Salud (APS)** y **Salud Sexual y Reproductiva (SSR)**. Funciona sin internet; los datos quedan en
la computadora (`%LOCALAPPDATA%\BrigadasMedicas`).

## Instalar y abrir en otra computadora
Vea **INSTALACION.md** (Python 3.10+, Google Chrome y doble clic en `iniciar_MDm.bat`).

## Crear el .exe (Windows)
1. Instale Python 3.10+ desde python.org (marque *Add python.exe to PATH*).
2. Doble clic en **`build.bat`**. Instala dependencias, corre las pruebas y genera
   `dist\BrigadasMedicas\BrigadasMedicas.exe` (copie la carpeta completa donde quiera).
3. Para probar sin crear el .exe: `ejecutar.bat` (tras haber corrido `build.bat` una vez).

## Uso rápido
- **Inicio**: elija la *brigada actual*; verá totales, borradores pendientes y últimas atenciones.
- **Registrar paciente** → al guardar ofrece registrar APS/SSR de inmediato. Avisa si hay posibles duplicados.
- Barra azul "Paciente activo": accesos directos a Ficha Integral, nueva APS/SSR e historial.
- Fichas APS/SSR: 5 pestañas; **Guardar borrador** en cualquier momento, **Finalizar ficha** al terminar.
  Una ficha finalizada se abre en modo lectura (botón *Editar ficha*); cada cambio queda en *Ver cambios*.
- **Ctrl+N** nuevo paciente · **Ctrl+B** buscar · **Ctrl+S** guardar.
- Campos de fecha: escriba solo números (`17102026` → `17/10/2026`).

## Reglas clínicas del sistema
- Nada se rellena ni se marca "normal" automáticamente: lo no medido/evaluado queda vacío o *Pendiente*.
- Abdomen: botón para documentar *exploración limitada por ausencia de espacio/camilla*.
- La HEA por plantilla usa **solo** lo que el personal escribió, marca lo faltante como PENDIENTE y exige
  marcar "HEA revisada" para finalizar. Todo es local (sin IA en la nube).
- Prescrito vs. entregado se registran por separado; el sistema no calcula dosis.
- Consejería e intervenciones SSR quedan *Pendiente* hasta confirmarlas.

## Copias de seguridad
Menú **Copias de seguridad**: crear copia, guardarla en USB/otra carpeta, restaurar (se guarda antes una
copia "previa_restauracion"). Se crea una copia automática al cerrar (configurable).

## Contraseña
Menú **Configuración → Seguridad**. Se guarda cifrada (PBKDF2). Si se olvida no hay recuperación.

## Estructura
`main.py` · `database.py` · `config.py` · `backup.py` · `security.py` · `services/` (lógica, validaciones)
· `reports/` (PDF con ReportLab, Excel con OpenPyXL) · `ui/` (pantallas Tkinter) · `tests/`.

## Pruebas
`python -m unittest discover -s tests`:
- `test_all` (datos, PDF, Excel, respaldos), `test_ui` (interfaz; requiere pantalla),
- `test_hea` (banco de HEA: 3,000 combinaciones al azar de 1–3 diagnósticos, edad y sexo),
- `test_ai_fill` (llenado de ActivityInfo contra una réplica local del formulario, `tests/mock_activityinfo.html`;
  comprueba el orden, el punto de atención «Otro», la HEA, los diagnósticos y que **nunca** se pulse guardar;
  se omite si no está instalado Playwright).

## Limitaciones conocidas
- No incluye OCR de la hoja ATA (escritura manuscrita poco fiable); la importación desde foto sigue pendiente.
- No hay campo "número de identidad" en la Ficha Integral.
- Impresión: abre el PDF en el visor predeterminado para imprimir desde allí.
- El .exe se probó construyendo y arrancando en Linux; la compilación en Windows debe hacerla `build.bat` en su PC.


## Hojas ATA

En el menú lateral, **Cargar ATA** (pantalla «Pacientes atendidos»): suba el Excel ATA-2023 o escriba/pegue los datos
en la tabla y confirme con **Guardar en la base**. Ya no se sube la foto de la hoja (se transcribe aparte a Excel).
El programa no rellena nada por sí solo: solo guarda lo que usted confirma.
Las comillas (") en departamento, municipio y localidad se repiten desde la fila anterior.
**Exportar Excel** genera el archivo con las columnas del ATA. La Ficha Integral tiene ahora el campo
*Número de identidad* (opcional); también se usa en la búsqueda y en la detección de duplicados.


## Pestañas del programa
**Cargar ATA** (subir Excel, confirmar y guardar en la base) · **Pacientes** (un renglón por paciente,
con el botón «➕ Añadir registro») · **Copias de seguridad** · **Configuración**.

## Añadir registro en ActivityInfo
Al pulsar «➕ Añadir registro» se abre una ventana para revisar los datos, y luego Chrome (con un perfil
propio del programa) abre el formulario y **lo llena**. El programa **nunca guarda**: no pulsa
«Guardar registro», «Guardar como borrador» ni «Está hecho»; la ficha la crea usted a mano después de revisar.
- Si ActivityInfo pide iniciar sesión, hágalo en esa ventana (el programa no escribe contraseñas).
- Lo que el ATA no trae (estado civil, escolaridad, ocupación…) lo elige usted en la ventana; vacío = no se toca.
- Valores fijos (lugar de atención, proyecto, nacionalidad, idioma, profesional) se configuran en **Configuración**.
- Si el lugar de atención es uno de los «… - Otro», escriba en «Especifique punto de atención» cuál es.
- **Diagnósticos**: cada diagnóstico del ATA se elige de la lista de ActivityInfo (260 opciones con su código,
  guardadas en el programa; se puede escribir para buscar). El programa escribe la descripción y ActivityInfo pone
  el código. Nunca elige una opción que no coincida: si no la encuentra, la deja vacía y lo avisa.
- **HEA**: se arma sola con sexo, edad y diagnósticos (banco de 346 diagnósticos con 14 versiones distintas cada uno, en lenguaje médico; una sola HEA para APS y SSR) y se
  escribe en «Historia de la enfermedad actual» del subformulario APS. Con 2–3 diagnósticos se escribe una sola
  historia: los crónicos como «antecedente de…», el agudo como cuadro actual y los demás como «Además refiere…».
  Respeta edad y sexo, avisa si un diagnóstico no corresponde, y el botón «Otra versión» cambia la redacción.
  Siempre se puede corregir a mano antes de abrir Chrome.
- **Signos vitales**: listas desplegables en la ventana (sistólica 60–250 de 10 en 10, diastólica 30–150 de 10 en 10,
  frecuencia cardiaca 40–200, respiratoria 10–50, temperatura 35.0–41.0). Valores iniciales: 120 / 80 (hombre) o 70 (mujer),
  pulso al azar 65–90, respiratoria al azar 12–20 solo en mayores de 10 años (en niños se elige), temperatura al azar
  36.0–37.2. Se escriben en el subformulario APS; lo que se deje vacío no se toca.
- **Examen físico**: «Peso» se escribe a mano en la ventana (vacío = no se llena); la talla nunca se llena y el IMC lo
  calcula el formulario. «Examen Físico» se escribe como «Cefalo-caudal» por ahora (se puede editar en la ventana).
- **Plan** (cuadro de texto, por ahora solo «Plan») y **Derivación / servicio brindado**: «¿Va a ser derivado?» empieza vacío; al elegir Sí
  se muestran los demás campos (como en la página): «Servicio brindado» = Salud y, en la lista «Salud», por defecto
  «MdM - Atención primaria» (se puede elegir otra). Todo en el orden de la página.
- Necesita internet y Google Chrome.

## Salud Sexual y Reproductiva (1.4)
Al marcar «Salud Sexual y Reproductiva» en la ventana de «Añadir registro» se despliega, abajo del todo, su sección: defaults
(mismo punto = Sí, mismo proyecto = Sí, ficha Larga, recibió APS = Sí) y **dos listas de diagnósticos distintas**: la de
Atención primaria (la de siempre) y la de SSR (105 diagnósticos, máximo 2). La HEA, el examen físico, el plan y el profesional
son los mismos de Atención primaria. En ActivityInfo el programa pulsa «Está hecho» **solo en el subformulario de Atención
primaria** (únicamente si también hay SSR; vuelve a la ficha, no guarda nada) para poder abrir el de SSR; en SSR no pulsa nada,
ni «Guardar registro» ni «Guardar como borrador». También se llenan, en el orden de la página: ¿Ha sufrido violencia?, antecedentes (ITS, ITU, vacunación, VPH, Papanicolau, examen de mama,
observaciones), observaciones del diagnóstico, consejería de anticoncepción, derivación y «¿Víctima de violencia sexual reciente?».
Los diagnósticos salen en el mismo formato que los de APS (uno por cada diagnóstico del ATA; SSR admite máximo 2) y solo se sugiere
un equivalente cuando el nombre coincide exactamente o es un sinónimo conocido. Todo queda vacío por defecto (salvo los defaults
indicados y Servicio brindado = Salud / «MdM-Salud sexual y reproductiva»). La sección sigue el orden del subformulario: HEA, examen físico y plan propios (copian los de APS y se pueden editar), y los campos
que dependen de otro aparecen al elegirlo (violencia → tipo; ITS «Sí» → ¿Cuál?; ITU «Sí» → ¿complicada? y n.º de episodios; consejería
«Si» → ¿Ya planifica?, métodos y acceso). Los métodos anticonceptivos se eligen en listas ordenadas por frecuencia de uso (píldora, inyectable, condón… anillo vaginal al final). También hay antecedentes obstétricos (embarazo actual/anterior, FUM, control prenatal, gestaciones…). Con ficha «Larga» también salen, según el género, menarquía/ritmo/citología/VPH/autoexamen de mamas o espermarquia/testículos/próstata. No se llenan: signos
vitales/peso de SSR, medicamentos, lista de verificación de embarazo y los otros campos condicionales de SSR.

## Cambios
- **2.6** — Examen físico: sección «Piel y faneras» al final (después de Extremidades), con hallazgos según el diagnóstico (dermatitis, anemia, hepatitis, herpes, pediculosis, embarazo…); los diagnósticos escritos como en el ATA («Dermatitis», «HTA») ya se reconocen; unas 10 redacciones por hallazgo. Llenado: la bitácora (`bitacora_llenado.log`, botón «Bitácora del llenado») guarda cada intento con lo que falló; tras llenar se vuelve a leer cada cuadro de texto y se avisa si quedó vacío o distinto («Verificación»); «Está hecho» de APS ahora detecta bien que el subformulario se cerró. Pacientes: botón «Siguiente pendiente ▶», barra de avance, filtros por sexo, edad y diagnóstico, alertas ⚠ de incoherencias (sexo/edad/diagnóstico, fiebre sin temperatura; también en el panel izquierdo de «Añadir registro»), «Papelera» (borrar ya no es definitivo; se pueden recuperar) y «Resumen a Excel» (pacientes por sexo y edad, diagnósticos más frecuentes, estado de ActivityInfo).
- **2.5** — Ventana «Añadir registro»: secciones plegables en el mismo orden que ActivityInfo (Datos, HEA, Signos vitales, Examen físico, Diagnósticos, Plan, Derivación, SSR), panel izquierdo con ✓/● por sección, acceso directo («IR A») y lista de lo que falta; campos clave vacíos en rojo y aviso ampliado antes de abrir Chrome (Ctrl+Enter llena, Esc cancela). Pacientes: tercer estado «Llenado» (formulario llenado, ficha por crear) con colores. Configuración → Apariencia: tema claro/oscuro y tamaño de letra (se aplican al reiniciar). Ctrl+1…4 cambian de pantalla; Ctrl+F busca en Pacientes.
- **2.4** — HEA con varios diagnósticos: cada diagnóstico agudo adicional (APS o SSR: vaginosis, candidiasis, cervicitis, dismenorrea…) se cuenta con su propio cuadro (evolución, síntomas, un dato y sus «Niega…»), no con una sola etiqueta. Se evita «embarazo actual» sin diagnóstico de embarazo y «cuadro actual de cuadro».
- **2.3** — Plan: todas las medidas redactadas con verbo en infinitivo (lectura uniforme) y sin controles, citas, seguimiento ni referencias. Examen físico: la leyenda de genitourinario ya no menciona espéculos y se conservan los hallazgos que no requieren explorar (p. ej. altura uterina y frecuencia cardíaca fetal en embarazo, dolor suprapúbico).
- **2.2** — Ventana «Añadir registro»: panel fijo a la izquierda con nombre, edad, sexo y diagnósticos del paciente (se actualiza al corregir datos y no se desplaza con el formulario).
- **2.1** — Examen físico con etiquetas (Apariencia general, Cabeza, ORL, Cuello, Tórax, Corazón, Pulmones, Abdomen, Genitourinario, Extremidades). El genitourinario va después del abdomen y siempre dice que no se realiza inspección genital por falta de espacio privado, camilla e instrumental (incluidos espéculos vaginales); solo agrega la puño percusión lumbar si el diagnóstico la pide. El plan ya no lleva seguimiento y sus signos de alarma empiezan con «Vigilar signos de alarma como…».
- **2.0** — Plan general sin medicamentos: banco de 336 diagnósticos (APS y SSR) con medidas generales, signos de alarma y seguimiento, ordenados por importancia. El plan sale como un párrafo corto (3 a 4 medidas, 3 a 4 signos de alarma y un seguimiento); con varios diagnósticos solo entran las ideas de mayor peso, sin repetir. Se regenera al cambiar diagnósticos, hay botón «Otra versión del plan» y lo escrito a mano no se pisa. Los medicamentos se agregan a mano.
- **1.9** — Signos vitales pediátricos: en menores de 18 años la presión arterial, el pulso y la frecuencia respiratoria se proponen al azar dentro del rango normal para su edad (0–3 m, 3–6 m, 6–12 m, 1–3 a, 3–6 a, 6–12 a, 12–18 a). Si se corrige la edad a otra franja se vuelven a proponer (salvo lo escrito a mano).
- **1.8** — Pantalla «Cargar ATA» rediseñada: tarjetas para foto, encabezado y pacientes; zona de foto con área para hacer clic y subirla, zoom con Ctrl + rueda y arrastre para mover; toda la pantalla se desliza en conjunto (la tabla ya no tiene barra vertical propia, solo horizontal).
- **1.7** — Respaldo: segunda ubicación configurable (OneDrive, USB, disco externo) donde se deja una copia de cada respaldo automático, y copia automática cada 30 minutos mientras el programa está abierto (desactivable). Si la segunda ubicación no está disponible, la copia local se hace igual y se muestra un aviso. La base de pacientes nunca se sube a GitHub.
- **1.6** — Examen físico por secciones (General, Cabeza, ORL, Cuello, Tórax, Corazón, Pulmones, Abdomen, Extremidades, Genitourinario) que cambia según los diagnósticos elegidos (APS y SSR). Genitourinario: siempre en SSR; en APS solo si un diagnóstico lo requiere. El abdomen siempre dice que no se explora. Se regenera al cambiar diagnósticos salvo que se edite a mano.
- **1.5** — HEA nueva: banco ampliado y rehecho para las listas de APS (326) y de SSR (todas con HEA propia, p. ej. vaginosis bacteriana, cervicitis,
  dismenorrea, mastitis, obstétricos). 14 versiones por diagnóstico, sin repetirse; la HEA sale de los diagnósticos de APS **y** de SSR y es la
  misma en las dos secciones. Se regenera con `python3 tools/hea_gen.py` (fichas en `tools/hea_specs_*.py`).
- **1.4** — Salud Sexual y Reproductiva: sección propia en la ventana, lista de diagnósticos de SSR, llenado del subformulario.
- **1.3** — Peso y examen físico («Cefalo-caudal»); signos vitales con listas desplegables; HEA sin el prefijo «HEA:»; el lugar de atención espera más a que cargue la lista.
- **1.2** — HEA según edad y sexo; abreviaturas del ATA (PF, RC, FAB, FAV, tiña pedis, cervicalgia, vaginosis…);
  búsqueda al escribir en los diagnósticos y «HEA usa» por diagnóstico; «11» como comillas de ídem en el ATA;
  pruebas del banco de HEA y del llenado.
- **1.1** — Lista de diagnósticos de ActivityInfo, HEA en el subformulario APS, punto de atención «Otro»,
  ventana de registro con desplazamiento y maximizable.


## 2.7
- La HEA de APS ahora usa solo los diagnósticos de APS y la de SSR solo los de SSR (cada una con su botón de otra versión). El examen físico es el mismo en ambas fichas. El plan y las recomendaciones generales también se separan: el plan de APS usa solo los diagnósticos de APS y el de SSR solo los de SSR.
- SSR: se agregó la «Lista de verificación de embarazo» (6 preguntas Sí/No y el resultado, igual que en ActivityInfo). Aparece con consejería «Si» y género Mujer CIS u Hombre TRANS, entre el método actual y el método elegido, y se llena en ActivityInfo en ese mismo orden.
- HEA de planificación familiar (PF): ahora habla del método que dice el ATA («PF (ACOs)» → pastillas, «PF (Depo)» → inyección trimestral, implante, DIU, condón; «PF» solo → sin nombrar método), con 30 versiones por método (`services/hea_pf.py`). Antes la HEA de SSR salía siempre con la inyección porque la lista de SSR dice solo «anticoncepción»; ahora usa el texto del ATA mientras no cambies esa fila. También se entienden variantes como «PF (ACOS) 3 meses» o «PF (Depo) 3 meses» y todas pasan a SSR.

## 2.8 — valores por defecto
Lo que el ATA no trae ahora se propone ya puesto (la persona lo corrige en la ventana; vacío = no se llena):
- **Ficha:** LGTBIQ+ No · pueblo Ladino / Mestizo · estado civil Unión Libre · escolaridad al azar entre Primaria y Secundaria/Bachillerato · sector de ocupación al azar entre «Trabajo doméstico NO remunerado» y «Otro» · discapacidad No · ¿Ha sido derivado/a? No · tipo de consulta (APS) Primera · ¿Va a ser derivado? No (APS y SSR).
- **Signos vitales:** temperatura 36 o 37 (SIN decimales; la lista trae primero los grados enteros). Con diagnóstico de HTA (adultos): sistólica 140 o 130 y diastólica 90 u 80; si se agrega o quita la HTA en la ventana, se proponen de nuevo mientras no se hayan cambiado a mano.
- **SSR:** tipo de consulta Primera · violencia No · menarquía 12 · ritmo menstrual en lista (REGULAR / IRREGULAR, por defecto REGULAR) · trastorno menstrual, menopausia, prueba de VPH, autoexamen de mamas, ITS e ITU: No · embarazo actual No · embarazo anterior «> 2 AÑOS» · gestaciones, partos, cesáreas, abortos, óbitos, hijos vivos y muertos en lista de 0 a 16 (sin valor por defecto) · lactancia No · VPH, Papanicolau y examen de mama No · consejería Si · método elegido hoy Preservativo masculino · acceso Sí.
Están en `defectos_ficha()`, `defectos_ssr()` y `vitales_defecto()` de `services/activityinfo.py`.

## 2.9 — derivación (desde), viñeta de SSR, crónicos y registro guardado
- **Derivación (desde):** con «¿Ha sido derivado/a?» = Sí aparecen Procedencia de la derivación (lista de ActivityInfo), Observaciones y Código de referencia, y se llenan en la página.
- **Discapacidad:** con «Sí» aparece «¿Qué tipo de discapacidad?» (Física o motora, Intelectual, Mental, Sensorial).
- **Salud sexual y reproductiva** tiene su viñeta plegable como las otras secciones.
- **Crónicos sin crisis:** HTA, DM2, asma, EPOC, tiroides, epilepsia, dislipidemia, ERC… llevan examen físico NORMAL (viene a surtir su medicamento), salvo que el ATA diga crisis/descompensada/exacerbación, o que la descripción elegida ya sea una complicación (exacerbación, hipoglucemia, úlcera del pie diabético…).
- **Ver registro guardado:** al pulsar «Abrir Chrome y llenar» se guarda lo revisado (en la base, nunca en GitHub). El botón «Ver registro guardado» lo reabre tal cual, aunque se haya cerrado el programa.
- El plan de SSR siempre empieza con «Se entregan 10 Condones.» y la localidad del ATA va en «Especifique punto de atención».

## 3.0 — plantilla ATA-2023 (teléfono y gestas/partos)
- **Subir Excel** lee dos formatos: el de columnas simples de siempre y la plantilla ATA-2023 (encabezados de 3 filas, teléfono, procedencia, 3 diagnósticos y la columna «G= P= C= A= HV= HM=»). El encabezado de la hoja (establecimiento, código, tipo, departamento, municipio, fecha, profesional) se lee de las celdas de al lado de cada etiqueta.
- **Sexo:** la plantilla dice SEXO (M/F): se lee M = masculino (H) y F = femenino (M), y el programa avisa que se verifique.
- **Fechas** con año de dos cifras (15/10/26) se completan solas; las comillas (") repiten la fila anterior.
- **G/P/C/A/HV/HM** pasan a los antecedentes obstétricos de SSR (gestaciones, partos, cesáreas, abortos, hijos vivos y muertos). Con G=0 el embarazo anterior queda en «No hubo embarazo». La celda vacía («G=  P=  …» sin números) no llena nada.
- El **teléfono** y los números obstétricos se guardan con cada paciente del ATA.
- **Cargar ATA** ahora gira en torno a la plantilla: la tabla trae las columnas de la plantilla ATA-2023 (N°, nombre, teléfono, sexo, fecha de nacimiento, edad años/meses/días, departamento, municipio, localidad, 3 diagnósticos y G/P/C/A/HV/HM) y «Subir Excel (ATA-2023)» es el botón principal. HC, identidad, códigos CIE y referencias ya no se piden (lo ya guardado se conserva).
- **Exportar Excel** sale con la misma distribución de la plantilla, así que se puede volver a subir tal cual.
- **Sexo:** aunque el encabezado dice (M/F), en la hoja se escribe H/M. Solo si aparece «F» y ninguna «H» se entiende M/F y se convierte (con aviso).
- **Sexo:** siempre queda como H (hombre) o M (mujer). Se corrige solo lo escrito como masculino/femenino, hombre/mujer, masc./fem., F, etc., tanto al subir el Excel como al guardar la tabla. Una «M» sola es mujer; solo en una hoja que usa «F» (no menos que «M») y ninguna «H» se entiende M = masculino. Al subir un Excel el programa avisa cuántos valores corrigió.
- **Estética** — La app se llama «Expedientes MdM»; se quitó la foto de la pantalla de ATA (pantalla «Pacientes atendidos»); el tema oscuro pasó a gris cálido con acento terracota (como Claude Code) y barra de título oscura en Windows.

## Más versiones de texto
- HEA: 52 versiones por diagnóstico (las 26 primeras no cambian); sirven igual para APS y para SSR. Planificación familiar: 60 versiones por método.
- Examen físico: cada hallazgo positivo tiene hasta 24 redacciones nuevas (`services/examen_variantes_extra.py`).
- Plan de APS: frases propias de cada diagnóstico más frases por grupo clínico (`services/plan_extra_data.py`, generado con `tools/plan_extra_build.py` y `tools/plan_aps_grupos.py`): de 26 a 51 medidas y al menos 9 signos de alarma por diagnóstico.
Los textos nuevos no han tenido revisión clínica.
- Plan de SSR: cada diagnóstico de SSR tiene su propio plan (`services/plan_ssr_data.py`, generado con `tools/plan_ssr_build.py`), con frases distintas a las del plan de APS (consejería, pareja, preservativo, control ginecológico o prenatal). Cada plan tiene su botón «Otra versión».
- Medicamentos en el plan: lista de 42 medicamentos con dosis y frecuencia habituales (`services/medicamentos.py`, selector `ui/med_picker.py`); se eligen uno a uno, se pueden corregir y se escriben al final del plan de APS o de SSR sin cambiar el texto del plan.
- Arranque rápido: las versiones de HEA de planificación familiar están ya calculadas en `services/hea_pf_cache.py`; si se cambian las piezas de `services/hea_pf.py`, se regenera con `python tools/hea_pf_cache.py` (si no, el programa las calcula al abrir y tarda unos 25 s).
