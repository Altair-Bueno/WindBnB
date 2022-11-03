Contiene el microservicio encargado de servir los datos abiertos escogidos

# Uso

## Ejecución de desarrollo

### Requisitos

- Python 3.9 o superior
- pip3

### Instrucciones

```sh
# Crear un entorno virtual
virtualenv .venv
source .venv/bin/activate
# Instalar los paquetes necesarios
pip install -r requirements.txt
# Iniciar el servidor
uvicorn --reload --port 8080 --host 0.0.0.0 src:app
```

## Ejecución mediante docker

### Requisitos

- Docker

### Instrucciones

```sh
# Compilar el contenedor
docker build -t a2reservas .
# Inicializar el contenedor
docker run a2reservas -p 8080:8080
```

# Documentación

Se proporciona un fichero `openapi.json` con la especificación de OpenApi.
Además, el propio servidor web proporciona la documentación sobre los endpoints
REST bajo las rutas `/docs` (SwaggerUI) y `/redoc` (Redoc)