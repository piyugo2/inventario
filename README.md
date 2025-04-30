# Sistema de Inventario de Farmacia

Sistema de gestión de inventario para farmacias que permite registrar medicamentos, gestionar entregas y generar informes detallados. Desarrollado con Flask y Bootstrap.

![Sistema de Inventario de Farmacia](/static/img/screenshot.png)

## Características

- ✅ Registro de medicamentos individual y por importación de CSV
- ✅ Gestión de entregas con estados (Entregado, Sin Existencia, No Reclamado)
- ✅ Informes detallados de transacciones filtrados por mes/año
- ✅ Informes de resumen con estadísticas por estado
- ✅ Interfaz responsive y amigable con Bootstrap
- ✅ Base de datos SQLite para almacenamiento simple y efectivo

## Requisitos

- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge)
- Conexión a Internet para descargar dependencias

## Instalación en Windows

Siga los siguientes pasos para instalar y ejecutar la aplicación:

1. **Instalar Python**:
   - Descargue Python desde [python.org](https://www.python.org/downloads/)
   - Durante la instalación, asegúrese de marcar la opción "Add Python to PATH"
   - Verifique la instalación abriendo CMD y ejecutando:
     ```
     python --version
     ```

2. **Clonar o descargar el proyecto**:
   - Puede descargar el proyecto como ZIP y descomprimirlo, o
   - Si tiene Git instalado:
     ```
     git clone <url-del-repositorio>
     ```

3. **Crear la estructura del proyecto**:
   - Ejecute el archivo `setup_project.bat` haciendo doble clic en él
   - Esto creará la estructura de directorios y archivos necesarios

4. **Copiar los archivos de código**:
   - Copie los archivos de código en sus respectivas ubicaciones según la estructura generada

5. **Crear y activar un entorno virtual** (opcional pero recomendado):
   ```
   cd pharmacy_inventory
   python -m venv venv
   venv\Scripts\activate
   ```

6. **Instalar dependencias**:
   ```
   pip install -r requirements.txt
   ```

7. **Inicializar la base de datos**:
   ```
   python -c "from app import create_app; from models import db; app=create_app(); app.app_context().push(); db.create_all()"
   ```

8. **Ejecutar la aplicación**:
   ```
   python app.py
   ```

9. **Acceder a la aplicación**:
   - Abra su navegador y vaya a: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Uso rápido

1. **Agregar medicamentos**: Vaya a la sección "Medicamentos" y agregue medicamentos individualmente o importe un archivo CSV.

2. **Registrar entregas**: En la sección "Entregas", seleccione un medicamento, la cantidad, unidad y el estado correspondiente.

3. **Generar informes**: Acceda a la sección "Informes" y elija entre ver "Transacciones Detalladas" o "Resumen por Estado".

## Problemas comunes y soluciones

- **Error al instalar dependencias**: Asegúrese de tener conexión a Internet y que pip esté actualizado:
  ```
  python -m pip install --upgrade pip
  ```

- **Base de datos no se crea**: Verifique que tiene permisos de escritura en el directorio de la aplicación.

- **La aplicación no inicia**: Compruebe que todas las dependencias están instaladas y que está utilizando Python 3.8+.

## Respaldo y migración

- El archivo de base de datos SQLite se guarda como `pharmacy_inventory.db` en el directorio raíz
- Para hacer un respaldo, simplemente copie este archivo
- Para migrar a otro sistema, copie este archivo a la nueva instalación

## Licencia

Este proyecto está licenciado bajo [LICENCIA].

## Contacto

Para soporte o consultas: [su-email@example.com]