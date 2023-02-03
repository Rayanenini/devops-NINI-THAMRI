# TP 1 - DevOps

## Base images

* docker pull httpd 
* docker pull openjdk
* docker pull postgre

## Database

1-1 Document your database container essentials: commands and Dockerfile.
-> création des deux containers :
* docker run -p 5432:5432 -d --network app-network --name postgresql-tp1 fayc69/postgresql-tp1 
* docker run -d -p 8090:8080 --net=app-network --name adminer-tp1 adminer

-> dans le même réseau donc dans localhost:8090 on mentionne "postgresql-tp1" dans le serveur (résolution nom automatique)

## Spring 
docker build -t fayc69/sprint-tp1 .
docker run --name spring-tp1 fayc69/spring-tp1

## HTTP



TP3 : ERREURS 
networks:
    - name : (oublie du name)
dans backend restart : always pas bon
 