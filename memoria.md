---
title: "Práctica de servicios Web (II): cliente"
author:
  - "Álvaro Jesús Tapia Muñoz"
  - "Jose Luis Bueno Pachón"
  - "Carlos Marín Corbera"
  - "Carmen González Ortega"
  - "Altair Bueno Calvente"
date: 28 nov 2022
titlepage: true
titlepage-rule-color: "4506B3"
toc-own-page: true
toc: true
---

# Introducción

Para la realización del cliente REST propuesto en el documento 
_Práctica de servicios Web (II): cliente_, se ha optado por usar un cliente de
tipo [Server-Side Rendering con Astro](https://docs.astro.build/en/guides/server-side-rendering/).

# Replanteamiento de decisiones anteriores

<!--TODO: - cualquier replanteamiento de decisiones anteriores (de tecnologías a utilizar u otros) o cambios en el diseño de la base de datos o la implementación de los servidores web.-->

# Requisitos considerados

Se han considerado los siguientes requisitos para la realización del cliente REST: 

- **Uso de los microservicios de acceso CRUD**
- **Uso de las consultas y búsquedas a la base de datos**
- **Uso de los datos abiertos desplegados como servicios REST en la práctica anterior**
- **Visualización de mapas con información relevante**: [Leaflet](https://leafletjs.com/) y OpenStreetMaps
- **Visualización de imágenes almacenadas en algún servicio cloud**: [Cloudinary](https://cloudinary.com/)

# Tecnologías Utilizadas

Para la interfaz del ciente se ha usado los frameworks 
[Astro](https://astro.build/) junto a [Svelte](https://svelte.dev/) para 
la generación de las páginas y componentes usando Typescript. Para los mapas
se ha usado la librería [Leaflet](https://leafletjs.com/) que hace a su vez uso
de OpenStreetMaps.

Para la persistencia de datos se ha optado por la base de datos de
[MongoDB](https://www.mongodb.com/), conectada a través del driver asíncrono
[Motor](https://motor.readthedocs.io/en/stable/index.html), al igual que con 
el servidor REST, y para el servicio cloud de almacenaje de imágenes 
[Cloudinary](https://cloudinary.com/).

# Instrucciones de Despliegue

Se facilita el fichero `docker-compose.yml` para poder hacer un despliegue de
todos los microservicios utilizando la herramienta
[Docker Compose](https://docs.docker.com/compose/compose-v2/). Instrucciones más
detalladas están disponibles en el fichero `README.md`

Para facilitar el despliegue de cada aplicación de forma individual, se
proporciona un fichero `Dockerfile` para construir un contenedor de
[Docker](https://docker.com). Las instrucciones detalladas sobre como utilizar
la imagen y las opciones de configuración disponibles se pueden encontrar en el
fichero `README.md`, dentro del directorio correspondiente a cada microservicio.

En caso de no disponer de las herramientas mencionadas, dentro del mismo fichero
`README.md` en cada microservicio, se indica paso a paso cómo realizar un
despliegue con [uvicorn](https://www.uvicorn.org).

## Datos de prueba para Mongo

En el interior de la carpeta `iweb`, se proporciona un fichero `houses.json` con
el volcado de la colección de pruebas. Para restaurarla, basta con realizar una
inserción de multiples elementos del contenido del fichero. Para automatizar el
proceso, se proporciona un script de Python `iweb.py`. Requiere que la librería
`pymongo` esté instalada

# Funcionalidad de la aplicación cliente

## Página principal `/houses`

- Lista de viviendas que están en la base de datos. Pulsando sobre un título se 
accede a la página de la vivienda. Muestra varios datos de cada vivienda, 
almacenados en la base de datos.
- Visualización de una barra de navegación con las opciones de:
  - `Home` y `WindBnB`: Redirige a la Página principal
  - `Bookings`: Accede a la Páginas de reservas del usuario
  - `New House`: Una vez iniciada sesión, aparece esta opción que redirige a la
    página para crear una nueva vivienda.
  - `Login/Logout`: Redirige a una página de inicio de sesión si no se ha
    iniciado sesión aún, o directamente sale de la sesión si se estaba en una
- Buscador de viviendas mediante un filtro que busca por título de la vivienda. 

## Página de inicio de sesión `/auth/login`

La página de inicio de sesión tiene la única funcionalidad de que un usuario
entre a su sesión con su nombre de usuario. La contraseña no es requerida. 
Con el botón `Log in` se redirige a la Página principal con la
sesión ya iniciada.

## Página de una vivienda `/houses/{vivienda_id}`

La página de una vivienda tiene distintas funciones:

- Botón `Modificar vivienda`: Redirige a una página para completar la acción de 
  editar. 
  Sólo disponible si el usuario es el dueño.
- Botón `Eliminar vivienda`: Realiza la acción de borrar la vivienda de la base 
  de datos y redirige a la página principal. Sólo disponible si el usuario es 
  el dueño.
- Visualización de **datos** de la vivienda.
- Visualización de **imágenes** de la vivienda.
- Formulario para reservar la vivienda: Muestra dos campos de fecha de 
  calendario para indicar el rango de días que quiere reservar el usuario y
  un botón `Reservar` para realizar la acción y añadir la reserva a la base de
  datos.
- Visualización de un **mapa**: Muestra la localización de la vivienda a 
  partir de la latitud y longitud almacenados en la base de datos, y las 
  gasolineras cercanas en un área de 5km llamando a la api encargada de los
  datos abiertos en el backend
  (`/gas-stations?area={area}&limit={limit}&latitude={latitude}&longitude={longitude}`). 
  Se hace uso de la librería Leaflet y se muestra con OpenStreetMaps.
- Visualización de la **estancia media**: Muestra la estancia media de los
  viajeros en esa provincia a partir de la provincia de la vivienda llamando
  a la api encargada de los datos abiertos en el backend
  (`/average-stay?provincia={provincia}`).

## Página de reservas `/bookings`

La página de reservas muestra una lista de reservas realizadas por el usuario
que está con la sesión iniciada en ese momento. De cada reserva se muestra la
vivienda, a la que se puede acceder a su página pulsando sobre ella, la fecha de
inicio y fin de la reserva, el estado y el botón `Cancel booking` cancela la 
reserva, eliminándola de la base de datos. 

Las reservas se encuentran paginadas de 10 en 10, contando con los botones 
`Previous` y `Next` para navegar entre la lista de reservas del usuario.

También cuenta con opciones de filtro y ordenación de las reservas:

- Filtro por fecha de inicio
- Filtro por fecha de fin
- Filtro por estado
- Ordenar por fecha de inicio o fin
- Orden ascendente o descendente

## Página de creación de una vivienda `/houses/new`

La página muestra un formulario con los datos correspondientes a una vivienda
para crear una nueva vivienda y almacenarla en la base de datos:

- Título
- Descripción
- Calle
- Número
- Ciudad
- Provincia
- Código postal
- País
- Precio por noche
- Imágenes: Mediante un botón `Elegir archivos` se accede al explorador de 
  archivos donde se puede realizar una selección múltiple de imágenes. Es
  obligatorio seleccionar al menos 1 imagen.

Mediante el botón `Crear` se añade a la base de datos con los datos rellenados
en el formulario y se redirige a la página de esa vivienda. Las fotos 
seleccionadas se almacenan en Cloudinary.

## Página de modificación de una vivienda `/houses/edit/{vivienda_id}`

La página muestra un formulario con los datos correspondientes a una vivienda
para modificar una vivienda ya existente en la base de datos, con los campos
ya autocompletados:

- Título
- Descripción
- Calle
- Número
- Ciudad
- Provincia
- Código postal
- País
- Precio por noche
- Imágenes

Mediante el botón `Modificar datos` se actualiza la vivienda de la base de datos
si se ha cambiado algún campo y redirige a la página de la vivienda. Si se han
modificado imágenes, de la misma manera se actualiza en Cloudinary.
