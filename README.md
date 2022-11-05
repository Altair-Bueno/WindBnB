# WindBnB

Proyecto para la asignatura Ingeniería Web para el curso 2022-2023. Universidad
de Málaga, Grado en Ingeniería del Software

## Miembros del grupo

- Alvaro Tapia Muñoz
- Jose Luis Bueno Pachón
- Carlos Marín Corbera
- Carmen González Ortega
- Altair Bueno Calvente

## Despliegue del servicio

### Mediante Docker compose

En caso de disponer de la herramienta [Docker Compose V2](https://docs.docker.com/compose/compose-v2/), es posible realizar el despliegue siguiendo las siguientes instrucciones

```sh
# Acceder a la carpeta ROOT del proyecto
cd /WindBnB
# Iniciar el servicio
docker compose up -d
# Detener el servicio
docker compose down
```

En otro caso, si tenemos la herramienta `docker-compose` convencional

```sh
# Acceder a la carpeta ROOT del proyecto
cd /WindBnB
# Iniciar el servicio
docker-compose up -d
# Detener el servicio
docker-compose down
```

- El servidor de mongo está disponible en <mongodb://root:example@localhost:27017>
- El microservicio A2reservasREST está disponible en <http://localhost:8001>
- El microservicio A2viviendasREST está disponible en <http://localhost:8002>
- El microservicio A2datosabiertosREST está disponible en <http://localhost:8003>
