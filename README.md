# TP2-Mundial / ESTA LOCURAA!!!!

Seguí estos pasos para levantar el proyecto

# 1. Requisitos Previos
* Python 3.10 o superior
* MySQL Server
* Postman (o similar) para probar los endpoints

# 2. Creacion y Activación del Entorno Virtual
Desde la terminal, parado en la carpeta raíz del proyecto (`TP2-MUNDIAL`), ejecutá:

* **Crear entorno (Si no esta creado):** `python -m venv .venv`
* **Activar en Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
* **Activar en Windows (CMD):** `.\.venv\Scripts\Activate`
* **Activar en macOS/Linux:** `source .venv/bin/activate`

# 3. Instalación de Dependencias
Con el entorno virtual activo, ejecuta el siguiente comando para instalar todas las librerías necesarias:
`pip install -r requirements.txt`

# 4. Ejecución de la Base de Datos
Seguí estos pasos en orden para la configuración base de datos:

### 1. Configurar la Base de Datos en DataGrip
* En DataGrip en Database Explorer -> Data Source -> MySQL
* En la configuración, ingresa tu usuario (root) y contraseña
* Una vez conectado, hace click derecho sobre localhost y seleccioná New -> Query Console
* Copiá todo el código SQL que se encuentra dentro del archivo de la carpeta `/scripts`
* Pegalo en la consola que abriste en Datagrip

### 3. Configurar el archivo .env
* Creá un archivo llamado exactamente `.env` en la raíz del proyecto (`TP2-MUNDIAL`).
* Copiá y pegá lo siguiente dentro del archivo que acabas de crear, ajustando tu usuario y tu contraseña:
DB_USER=root
DB_PASSWORD=1234 (o tu contraseña de MySQL)

**Nota:** Prioriza que no haya espacios al momento de poner el usuario y contraseña

### 4. Iniciar el servidor
* Con el entorno virtual activo y las librerías instaladas, ejecuta 
`python backend/app.py`
* En Datagrip selecciona todo el bloque de código **HASTA LA LINEA 42** y ejecutalo con el boton de Play verde. Esto creará automáticamente la base de datos `database_tpbackend` y todas sus tablas