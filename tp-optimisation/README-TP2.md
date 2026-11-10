# TP Optimisation Docker

## Objectif

### Mauvaises pratiques identifiées

- `FROM node:latest` ne fixe pas la version de Node, ce qui rend les builds moins reproductibles.
- Copier `node_modules` depuis l'hôte puis lancer `npm install` peut produire des dépendances incohérentes. Le projet fournit un lockfile : utiliser `npm ci`.
- `COPY . /app` avant l'installation des dépendances empêche de bien réutiliser le cache lorsque le code change. Copier d'abord `package*.json`.
- Aucun `.dockerignore` ne limite le contexte de build ; des fichiers inutiles, notamment `node_modules`, peuvent être envoyés à Docker.
- L'installation de paquets système alourdit l'image et les caches APT ne sont pas nettoyés.
- `NODE_ENV=development` n'est pas adapté à une image de production.
- L'application s'exécute en `root`, ce qui augmente les risques en cas de compromission.
- `EXPOSE 4000 5000` est inutile : le serveur écoute sur le port 3000. `EXPOSE` ne publie pas les ports.
- Le script `build` de `package.json` ne fait qu'afficher un message.
- Le paquet `mongodb` n'est pas utilisé par `server.js`.
- La route `/big` lit le fichier de façon synchrone et bloque le serveur pendant la lecture.

`CMD ["node", "server.js"]` est valide et n'est pas une mauvaise pratique en soi.

### Étapes d'optimisation

1. **Terminée :** renommer `dockerfile` en `Dockerfile` et formater les fichiers. Aucun impact attendu sur le temps de build ni la taille de l'image.
2. **Terminée :** ajouter `.dockerignore`, copier les manifestes avant le code et installer avec `npm ci`.
3. Optimiser l'image : fixer la version de Node, retirer les paquets inutiles et le `npm run build` factice, installer seulement les dépendances de production et lancer en utilisateur non privilégié.
4. Optimiser le projet : retirer `mongodb` inutilisé, remplacer la lecture synchrone de `/big` par une lecture asynchrone et corriger le script `dev` pour Windows.

### Suivi des optimisations et des performances

Noter le temps et la taille après chaque étape, dans les mêmes conditions de build.

| Étape | Changement réalisé | Temps de build | Taille disque de l'image | Taille du contenu | Observations |
|---|---|---:|---:|---:|---|
| 0 — Référence | État initial | 23,0 s | 1,88 GB | 474 MB | Image de base déjà présente. |
| 1 | Renommage en `Dockerfile` et mise en forme | 24,3 s | 1,88 GB | 474 MB | Build relancé ; `WORKDIR` apparaît encore comme `CACHED`. |
| 2 | `.dockerignore`, copie des manifestes puis `npm ci` | 23,9 s | 1,89 GB | 476 MB | Contexte réduit à 196 B ; image de base déjà présente. |

Tailles mesurées avec `docker images`. Pour un build sans cache : `docker build --pull --no-cache -f Dockerfile -t tp-optimisation:latest .`.