Contiene el microservicio encargado de gestionar la información sobre las
viviendas

# Uso

## Ejecución de desarrollo

### Requisitos

- Python 3.10 o superior
- Pip3

### Instrucciones

```sh
# Crear un entorno virtual
virtualenv .venv
source .venv/bin/activate (Linux o MacOS)
./.venv/Scripts/activate (Windows)
# Instalar los paquetes necesarios
pip install -r requirements.txt

# Iniciar el servidor
uvicorn app:app --reload
```

## Ejecución mediante docker

### Requisitos

- Docker

### Instrucciones

```sh
# Compilar el contenedor
docker build -t a2viviendas .
# Inicializar el contenedor
docker run a2viviendas -p 8080:8000 \ -e mongo_url=<VALOR>\ -e mongo_collection=<VALOR>\ -e mongo_database=<VALOR> (Linux y MacOs)
docker run a2viviendas -p 8080:8000 -e mongo_url=<VALOR> -e mongo_collection=<VALOR> -e mongo_database=<VALOR> (Windows)
```

# Configuración

| Variable           | Descripción                             | Valor por defecto |
| ------------------ | --------------------------------------- | ----------------- |
| `mongo_url`        | URL de un servidor Mongodb              |                   |
| `mongo_collection` | Colección donde almacenar los datos     |                   |
| `mongo_database`   | Base de datos donde buscar la colección |                   |
| `mongo_valoraciones` | Colección donde almacenar los datos   |                   |
| `auth_audience`    | Audicencia JWT                          |                   |
| `auth_baseurl`     | URL base donde se encuentra el JWK público|                   |


# Documentación

Se proporciona un fichero `openapi.json` con la especificación de OpenApi.
Además, el propio servidor web proporciona la documentación sobre los endpoints
REST bajo las rutas `/docs` (SwaggerUI) y `/redoc` (Redoc)

