@echo off
echo Creando estructura de directorios para el Sistema de Inventario de Farmacia...

REM Crear directorio principal y subdirectorios
mkdir pharmacy_inventory
cd pharmacy_inventory
mkdir static
mkdir static\css
mkdir static\js
mkdir static\img
mkdir templates
mkdir models

REM Crear archivos Python principales
echo # Archivo principal de la aplicación Flask > app.py
echo # Archivo de configuración > config.py
echo # Listado de dependencias > requirements.txt

REM Crear archivos de modelos
echo # Paquete de modelos > models\__init__.py
echo # Configuración de base de datos > models\database.py
echo # Modelo de medicamentos > models\medicamento.py
echo # Modelo de transacciones > models\transaccion.py

REM Crear archivos de plantillas HTML
echo {% extends 'base.html' %} > templates\index.html
echo <!DOCTYPE html> > templates\base.html
echo {% extends 'base.html' %} > templates\medicamentos.html
echo {% extends 'base.html' %} > templates\entregas.html
echo {% extends 'base.html' %} > templates\informes.html
echo {% extends 'base.html' %} > templates\transacciones.html
echo {% extends 'base.html' %} > templates\resumen.html

REM Crear archivos estáticos
echo /* Estilos personalizados */ > static\css\main.css
echo // JavaScript personalizado > static\js\main.js

REM Crear archivo README.md
echo # Sistema de Inventario de Farmacia > README.md

echo.
echo ¡Estructura de proyecto creada correctamente!
echo El directorio del proyecto es: %cd%
echo.
echo Ahora puede copiar los archivos fuente en sus respectivas ubicaciones.
echo.
pause