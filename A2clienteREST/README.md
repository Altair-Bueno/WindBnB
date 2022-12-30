Contiene el cliente web para acceder a los microservicios desarrollados

# Uso

## Ejecución de desarrollo

### Requisitos

- Node 19+
- npm 8+
- Java JDK 1.8+

### Instrucciones

```sh
# 1. Instalar las dependencias
npm i
# 2. Compilar la api. Se debe de ejecutar en cada cambio en la especificación
npm run openapi
# 3. Iniciar el servidor
npm run dev
```

## Ejecución de producción

La aplicación ha sido configurada para ser desplegada en Vercel para producción.

La aplicación se encuentra desplegada en <https://windbnb-fawn.vercel.app/>

# Configuración

La aplicación admite las siguientes opciones de configuración mediante ficheros
`.env` o variables de entorno

| Variable                   | Descripción                                                                | Valor por defecto |
| -------------------------- | -------------------------------------------------------------------------- | ----------------- |
| `RESERVAS_BASE_PATH`       | Url del servidor donde se encuentra el microservicio `A2reservasREST`      |
| `VIVIENDAS_BASE_PATH`      | Url del servidor donde se encuentra el microservicio `A2viviendasREST`     |
| `DATOSABIERTOS_BASE_PATH`  | Url del servidor donde se encuentra el microservicio `A2datosabiertosREST` |
| `POSITION_STACK_API_KEY`   | ApiKey de http://api.positionstack.com                                     |
| `CLOUDINARY_CLOUD_NAME`    | Cloud name de Cloudinary                                                   |
| `CLOUDINARY_UPLOAD_PRESET` | Upload preset de Cloudinary                                                |
| `PUBLIC_PAYPAL_CLIENTID`   | Client ID de Paypal                                                        |
| `AUTH0_CLIENTSECRET`       | Client secret de Auth0                                                     |
| `PUBLIC_AUTH0_CLIENTID`    | Client ID de Auth0                                                         |
| `PUBLIC_AUTH0_BASEURL`     | Base URL del dominio Auth0                                                 |
| `PUBLIC_AUTH0_AUDIENCE`    | Audiencia del dominio Auth0                                                |
