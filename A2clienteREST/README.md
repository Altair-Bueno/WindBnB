Contiene el cliente web para acceder a los microservicios desarrollados

# Uso

## Ejecución de desarrollo

### Requisitos

- Node 19+
- npm 8+

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

Actualmente la aplicación no puede ser ejecutada en modo producción localmente

<!--
TODO update URL

Se encuentra disponible en la url: <https://example.org>
-->

# Configuración

La aplicación admite las siguientes opciones de configuración mediante ficheros
`.env` o variables de entorno

| Variable                  | Descripción                                                                | Valor por defecto |
| ------------------------- | -------------------------------------------------------------------------- | ----------------- |
| `RESERVAS_BASE_PATH`      | Url del servidor donde se encuentra el microservicio `A2reservasREST`      |
| `VIVIENDAS_BASE_PATH`     | Url del servidor donde se encuentra el microservicio `A2viviendasREST`     |
| `DATOSABIERTOS_BASE_PATH` | Url del servidor donde se encuentra el microservicio `A2datosabiertosREST` |
