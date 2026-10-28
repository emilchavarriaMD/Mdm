# Historial de la conversación — Expedientes MdM (para revisión en Claude Code)

Resumen de lo trabajado con Emil (médico, Honduras) en la sesión de Claude. Sirve para que otra sesión revise todo con contexto.
Reglas fijas del proyecto: ver `CLAUDE.md`. Repositorio: https://github.com/emilchavarriaMD/mdm (rama `main`; se sube con `git push origin master:main`).
Último commit subido a GitHub: `af55cb6`. Commits locales posteriores (sin subir): `19fa5f9` (CLAUDE.md) y este documento.

## 1. Qué es el programa
Programa de escritorio Windows (Tkinter + SQLite + openpyxl). Se cargan hojas ATA, y por paciente «Añadir registro» abre una ventana
de revisión; luego Chrome/Selenium **llena sin guardar** el formulario de ActivityInfo. Emil crea la ficha a mano después.

## 2. Cambios hechos en esta etapa (todos con pruebas)
1. **Medicamentos en el plan (APS y SSR)**: lista de 42 medicamentos (A–Z, con lupa de búsqueda, filas editables) que se agrega al final del
   plan como «Medicamentos indicados: …» sin alterar el texto del plan (`services/medicamentos.py`, `ui/med_picker.py`).
2. **Arranque más rápido**: caché de las versiones HEA de PF (`hea_pf_cache.py`) y precompilación en `iniciar_MDm.bat`. En el PC de Emil aún tarda ~25–30 s (causa sin confirmar).
3. **Referencia Transfronteriza** siempre visible en APS, por defecto «No». (En SSR sigue dentro de «derivación extra»).
4. **HEA/plan de APS nunca llevan diagnósticos de SSR** (y al revés); candidiasis vaginal + parasitismo ya no mezcla HEA.
5. **Chrome cerrado entre registros**: reconexión y un reintento (`fill_form`).
6. **Menores de 18 años**: estado civil «No aplica», escolaridad «Ninguno», ocupación «No aplica».
7. **Diagnósticos en orden A–Z con buscador** (lupa) en APS y SSR; **antecedentes obstétricos** (G, P, C, A, HV, HM) editables además de la lista 0–16.
8. Corrección del error `KeyError: 'popdown'` (usar `str(w.tk.call("focus"))` en vez de `focus_get()`).
9. **Tabla de Pacientes**: se quitaron las columnas Sexo y Edad y se muestra **Localidad** (los filtros Sexo/Edad de arriba se conservaron; Emil puede pedir quitarlos).
10. **ATA nuevo** (`ATA_modificado.xlsx`): estado civil en letras (S, C, UL, D, V), profesión AM («Trabajo doméstico NO remunerado») u O («Otro»),
    edad en una sola columna («34», «8m», «10d», «5a 3m»), 2 diagnósticos, y localidad/departamento del encabezado copiados a cada fila.
    Columnas nuevas en «Cargar ATA» y en la exportación. Menores siguen en «No aplica» aunque el ATA diga otra cosa.
11. **Revisión general** (análisis estático + un revisor independiente). Corregido: un solo llenado a la vez; conservar el estado «Registrado»
    al corregir un nombre (se enlaza por id de fila); copia de seguridad antes de «Eliminar hoja»; recargar la hoja ATA al volver a la pantalla;
    búsqueda sin tildes; edad desde fecha de nacimiento y «0 años» = menor de un año; edad > 120 rechazada; espera de login tolerante a redirecciones;
    cerrar chromedriver al salir; exportar con «SEXO (H/M)»; «cervicalgia» ya no dispara la alerta de «solo mujer».

## 3. Pruebas
`tests.test_ui`, `test_extras`, `test_all`, `test_ssr_catalogo` (85 OK, ~15 s) y `test_hea` (37 OK, ~10 min). Instrucciones en `CLAUDE.md`.
El llenado real del formulario solo está probado contra simulaciones; el ATA nuevo se probó con una hoja de ejemplo, no con una real.

## 4. Pendientes y puntos para que Code revise
- **Duplicados**: subir dos veces el mismo Excel crea la hoja y los pacientes dos veces, sin aviso.
- **Restaurar copia de seguridad** también restaura ajustes (incluida la contraseña) y no rota las copias `previa_restauracion_*`.
- **Valores propuestos al azar o por defecto** (escolaridad/ocupación, signos vitales en menores, antecedentes en «No») aparecen como «listo» aunque nadie los confirmó.
- **Sexo M/F**: una «M» sola se toma como mujer; con M y F sin H se adivina por conteo (solo hay aviso al importar Excel, no al escribir en la tabla).
- `visits.py` / `patients.py` tienen código sin conexión a la interfaz con errores latentes (finalizadas vuelven a borrador; `find_duplicates` lento con miles de filas).
- Rendimiento: `list_records` trae `ai_datos` de todas las filas; el panel del diálogo se refresca cada 700 ms.
- «Municipio» no viene en el ATA nuevo: el «Lugar de atención» (Choloma/San Pedro Sula) cae al establecimiento o a Configuración.
- Medicamentos y dosis propuestos por Claude, **sin revisión clínica** (dudas: medroxiprogesterona 150 mg, clindamicina/clotrimazol 3 días, loperamida, prednisona 4 Tab).
- Ofrecidos y sin hacer: botón «Buscar actualización» (git pull), registro de tiempos de arranque, mensaje del `.bat` que diga «instale Python», SSR transfronteriza siempre visible.
- Entorno de Emil: PC con Python 3.14.x; en otra computadora tuvo bloqueo de «Control inteligente de aplicaciones» y error «No installed Python found» (se resolvió instalando Python 3.14.8 con «Add to PATH»).
- Control remoto de la PC desde Claude falló una vez por UIPI (ventana con permisos de administrador, p. ej. Valorant/Riot): no se puede hacer clic mientras esté abierta.
