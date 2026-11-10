# TP 1 — Application Flask et Docker Compose

## Objectif

Ce dossier contient une application web minimale (vraiment minimale) Flask exécutée dans un conteneur Docker et un serveur MongoDB. Docker Compose orchestre les deux services.

La page d’accueil (la seule page existante) effectue une vérification de santé de MongoDB en exécutant la commande `ping` sur le serveur :

- si MongoDB répond, la page affiche `Database status: Healthy` et renvoie le code HTTP `200` ;
- si MongoDB ne répond pas, elle affiche `Database status: Unhealthy`, consigne l’erreur dans les journaux de Flask et renvoie le code HTTP `503`.

Cette vérification confirme que le serveur MongoDB est joignable ; elle ne teste pas une opération de lecture ou d’écriture dans la base.

## Contenu du dossier

- `app.py` : application Flask et vérification de santé MongoDB ;
- `Dockerfile` : image Python et démarrage de l’application ;
- `requirements.txt` : dépendances Python (`Flask` et `Flask-PyMongo`) ;
- `docker-compose.yml` : services `web` et `mongo`, ainsi que leurs ports.

## Démarrer l’application

Depuis le dossier `tp-docker` :

```powershell
docker compose up --build -d
```

L’option `--build` reconstruit l’image web à partir des fichiers du projet, notamment après une modification de `app.py`. L’application est ensuite accessible à l’adresse <http://localhost:8080/>.

MongoDB est accessible depuis l’hôte sur le port `27017`. Dans le réseau Compose, Flask s’y connecte avec le nom de service `mongo` et utilise la base `tp-docker`.

## Vérifier le résultat

Ouvrir <http://localhost:8080/> dans un navigateur. La réponse attendue lorsque MongoDB est disponible est :

```text
Hello, World!
Database status: Healthy
```