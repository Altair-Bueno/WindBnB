---
title: "Práctica de computación en la nube"
author:
  - "Álvaro Jesús Tapia Muñoz"
  - "Jose Luis Bueno Pachón"
  - "Carlos Marín Corbera"
  - "Carmen González Ortega"
  - "Altair Bueno Calvente"
date: 23 dic 2022
titlepage: true
titlepage-rule-color: "4506B3"
toc-own-page: true
toc: true
---

<!--

Nota: credenciales PayPal

```json
[
  {
    "email": "sb-5qp7q22405408@personal.example.com",
    "password": "2o}yF$ct"
  }
]
```
-->

[x] la(s) URL(s) donde está desplegada la aplicación en la nube.
[x] las tecnologías utilizadas en la práctica (proveedor cloud, lenguajes, bibliotecas, frameworks, base de datos, etc.)
[ ] los principales requisitos del caso de estudio considerados en la práctica y cómo se han abordado desde un punto de vista técnico (es decir, el uso que se ha hecho de las tecnologías y APIs mencionadas anteriormente). 
[ ] la arquitectura de la aplicación y su esquema de navegación, por ejemplo, actualizando los esquemas desarrollados en la primera entrega.
[x] las entidades de la base de datos, sus propiedades (columnas de las tablas) y la relación entre ellas, así como las credenciales o una cuenta de usuario que permita acceder a los datos almacenados en la base de datos.
[x] instrucciones y scripts de instalación y despliegue de las aplicaciones, en particular si utilizáis cualquier tecnología diferente de las presentadas en clase.
[x] descripción de los conjuntos de datos abiertos utilizados, incluyendo sus puntos de acceso.
[ ] descripción de la API REST desarrollada, especialmente si se han realizado cambios respecto a la anterior entrega del caso de estudio.
[x] la funcionalidad de la capa de presentación o la aplicación cliente. 

# Despliegue

