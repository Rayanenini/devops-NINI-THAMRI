# Compte-rendu de TP

Auteurs : NINI Rayane, THAMRI Fayçal.

## Partie 1 - Discover Devops

### Questions
1-1 Document your database container essentials: commands and Dockerfile.
> Voici le code commenté de la base de données :
```
FROM postgres:14.1-alpine #on recupère une BD Postgresql 
COPY ./scripts/ /docker-entrypoint-initdb.d/ #on copie les scripts SQL (dans l'ordre alphabétique) dans le dossier docker-entrypoint-initdb.d/ pour qu'ils s'exécutent lors de la création de la BD
#variable d'environnement 
ENV POSTGRES_DB=db \
   POSTGRES_USER=usr \
   POSTGRES_PASSWORD=pwd
```
1-2 Why do we need a multistage build? And explain each step of this dockerfile.
> Le **build multistage** permet de créer des images Docker plus petites et plus sûres en séparant le processus de construction en plusieurs étapes avec des images intermédiaires minimales : dans notre cas, on va avoir un "Build" puis un "Run". 

Le [Dockerfile](spring2/Dockerfile) permet de créer un image Docker pour une application Java construite avec Maven : 
1. La  première étape est "Build"
2. La seconde étape est "Run" puis on copie le fichier jar de l'étape de construction (target/*.jar) dans le répertoire de travail sous le nom "myapp.jar". 
3. À la fin, l'image est exécutée via la commande "ENTRYPOINT java -jar myapp.jar". Cela signifie que lorsque l'image Docker est lancée, elle exécutera cette commande.

1-3 Document docker-compose most important commands. 
> Le fichier **docker-compose.yml** simplifie la configuration et le déploiement d'applications multi-conteneurs en définissant les conteneurs, les réseaux, les volumes et les paramètres dans un seul fichier. Docker Compose est un outil permettant de définir et d'exécuter des applications Docker multi-conteneurs. Il est alors possible d'utiliser un fichier YAML pour configurer différents services à l'aide d'une seule commande. On dénombre de nombreuses commandes importantes mais on peut citer les suivantes comme les plus utilisées au cours de ce projet :
```
docker-compose up #à faire dans le dossier du dockercompose.yml
docker-compose down #arrête et supprime les containers
docker-compose ps #affiche les containers en cours  
```

1-4 Document your docker-compose file.
> L'objectif est donc de créer trois containers dans un même réseau Voici le code commenté :
```
version: '3.7'
services: #définitions des trois services 
    database: #le service de base de données
        build: ./postgresql #dans le dossier postgresql du projet
        ports:
          - 5432:5432 
        environment: #les variables d'environnements de la base de données
          POSTGRES_DB: db
          POSTGRES_USER: usr
          POSTGRES_PASSWORD: pwd
        volumes: #pour la persistance des données
          - postgrevol:/var/lib/postgresql/data
        networks: #définiton du réseau
          - app-network 
        
    backend: 
        build: ./spring2 #dans le dossier spring2 du dossier
        restart: always
        networks:
          - app-network
        ports:
          - 8080:8080
        depends_on: #il est nécessaire de créer la database avant le backend puisqu'il en a besoin pour fonctionner
          - database

    httpd:
        build: ./http
        ports:
          - 8081:80 
        networks:
          - app-network
        depends_on:
          - backend

volumes:
  postgrevol:
networks: #définition du réseau
    app-network:
```
> On peut suggérer un renforcement de sécurité en créant un réseau entre la base de données et le backend ainsi qu'un second réseau entre le backend et le front.

1-5 Document your publication commands and published images in dockerhub.
> Il est possible de tagger l'image avec la commande :
```
docker tag tp-devops-db-pg faycalth/devops-tp1-database:1.0
```
Ensuite on la push à l'aide de la commande suivante :
```
docker push faycalth/devops-tp1-database:1.0
```

![TP1-1!](/images/tp1-dockerpush.png "dockerpush")

### À retenir :

> Après avoir rédiger le Dockerfile, on build puis on run :
```
docker build . 
``` 
> il est possible d'utiliser le paramètre "-t" pour "tagger".
``` 
docker run nom_reel_image
```
> docker run peut prendre plusieurs arguments intéressants :
1. -p pour spécifier les ports
2. --name nom_image_attribué_au_run
3. -d pour détacher la console
4. --network pour spécifier le reseau 
5. -v pour volume de données

## Partie 2 - Github Action session

### Questions
2-1 What are testcontainers ?
> Testcontainers est une bibliothèque Java qui facilite les tests pour les applications utilisant des conteneurs Docker.

2-2 Document your Github Actions configurations.

1. Avant toute chose, il faut ajouter les variables d'environnement dans Github Action (Settings->Security->Secrets) : notamment pour docker (username et token) et pour SonarCloud.
2. Ensuite, il faut lui apporter des modifications dans le fichier .github/workflows/main.yml.
    1. On va notamment spécifier après quel évènement :
        ```
        on:
            #to begin you want to launch this job in main and develop
            push:
                branches: master 
            pull_request:
        ``` 
        Dans notre cas, c'est après un push sur la branch master
    2. On indique ensuite les jobs et leurs steps. On utilise dans les steps :
        1. **name** : pour le nom
        2. **uses** : l'action à réaliser 
        3. **with** : complète le **uses** 

Ainsi, on obtient les résultats suivants après un push sur la branche master :
- Github Actions :

![TP2-2!](/images/tp2-ci.png "ci")

- Job 1 :

![TP2-1!](/images/tp2-test-backend.png "test-backend")

- Job 2 :

![TP2-4!](/images/tp2-build.png "build")

2-3 Document your quality gate configuration.

SonarCloud permet de vérifier la qualité du code. Les résultats dépendent fortement de la stratégie appliquée (plus ou moins stricte).  

- Résultat SONARCLOUD :
![TP2-3!](/images/tp2-qualitypass.png "qualitypass")

## Partie 3 - Ansible session

### Questions

3-1 Document your inventory and base commands
> Il faut tout d'abord créer le fichier "[setup.yml](ansible/inventories/setup.yml)" dans le dossier inventories. On ajoute notamment les informations concernant l'host et la clé privée pour se connecter.  

3-2 Document your playbook
> Voici le code dans le [playbook](ansible/playbook.yml) :
```
- hosts: all
  gather_facts: false
  become: yes
  roles: 
    - docker
    - create-network
    - launch-database
    - launch-app
    - launch-proxy
```
Les rôles vont être appelés et s'exécutés dans l'ordre. On retrouve les configurations dans le fichier roles/nom_du_role/tasks/main.yml.  

3-3 Document your docker_container tasks configuration.
> On utilise le module *docker_container* dans Ansible qui permet de gérer et automatiser la gestion des containers docker dans une infrastructure. Prenons l'exemple de la tâche qui va s'occuper d'executer le backend (role : [launch-app](ansible/roles/launch-app/tasks/main.yml))
```
- name: Run Backend #nom de la tâche
  docker_container: 
    name: backend 
    image: faycalth/tp-devops:spring #image à pull
    ports: #ports à attribuer
      - 8080:8080
    networks: #
      - name: app-network
```

### Résultats
- Appel de l'API réussi :

![TP3-1!](/images/tp3-api.png "api")

- Docker Hub:

![TP3-2!](/images/tp3-dockerhub.png "dockerhub")