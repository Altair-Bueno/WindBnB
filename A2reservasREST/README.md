Contiene el microservicio encargado de gestionar la información sobre las
reservas

# Uso

## Ejecución de desarrollo

### Requisitos

- Python 3.10 o superior
- Pip3

### Instrucciones

```sh
# Crear un entorno virtual
virtualenv .venv
source .venv/bin/activate
# Instalar los paquetes necesarios
pip install -r requirements.txt

# Configuración necesaria para arrancar el servicio
export mongo_url=<VALOR>
export mongo_database=<VALOR>
# Ver la sección Configuración ...
# Iniciar el servidor
uvicorn --reload --port 8000 --host 127.0.0.0 src:app
```

## Ejecución mediante docker

### Requisitos

- Docker

### Instrucciones

```sh
# Compilar el contenedor
docker build -t a2reservas .
# Inicializar el contenedor
docker run -p 8080:8000 \
    -e mongo_url=<VALOR> \
    -e mongo_collection=<VALOR> \
    -e mongo_database=<VALOR> \
    a2reservas
```

# Configuración

La aplicación admite las siguientes opciones de configuración mediante ficheros
`.env` o variables de entorno

| Variable           | Descripción                             | Valor por defecto |
| ------------------ | --------------------------------------- | ----------------- |
| `mongo_url`        | URL de un servidor Mongodb              |                   |
| `mongo_collection` | Colección donde almacenar los datos     |                   |
| `mongo_database`   | Base de datos donde buscar la colección |                   |
| `paypal_clientid`  | Paypal client id                        |                   |
| `paypal_secret`    | Paypal client secret                    |                   |
| `paypal_url`       | Paypal API URL                          |                   |

# Documentación

Se proporciona un fichero `openapi.json` con la especificación de OpenApi.
Además, el propio servidor web proporciona la documentación sobre los endpoints
REST bajo las rutas `/docs` (SwaggerUI) y `/redoc` (Redoc)
