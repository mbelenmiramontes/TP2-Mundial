# API Backend de ProDe - Mundial 2026

Este proyecto consiste en el desarrollo de una API utilizando Python y Flask para gestionar el fixture y un ProDe para el Mundial de 2026. La API permite administrar partidos, registrar resultados, gestionar usuarios y calcular un ranking de puntos basado en las predicciones.

### Integrantes del grupo
* Agustina Santos - 115127
* Bautista Rago Bustabas 115781
* Facundo Ariel Mamani - 115292
* Julián López Azar - 115400
* Luciano Chirito - 115334
* María Belén Miramontes - 114841
* Martin Guan - 115115
* Sabrina Araceli Sarmiento - 115361
* Sofia Abril Rial - 115584

# 1. Instrucciones de ejecución
Segui estos pasos para levantar el proyecto

### 1. Requisitos previos
* Python 3.10 o superior
* MySQL Server
* Postman (o similar) para probar los endpoints

### 2. Creacion y Activación del Entorno Virtual
Desde la terminal, parado en la carpeta raíz del proyecto (`TP2-MUNDIAL`), ejecutá:

* **Crear entorno (Si no esta creado):** `python -m venv .venv`
* **Activar en Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
* **Activar en Windows (CMD):** `.\.venv\Scripts\Activate`
* **Activar en macOS/Linux:** `source .venv/bin/activate`

### 3. Instalación de Dependencias
Con el entorno virtual activo, ejecuta el siguiente comando para instalar todas las librerías necesarias:
`pip install -r requirements.txt`

# 2. Ejecución de la Base de Datos
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
* La API estará disponible en: `http://localhost:8000`
* En Datagrip selecciona todo el bloque de código **HASTA LA LINEA 42** y ejecutalo con el boton de Play verde. Esto creará automáticamente la base de datos `database_tpbackend` y todas sus tablas

# 3. Funcionamiento del código
La estructura del proyecto sigue una separación de capas para facilitar el mantenimiento y la escalabilidad:

* `app.py`: Punto de entrada de la aplicación, configura Flask y registra los blueprints de cada módulo
* Capas de Rutas (`rutas/`): Define los endpoints de la API, se encarga de recibir las peticiones, validar parámetros como el limit y offset de paginación y devolver las respuestas JSON con los códigos de estado correspondientes.
* Capas de Controladores (`controladores/`): Procesa los datos, interactúa con la base de datos y realiza validaciones complejas como verificar que un partido no se haya jugado antes de permitir una predicción.
* Capa de Base de Datos (`database`): Centraliza la conexión y ejecución de queries mediante `mysql-connector`
* `HATEOAS`: Las respuestas de los listados incluyen enlaces de navegación (`_first, _next, _prev, _last`)

# 4. Ejemplos de Uso
A continuación se muestran ejemplos básicos de lo que se espera como resultado de algunos de los endpoint.

**Validaciones a conocer antes de ejecutar**

* Equipos no pueden ser iguales.
* No se permiten partidos duplicados.
* Fases válidas: grupos, dieciseisavos, octavos, cuartos, semis, final.
* Fecha en formato YYYY-MM-DD
* Goles deben ser enteros ≥ 0
* Restricciones de Predicción: Solo se puede predecir un partido que no haya comenzado y solo una vez por usuario.
* Puntaje ProDe: 3 puntos por resultado exacto, 1 punto por acertar ganador/empate.

# Gestión de usuarios
* Crear usuario: `POST /usuarios`

**Body:**
{
  "nombre": "Bruno Lanzillota",
  "email": "blanzillota@fi.uba.ar"
}

**Response (201 Created):**
{
  "id": 1
}


* Consultar usuarios: `GET /usuarios`

**Response (200 OK):**
{
  "total": 1,
  "usuarios": [
    {
      "id": 1,
      "nombre": "Bruno Lanzillota",
      "email": "blanzillota@fi.uba.ar"
    }
  ],
  "_links": {
    "_first": { "href": "/usuarios?_limit=10&_offset=0" },
    "_last": { "href": "/usuarios?_limit=10&_offset=0" }
  }
}


* Obtener usuario por ID: `GET /usuarios/1`

**Response (200 OK):**
{
  "id": 1,
  "nombre": "Bruno Lanzillota",
  "email": "blanzillota@fi.uba.ar"
}


* Actualizar usuario: `PUT /usuarios/1`

**Body:**
{
  "nombre": "Bruno Lanzillota Modificado",
  "email": "bruno.nuevo@fi.uba.ar"
}

**Response**: *204 No content*


* Eliminar usuario: `DELETE /usuarios/1`

**Response**: *204 No content*


# Gestión de partidos
* Crear partido: `POST /partidos`

**Body:**
{
  "equipo_local": "Argentina",
  "equipo_visitante": "Brasil",
  "fecha": "2026-06-10",
  "fase": "GRUPOS"
}

**Response (201 Created):**
{
  "mensaje": "Partido creado exitosamente",
  "id": 1
}


* Consultar partidos: `GET /partidos`

**Response (200 OK):**
{
  "partidos": [
    {
      "equipo_local": "Argentina",
      "equipo_visitante": "Brasil",
      "fase": "grupos",
      "fecha": "Wed, 10 Jun 2026 00:00:00 GMT",
      "id": 1
    }
  ],
  "_links": {
    "_first": { "href": "..." },
    "_last": { "href": "..." }
  }
}


* Cargar resultado del partido: `PUT /partidos/1/resultados`

**Body:**
{
  "local": 2,
  "visitante": 1
}

**Response:** *204 No content*


* Crear una prediccion: `POST /partidos/1/prediccion`

**Body:**
{
  "id_usuario": 1,
  "goles_local": 2,
  "goles_visitante": 1
}

**Response (201 Created):**
{
  "message": "Predicción registrada correctamente."
}


* Actualizar un Partido: `PUT /partidos/1`

**Body:**
{
  "equipo_local": "Argentina",
  "equipo_visitante": "Uruguay",
  "fecha": "2026-06-12",
  "fase": "grupos"
}

**Response:** *204 No content*

### Ejemplo de Error
`POST /partidos`

**Body:**
{
  "equipo_local": "Argentina",
  "equipo_visitante": "Argentina",
  "fecha": "2026-06-10",
  "fase": "GRUPOS"
}

**Response (400 Bad Request):**
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

# Gestión de Ranking
* Consultar Ranking: `GET /ranking`

**Response (200 OK):**
{
  "total": 2,
  "ranking": [
    {
      "id_usuario": 1,
      "puntos": 3
    },
    {
      "id_usuario": 2,
      "puntos": 1
    }
  ],
  "_links": {
    "_first": { "href": "/ranking?_limit=10&_offset=0" },
    "_next": { "href": "/ranking?_limit=10&_offset=10" },
    "_prev": { "href": null },
    "_last": { "href": "/ranking?_limit=10&_offset=20" }
  }
}
