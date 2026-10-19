# MDm – Registro Clínico de Brigadas Médicas (Honduras)

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
`python -m unittest tests.test_all` (datos, PDF, Excel, respaldos) y
`python -m unittest tests.test_ui` (interfaz; requiere pantalla).

## Limitaciones conocidas
- No incluye OCR de la hoja ATA (escritura manuscrita poco fiable); la importación desde foto sigue pendiente.
- No hay campo "número de identidad" en la Ficha Integral.
- Impresión: abre el PDF en el visor predeterminado para imprimir desde allí.
- El .exe se probó construyendo y arrancando en Linux; la compilación en Windows debe hacerla `build.bat` en su PC.
