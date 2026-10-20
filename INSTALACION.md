# Instalar Expedientes MdM en otra computadora (Windows)

## Qué necesita
1. **Python 3.10 o más nuevo** (python.org). Al instalar, marque **«Add python.exe to PATH»** y deje la opción de **tcl/tk**.
2. **Google Chrome**, para el llenado de ActivityInfo. La primera vez que se llena un registro hace falta internet
   (Selenium descarga solo el controlador de Chrome).
3. Una **cuenta de ActivityInfo** con acceso al formulario. El programa no guarda contraseñas: la persona inicia sesión
   en la ventana de Chrome que abre el programa y la sesión queda guardada en un perfil propio.

## Pasos
1. Copie la carpeta del programa (o descárguela de GitHub con *Code → Download ZIP* y descomprímala).
   No copie la carpeta `.venv` si viene de otra computadora: se crea sola.
2. Doble clic en **`iniciar_MDm.bat`**. La primera vez prepara todo solo (varios minutos, con internet); después abre directo.
3. Abra **Configuración** y escriba los datos fijos (lugar de atención, proyecto, profesional…).

## Dónde quedan los datos
En `%LOCALAPPDATA%\BrigadasMedicas` (base de datos, respaldos, exportaciones y el perfil de Chrome). Cada computadora
empieza con su propia base vacía. Para llevarse los datos a otra computadora, use *Copias de seguridad* y restaure ahí.

## Si algo falla
- «No se encontró Python»: reinstálelo marcando *Add python.exe to PATH*.
- «Falta Tkinter»: reinstale Python con la opción *tcl/tk and IDLE*.
- El llenado de ActivityInfo nunca guarda ni crea la ficha: se revisa y se guarda a mano.
- Los errores quedan en el archivo de registro de la carpeta de datos.
