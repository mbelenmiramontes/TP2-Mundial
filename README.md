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

### 2. Configurar el archivo .env
* Creá un archivo llamado exactamente `.env` en la raíz del proyecto (`TP2-MUNDIAL`).
* Copiá y pegá lo siguiente dentro del archivo que acabas de crear, ajustando tu usuario y tu contraseña:
DB_USER=root
DB_PASSWORD=1234 (o tu contraseña de MySQL)

**Nota:** Prioriza que no haya espacios al momento de poner el usuario y contraseña

### 3. Iniciar el servidor
* Con el entorno virtual activo y las librerías instaladas, ejecuta 
`python backend/app.py`
* En Datagrip selecciona todo el bloque de código **HASTA LA LINEA 42** y ejecutalo con el boton de Play verde. Esto creará automáticamente la base de datos `database_tpbackend` y todas sus tablas

# 5. Ejemplos de Uso
A continuación se muestran ejemplos básicos de lo que se espera como resultado de algunos de los endpoint.

**Validaciones a conocer antes de ejecutar**

* Equipos no pueden ser iguales
* Fases restringidas a valores válidos
* Fecha en formato YYYY-MM-DD
* No se permiten partidos duplicados
* Goles deben ser enteros ≥ 0

### Crear Usuario
`POST /usuarios`

**Body:**

{
  "nombre": "Mohamaad",
  "email": "mohamaad@email.com"
}

**Response:**

{
  "id": 1,
  "nombre": "Mohamaad",
  "email": "mohamaad@email.com"
}

### Crear Partido
`POST /partidos`

**Body:**

{
  "equipo_local": "Argentina",
  "equipo_visitante": "Brasil",
  "fecha": "2026-06-10",
  "fase": "grupos"
}

**Response:**

{
  "mensaje": "Partido creado exitosamente",
  "id": 1
}

### Consultar Partidos
`GET /partidos`

**Response:**

{
  "total": 1,
  "partidos": [
    {
      "id": 1,
      "equipo_local": "Argentina",
      "equipo_visitante": "Brasil",
      "fecha": "2026-06-10",
      "fase": "grupos"
    }
  ]
}

### Filtrar Partidos
`GET /partidos?equipo=Argentina`

### Cargar Resultado del Partido
`PUT /partidos/1/resultados`

**Body:**

{
  "local": 2,
  "visitante": 1
}

**Response:**

*204*

### Crear una Predicción
`POST /partidos/1/prediccion`

**Body:**

{
  "usuario_id": 1,
  "goles_local": 2,
  "goles_visitante": 1
}

**Response:**

*201*

### Actualizar un Partido
`PUT /partidos/1`

**Body:**

{
  "equipo_local": "Argentina",
  "equipo_visitante": "Uruguay",
  "fecha": "2026-06-12",
  "fase": "grupos"
}

**Response:**

*204*

### Ejemplo de Error
`POST /partidos`

**Body:**

{
  "equipo_local": "Argentina",
  "equipo_visitante": "Argentina",
  "fecha": "2026-06-10",
  "fase": "grupos"
}

**Response:**

{
  "errors": [
    {
      "code": "400",
      "message": "Bad Request",
      "level": "error",
      "description": "El equipo local y visitante no pueden ser el mismo"
    }
  ]
}
