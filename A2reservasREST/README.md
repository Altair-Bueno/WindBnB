# Uso

## Ejecución de desarrollo

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

export mongo_url=<MONGO_URL>
export mongo_collection=<MONGO_COLLECTION> 
export mongo_database=<MONGO_DATABASE>
uvicorn --reload --port 8080 --host 127.0.0.0 src:app
```

## Ejecución mediante docker

```sh
docker build -t a2reservas .
docker run a2reservas -p 8080:8080 \
    -e mongo_url=<MONGO_URL> \
    -e mongo_collection=<MONGO_COLLECTION> \
    -e mongo_database=<MONGO_DATABASE>
```

# Configuración

La aplicación admite las siguientes opciones de configuración mediante ficheros
`.env` o variables de entorno

| Variable | Descripción|Valor por defecto|
|-|-|-|
|`mongo_url`| URL de un servidor Mongodb | |
|`mongo_collection`| Colección donde almacenar los datos | |
|`mongo_database`| Base de datos donde buscar la colección||

