Contiene el microservicio encargado de gestionar la información sobre las
reservas

# Uso

## Ejecución de desarrollo

### Requisitos

- Python 3.11 o superior
- Pip3
- GNU Make

### Instrucciones

```sh
# Crear el entorno virtual e instalar dependencias
make install
# Arrancar el entorno de desarrollo
make dev
```

## Ejecución mediante docker

### Requisitos

- Docker

### Instrucciones

```sh
# Compilar el contenedor
docker build -t a2reservas .
# Inicializar el contenedor. Añadir las variables de entorno que faltan
# Ver la sección Configuración ...
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
| `auth_audience`    | JWT audience                            |                   |
| `auth_baseurl`     | Base url where to find public JWK       |                   |

# Documentación

Se proporciona un fichero `openapi.json` con la especificación de OpenApi.
Además, el propio servidor web proporciona la documentación sobre los endpoints
REST bajo las rutas `/docs` (SwaggerUI) y `/redoc` (Redoc)
