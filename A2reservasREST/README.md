Contiene el microservicio encargado de gestionar la información sobre las reservas

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
export mongo_collection=<VALOR> 
export mongo_database=<VALOR>
# Iniciar el servidor
uvicorn --reload --port 8080 --host 127.0.0.0 src:app
```

## Ejecución mediante docker

### Requisitos

- Docker

### Instrucciones

```sh
# Compilar el contenedor
docker build -t a2reservas .
# Inicializar el contenedor
docker run a2reservas -p 8080:8080 \
    -e mongo_url=<VALOR> \
    -e mongo_collection=<VALOR> \
    -e mongo_database=<VALOR>
```

# Configuración

La aplicación admite las siguientes opciones de configuración mediante ficheros
`.env` o variables de entorno

| Variable | Descripción|Valor por defecto|
|-|-|-|
|`mongo_url`| URL de un servidor Mongodb | |
|`mongo_collection`| Colección donde almacenar los datos | |
|`mongo_database`| Base de datos donde buscar la colección||

# Documentación
