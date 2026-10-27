# Expedientes MdM — notas para Claude Code

Programa de escritorio (Windows) de Emil, médico en Honduras: carga hojas ATA (Excel o escritas a mano), guarda los pacientes
en SQLite y, por paciente, abre una ventana de revisión y **llena (sin guardar)** el formulario de ActivityInfo con Chrome/Selenium.
Habla con Emil en español, sin rodeos; prefiere que se verifique antes de entregar.

## Reglas que no se rompen
- **Nunca guardar nada en ActivityInfo**: ni «Guardar registro» ni «Guardar como borrador». La ficha la crea Emil a mano tras revisar.
  Único clic permitido: «Está hecho» del subformulario APS, y solo si también se pide SSR (`PERMITIR_ESTA_HECHO_EN_APS`).
- Mantener el orden del formulario `https://www.activityinfo.org/app#form/cgagdtzm4cnphz5kmo/newRecord`.
- Nunca escribir contraseñas ni credenciales; nunca borrar de forma definitiva sin copia previa.
- **No subir a GitHub** `*.db`, `respaldos/` ni exportaciones de ActivityInfo (datos de pacientes).
- Hacer `git push origin master:main` solo cuando Emil lo pida. Commits con los trailers `Co-Authored-By` y `Claude-Session` que indique la sesión.
- No reiniciar la app mientras haya un diálogo «Añadir registro» abierto, salvo que Emil lo pida.

## Estructura
- `main.py`, `ui/` (Tkinter: `page_ata.py`, `page_pacientes.py`, `dialog_activityinfo.py`, `med_picker.py`, `buscador.py`), `database.py` (SQLite + migraciones), `backup.py`.
- `services/ata.py`: importar/exportar ATA, normalización (sexo H/M, estado civil S/C/UL/D/V, profesión AM/O, edad en una columna, localidad del encabezado).
- `services/activityinfo.py` + `ai_fill.js`: valores por defecto, `build_defaults`, Selenium (se conecta a Chrome en `127.0.0.1:9223`, perfil propio en `%LOCALAPPDATA%\BrigadasMedicas\chrome_activityinfo`).
- Bancos de texto: `hea_*`, `plan_*`, `examen_*` (grandes; regenerar con `tools/`). `medicamentos.py`: lista A–Z para los planes APS/SSR.
- Datos de Emil: la base y `respaldos/` viven fuera de la carpeta del programa (`%LOCALAPPDATA%\BrigadasMedicas`).

## Pruebas (Linux, Python 3.12 + Xvfb)
```
pkill Xvfb; rm -f /tmp/.X97-lock; (nohup Xvfb :97 -screen 0 1400x1000x24 &)
DISPLAY=:97 /usr/bin/python3.12 -m unittest tests.test_ui tests.test_extras tests.test_all tests.test_ssr_catalogo   # ~15 s
DISPLAY=:97 /usr/bin/python3.12 -m unittest tests.test_hea                                                          # ~10 min, en segundo plano
```
Si Xvfb muere, las pruebas de interfaz se saltan sin avisar. El llenado real del formulario solo está probado contra simulaciones.

## Detalles que muerden
- `widget.focus_get()` lanza `KeyError: 'popdown'` con un combo abierto: usar `str(w.tk.call("focus"))`.
- El PC usa Python 3.14.x (no 3.15); `iniciar_MDm.bat` crea `.venv` e instala; el arranque tarda ~25 s en el PC de Emil (causa sin confirmar).
- Los medicamentos y dosis de `services/medicamentos.py` los propuso Claude, **no** están revisados por un clínico.
- Pendientes ofrecidos: botón «Buscar actualización» (git pull), registro de tiempos de arranque, «Referencia Transfronteriza» siempre visible también en SSR, aviso al subir dos veces el mismo Excel, no restaurar contraseña/ajustes con una copia.
- Actualizar el PC: copiar archivos a la carpeta `Documentos\MDm` (sin sobrescribir `iniciar_MDm.bat` del PC) o seguir `INSTALACION.md`.