Para el despliegue de la parte frontend de la aplicación se ha hecho uso del proveedor [Vercel](https://vercel.com/)

Para el despliegue de la parte backend de la aplicación se ha hecho uso del proveedor [Fly.io](https://fly.io)

La base de datos se encuentra alojada en un cluster de [MongoDB Atlas](https://www.mongodb.com/atlas)

- La aplicación se encuentra desplegada en <https://windbnb-fawn.vercel.app>
- Los microservicios A2viviendasREST, A2datosabiertosREST y A2reservasREST están desplegados respectivamente en:
  - <https://a2viviendas.fly.dev>
  - <https://a2datosabiertos.fly.dev>
  - <https://a2reservas.fly.dev>

# Requisitos considerados

Se han considerado los siguientes requisitos para la realización del cliente
REST:

- **El almacenamiento de datos se realizará en una base de datos no relacional**
- **Identificación de los usuarios de la aplicación haciendo uso de técnicas basadas en OAuth**
- **La aplicación permitirá la interacción entre sus usuarios mediante un sistema de comentarios y valoraciones**
- **Integración de un servicio de pago en la aplicación**
- **La aplicación estará desplegada en la nube**

# Tecnologías Utilizadas

Durante el desarrollo de la interfaz del cliente se han usado los frameworks
[Astro](https://astro.build/), [Svelte](https://svelte.dev/) y
[Bootstrap](https://getbootstrap.com) para la generación de las páginas y
componentes usando Typescript. Para los mapas se ha usado la librería
[Leaflet](https://leafletjs.com/) que hace a su vez uso de OpenStreetMaps.
El proveedor OAuth2 escogido es [Auth0](https://auth0.com).

Para la persistencia de datos se ha optado por la base de datos de
[MongoDB](https://www.mongodb.com/), conectada a través del driver asíncrono
[Motor](https://motor.readthedocs.io/en/stable/index.html), al igual que con el
servidor REST, y para el servicio cloud de almacenamiento de imágenes
[Cloudinary](https://cloudinary.com/).

# Arquitectura de la aplicación y esquema de navegación

![Modelo IFML]()

El esquema de navegación de la aplicación consta de una página principal a la que se puede acceder sin credenciales. Desde ella, el usuario puede iniciar sesión, cambiando a un proveedor externo [Auth0](https://auth0.com), o crear una nueva vivienda (si ha iniciado sesión), o ver sus reservas (si ha iniciado sesión) o ver los detalles de una vivienda en concreto. Dentro de la vista de detalles de la vivienda, el usuario puede eliminar o editar dicha vivienda, siempre que el usuario que esté con la sesión iniciada coincida con el usuario que publicó la vivienda. Además se puede reservar la vivienda, si el usuario no es el dueño, cambiando a un proveedor externo [PayPal](https://www.paypal.com/es/home) para realizar el pago. Dentro de la vista de reservas de un usuario aparece una lista con las reservas, pudiéndose filtrar y cancelar. Dentro de las vistas de creación y edición de una vivienda, aparece un formulario con los campos de dicha vivienda y un botón para realizar la acción correspondiente. Al eliminar una vivienda, se pide confirmación explícita en otra vista.

# Base de datos

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
  //Lista de fotos de la vivienda
  "url_photo": ["string"],
  //Coordenada geográfica longitud
  "longitude": "string",
  //Coordenada geográfica latitud
  "latitude": "string",
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
  ],
  // Lista de todas las valoraciones de esta vivienda
  "valorations": [
    {
      "_id": "ObjectId",
      // Identificador del usuario que hace la valoración
      "user_id": "string",
      // Valoración de la vivienda entre 0 y 10
      "valoracion": "integer",
      // Comentario de la vivienda
      "comentario": "string",
      // Estado de la reserva. Por defecto: reserved
      "state": "enum(reserved,canceled)"
    }
  ]
}
```

Acceso a la base de datos:

- `mongo_url=mongodb+srv://root:root@windbnb.uecdw2z.mongodb.net`

Credenciales:

- Usuario: `root`
- Contraseña: `root`

# Instrucciones de Despliegue

Los todos los microservicios que conforman el backend de la aplicación pueden
ser desplegados a través de
[Docker Compose](https://docs.docker.com/compose/compose-v2/), o bien
desplegarlos individualmente mediante [Docker](https://docker.com) o
[uvicorn](https://www.uvicorn.org) (más información sobre el despliegue de cada
uno de los servicios se puede encontrar en el fichero `README.md` en la carpeta
de cada microservicio).

El cliente web está configurado para ser desplegado en Vercel, por lo que no se
proporciona un método para lanzar el servicio en producción localmente. Para más
información sobre como desplegar el servicio en modo desarrollo, visite el
fichero `A2clienteREST/README.md`.

# Conjunto de datos abiertos

El microservicio encargado de servir los datos abiertos es `A2datosabiertosREST`

## Precio de carburantes en las gasolineras españolas

El conjunto de datos abiertos relacionado con 
[las gasolineras de España](https://datos.gob.es/es/catalogo/e05068001-precio-de-carburantes-en-las-gasolineras-espanolas)
incluye información
sobre su posición geográfica, dirección y precio de los carburantes ofertados
de cada gasolinera.
Este será utilizado para mostrar en el mapa las gasolineras cercanas a la
vivienda publicada en una determinada
provincia.

### Endpoints

- `GET /gas-stations`: Devuelve una lista de gasolineras (`List[EESSPrecio]`)
  filtrados por provincia y rótulo. Por defecto 10 gasolineras como máximo

  - `provincia`: `Optional[str]`. Nombre de la provincia
  - `rotulo`: `Optional[str]`. Nombre de la marca o rótulo de la gasolinera
  - `limit`: `int`. Número máximo de elementos a devolver. Por defecto, el valor
    es 10

- `GET /gas-stations/{latitude}/{longitude}`: Devuelve una lista de gasolineras
  (`List[EESSPrecio]`) que se encuentran como máximo en un área a partir de una
  geolocalización. Por defecto 10 gasolineras como máximo.
  - `latitude`: `float`. Latitud de la vivienda
  - `longitude`: `float`. Longitud de la vivienda
  - `area`: `int`. Límite del área en kilómetros. Por defecto, el valor es 5
  - `limit`: `int`. Número máximo de elementos a devolver. Por defecto, el valor
    es 10

El modelo del tipo de salida `EESSPrecio` se puede ver en
`A2datosabiertosREST/src/models/gas_stations.py` en modo local.

## Estancia media de los viajeros por provincias y meses

El conjunto de datos abiertos relacionado con la
[estancia media de viajeros](https://datos.gob.es/es/catalogo/ea0010587-estancia-media-de-los-viajeros-por-provincias-y-meses-eoap-identificador-api-t11-e162eoap-a2020-l0-01ndp03-px)
contiene información de la estancia media en días de los viajeros por
provincia y mes según la vivienda. 

### Endpoints

- `GET /average-stay`: Devuelve el valor de la estancia media (`Data`) de
  viajeros de una provincia en un mes o año.
  - `provincia`: `str`. Nombre de la provincia
  - `mes`: `Optional[str]`. Nombre del mes

El modelo del tipo de salida `Data` se puede ver en
`A2datosabiertosREST/src/models/average_stay.py` en modo local.

## Casos Alternativos

En el caso de que no se introduzca una entrada correcta, se han definido dos
excepciones que se elevarán cuando sea oportuno: `NoGasStations` y
`NoDataFound`. Si no se encuentran resultados en la búsqueda, el endpoint
devuelve un mensaje indicándolo.

### NoGasStations Exception

En el caso de `NoGasStations`, se puede mostrar en dos ocasiones. Cuando no hay
gasolineras dado una provincia y rótulo se mostraría un objeto

```json
{
  "message": "No {rotulo} gas stations found in {provincia}"
}
```

O, en el caso de que no haya gasolineras dado un radio de búsqueda, una latitud
y una longitud, se mostraría otro objeto de la misma forma

```json
{
  "message": "No gas stations found within {kilometers}km from [{latitude}º, {longitude}º]"
}
```

### NoDataFound Exception

Cuando buscamos la estancia media dada una provincia y un mes (o la media
anual), puede darse el caso de que no haya datos sobre ello. No es que no se
encuentre el recurso, simplemente que no hay información sobre ello. En este
caso, se mostrará el objeto

```json
{
  "message": "No data was found for [{provincia}, {mes/total}]"
}
```

# API REST desarrollada