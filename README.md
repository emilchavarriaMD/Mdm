# MDm – Registro Clínico de Brigadas Médicas (Honduras)

**Versión 1.2**

Programa de escritorio para Windows (Python + **Tkinter** + SQLite) que registra pacientes de brigadas
médicas con tres fichas vinculadas por un único expediente: **Ficha Integral**, **Atención Primaria
en Salud (APS)** y **Salud Sexual y Reproductiva (SSR)**. Funciona sin internet; los datos quedan en
la computadora (`%LOCALAPPDATA%\BrigadasMedicas`).

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

En el menú lateral, **Hojas ATA**: cargue la foto de la hoja (queda a la vista, con acercar/alejar),
escriba o pegue los datos en la tabla (columnas iguales a la hoja) y confirme con **Guardar**.
El programa no lee la foto por sí solo ni rellena nada: solo guarda lo que usted confirma.
Las comillas (") en departamento, municipio y localidad se repiten desde la fila anterior.
**Exportar Excel** genera el archivo con las columnas del ATA. La Ficha Integral tiene ahora el campo
*Número de identidad* (opcional); también se usa en la búsqueda y en la detección de duplicados.


## Pestañas del programa
**Cargar ATA** (subir foto o Excel, confirmar y guardar en la base) · **Pacientes** (un renglón por paciente,
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
