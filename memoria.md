---
title: "Práctica de servicios Web (I): servidores"
author:
  - "Alvaro Tapia Muñoz"
  - "Jose Luis Bueno Pachón"
  - "Carlos Marín Corbera"
  - "Carmen González Ortega"
  - "Altair Bueno Calvente"
date: 11 oct 2022
titlepage: true
titlepage-rule-color: "4506B3"
toc-own-page: true
toc: true
---

<!--
TODO

- Indicar despliegue de los servicios con docker compose `docker compose up -d`. Esto está en el README.md
- Rellenar los datos de `iweb/iweb.json`
-->

# Introducción

# Esquema de las entidades

Los documentos almacenados en Mongo mantienen el siguiente esquema:

```json
{
  // Clave primaria de Mongo
  "_id": "ObjectId",
  // Titulo de la vivienda
  "title": "string",
  // Descripción de la vivienda
  "description": "string",
  // Identificador del usuario dueño de la vivienda
  "user_id": "string",
  // Ubicación de la vivienda
  "location": "string",
  // Estado de la vivienda. Por defecto: available
  "state": "enum(available,deleted)",
  // Lista de todas las reservas que ha recibido esta vivienda
  "bookings": [
    {
      "_id": "ObjectId",
      // Identificador del usuario que hace la reserva
      "user_id": "string",
      // Fecha de inicio de la reserva en formato YYYY-MM-DD
      "start_date": "string",
      // Fecha de fin de la reserva en formato YYYY-MM-DD
      "end_date": "string",
      // Estado de la reserva. Por defecto: reserved
      "state": "enum(reserved,canceled)"
    }
  ]
}
```

## Datos de prueba para Mongo

En el interior de la carpeta `iweb`, se proporciona un fichero `houses.json` con
el volcado de la colección de pruebas. Para restaurarla, basta con realizar una
inserción de multiples elementos del contenido del fichero. Para automatizar el
proceso, se proporciona un script de Python `iweb.py`. Requiere que la librería
`pymongo` esté instalada

# Descripción de los servicios

## A2ReservasREST

Este microservicio se encarga de proporcionar los datos sobre las reservas. Esta
desarrollado en Python utilizando el framework
[FastAPI](https://fastapi.tiangolo.com). Para la persistencia de datos utiliza
[MongoDB](https://www.mongodb.com/), a través del driver asíncrono
[Motor](https://motor.readthedocs.io/en/stable/index.html).

Para facilitar el despliegue de la aplicación, se proporciona un fichero
`Dockerfile` para construir un contenedor de [Docker](https://docker.com). Las
instrucciones detalladas sobre como utilizar la imagen y las opciones de
configuración disponibles se pueden encontrar en el fichero `README.md`, dentro
de la carpeta `A2ReservasREST`.

### Requisitos considerados

- **Al menos dos operaciones de consulta o búsqueda parametrizada**:
  `GET /booking`, `GET /booking/{booking_id}`, `DELETE /booking/{booking_id}`
- **Una operación de consulta sobre las relaciones entre las entidades**:
  `GET /booking` y su parámetro de consulta `owner_id`

### Endpoints REST disponibles

La siguiente lista es una especificación informal sobre los endpoints REST
disponibles en el microservicio, a modo de resumen. La documentación completa se
puede encontrar en el propio servidor, bajo las rutas `/docs` (SwaggerUI) y
`/redoc` (Redoc). Además, se adjunta una copia local en el fichero
`openapi.json`, dentro de la carpeta del proyecto.

- `GET /booking`: Devuelve una lista de reservas que cumplan con los filtros
  especificados. 10 reservas como máximo. Los parámetros de consulta son:
  - `skip`: Número de reservas a ignorar
  - `user_id`: Identificador de usuario (quien realiza la reserva)
  - `owner_id`: Identificador de usuario (propietario de la vivienda)
  - `before_date`: Fechas de fin anteriores
  - `after_date`: Fechas de inicio posteriores
  - `sort_by`: Campo utilizado para ordenar
  - `ascending`: Ordenar de forma ascendente. Por defecto: `false`
- `POST /booking`: Crea una nueva reserva. El cuerpo de la petición es un json
  con los siguientes campos:
  - `user_id`: Identificador del usuario que realiza la reserva
  - `house_id`: Identificador de la vivienda
  - `start_date`: Fecha de inicio de la reserva
  - `end_date`: Fecha de inicio de la reserva
- `GET /booking/{booking_id}`: Devuelve toda la información sobre la reserva con
  identificador `booking_id`
- `DELETE /booking/{booking_id}`: Cancela la reserva con identificador
  `booking_id`
- `GET /ping`: Ruta utilizada para validar que el servicio se encuentra
  disponible

# Datos Abiertos

## Precio de carburantes en las gasolineras españolas

Hemos escogido un [conjunto de datos abiertos](https://datos.gob.es/es/catalogo/e05068001-precio-de-carburantes-en-las-gasolineras-espanolas) con información sobre todas las gasolineras de España, incluyendo información sobre su posición geográfica, dirección y precio de los carburantes ofertados. Este será utilizado para mostrar en un mapa las gasolineras cercanas a una vivienda publicada en la aplicación, o las gasolineras en una determinada provincia.

