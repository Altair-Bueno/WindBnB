Contiene el cliente web para acceder a los microservicios desarrollados

# Uso

## Ejecución de desarrollo

### Requisitos

- Node 19+
- npm 8+

### Instrucciones

```sh
# Instalar las dependencias
npm i
# Compilar la api
npm run openapi
# Iniciar el servidor
npm run dev
```

# Configuración

La aplicación admite las siguientes opciones de configuración mediante ficheros
`.env` o variables de entorno

| Variable                  | Descripción                                                                | Valor por defecto |
| ------------------------- | -------------------------------------------------------------------------- | ----------------- |
| `RESERVAS_BASE_PATH`      | Url del servidor donde se encuentra el microservicio `A2reservasREST`      |
| `VIVIENDAS_BASE_PATH`     | Url del servidor donde se encuentra el microservicio `A2viviendasREST`     |
| `DATOSABIERTOS_BASE_PATH` | Url del servidor donde se encuentra el microservicio `A2datosabiertosREST` |
