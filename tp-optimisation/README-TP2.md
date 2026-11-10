# TP Optimisation Docker

## Objectif

### État initial (Mauvaises pratiques repérées)

- Le `dockerfile` n'a pas le bon nom de fichier (dockerfile au lieu de Dockerfile)
- Le contenu dans `package.json` est écrit en une seule ligne (doit être formatté correctement avec des sauts à la ligne et les indentations pertinentes)
- Le `dockerfile` copie les fichiers de `node_modules` (mauvaise pratique) mais en plus il fait `npm install` (il faut enlever la ligne `COPY node_modules ./node_modules`)
- La ligne `CMD ["node", "server.js"]` est incohérente avec les autres lignes comme `RUN npm run build` puisque la ligne de commande `node server.js` est déjà déclarée comme script dans `package.json` (il faudrait écrire plutôt `RUN npm run start`)
- Le contenu de `server.js` n'est pas correctement (pas du tout) indenté
- Le contenu du `dockerfile` est écrit sans laisser de l'espace entre lignes, c'est recommendable de diviser le fichier par "sections" afin d'améliorer la lisibilité et si possible mettre les mêmes types de commande ensemble

### Étapes d'optimisation

1. Renommer `dockerfile` en `Dockerfile` et formater le contenu des fichiers pour améliorer leur lisibilité. Cette étape ne vise pas à réduire sensiblement la taille de l'image.
2. À réaliser : retirer la copie de `node_modules`, installer les dépendances à partir du lockfile et corriger la commande de démarrage dans `Dockerfile`.

### Suivi des optimisations et des performances

Noter le temps et la taille après chaque étape, dans les mêmes conditions de build.

| Étape | Changement réalisé | Temps de build | Taille disque de l'image | Taille du contenu | Observations |
|---|---|---:|---:|---:|---|
| 0 — Référence | État initial | 23,0 s | 1,88 GB | 474 MB | Image de base déjà présente. |
| 1 | Renommage en `Dockerfile` et mise en forme | 24,3 s | 1,88 GB | 474 MB | Build relancé ; `WORKDIR` apparaît encore comme `CACHED`. |

Tailles mesurées avec `docker images`. Pour un build sans cache : `docker build --pull --no-cache -f Dockerfile -t tp-optimisation:latest .`.