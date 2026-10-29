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

## Cómo actualizar el programa (sin perder nada)

Los pacientes y las copias de seguridad **no están dentro de la carpeta del programa** (están en `AppData\Local\BrigadasMedicas`), así que actualizar el programa no los borra.

1. Cierre el programa.
2. Descargue de nuevo el ZIP desde GitHub (botón verde **Code** → **Download ZIP**).
3. Haga clic derecho sobre el ZIP → **Propiedades** → marque **Desbloquear** → **Aceptar** (si no, Windows bloquea los archivos nuevos).
4. Descomprima el ZIP en cualquier lugar (por ejemplo, el Escritorio).
5. Abra la carpeta descomprimida, seleccione **todo** su contenido y cópielo encima de la carpeta donde tiene instalado el programa. Cuando Windows pregunte, elija **Reemplazar los archivos en el destino**.
6. **No borre** la carpeta oculta `.venv` de la carpeta instalada: ahí están los componentes ya instalados y evita esperar otra vez.
7. Abra `iniciar_MDm.bat` como siempre.
8. Compruebe la versión: debajo de «Expedientes MdM», arriba a la izquierda, dice **v2.6** (o la más nueva). Si dice otra más vieja, los archivos no se reemplazaron: repita desde el paso 2.

Solo si alguna actualización indica que cambiaron los componentes (la lista `requirements.txt`), borre el archivo `.venv\listo.txt` y vuelva a abrir `iniciar_MDm.bat`: así descarga los componentes nuevos (necesita internet).
