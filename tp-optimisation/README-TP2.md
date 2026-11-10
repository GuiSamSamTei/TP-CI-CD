# TP Optimisation Docker

## Objectif

### Mauvaises pratiques identifiées

- **Corrigés à l'étape 3 :** image Node épinglée, dépendances de production uniquement, exécution sans privilèges root et suppression des paquets système et du faux script de build.
- **Corrigés à l'étape 4 :** dépendances inutilisées retirées, lecture de `/big` asynchrone et script de développement compatible Windows.

### Étapes d'optimisation

1. **Terminée :** renommer `dockerfile` en `Dockerfile` et formater les fichiers. Aucun impact attendu sur le temps de build ni la taille de l'image.
2. **Terminée :** ajouter `.dockerignore`, copier les manifestes avant le code et installer avec `npm ci`.
3. **Terminée :** alléger et sécuriser l'image ; installer seulement les dépendances de production.
4. **Terminée :** retirer `mongodb`, rendre `/big` asynchrone et utiliser `nodemon` pour le développement sous Windows.

### Suivi des optimisations et des performances

Noter le temps et la taille après chaque étape, dans les mêmes conditions de build.

| Étape | Changement réalisé | Temps de build | Taille disque de l'image | Taille du contenu | Observations |
|---|---|---:|---:|---:|---|
| 0 — Référence | État initial | 23,0 s | 1,88 GB | 474 MB | Image de base déjà présente. |
| 1 | Renommage en `Dockerfile` et mise en forme | 24,3 s | 1,88 GB | 474 MB | Build relancé ; `WORKDIR` apparaît encore comme `CACHED`. |
| 2 | `.dockerignore`, copie des manifestes puis `npm ci` | 23,9 s | 1,89 GB | 476 MB | Contexte réduit à 196 B ; image de base déjà présente. |
| 3 | Image Node slim, dépendances de production et utilisateur `node` | 7,6 s | 357 MB | 86,4 MB | `WORKDIR` apparaît comme `CACHED`. |
| 4 | Dépendances nettoyées et lecture asynchrone | 9,4 s | 343 MB | 83,2 MB | `WORKDIR` apparaît comme `CACHED`. |

Tailles mesurées avec `docker images`. Pour un build sans cache : `docker build --pull --no-cache -f Dockerfile -t tp-optimisation:latest .`.


### Temps de réponse HTTP

Référence avant l'étape 4 : une requête par scénario avec un fichier temporaire de 1 Mio. Les requêtes simultanées sont lancées ensemble ; résultats en millisecondes.

| État | Requête | Temps |
|---|---|---:|
| Avant étape 4 | `/` | 6,25 ms |
| Avant étape 4 | `/big` | 19,19 ms |
| Avant étape 4 | `/` en même temps qu'une requête `/big` | 13,97 ms |
| Après étape 4 | `/` | 10,41 ms |
| Après étape 4 | `/big` | 34,30 ms |
| Après étape 4 | `/` en même temps qu'une requête `/big` | 3,96 ms |

Une seule mesure par scénario : les écarts, surtout sur `/big`, peuvent varier d'un essai à l'autre.