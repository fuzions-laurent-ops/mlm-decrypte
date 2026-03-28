# 🚀 Guide de déploiement — MLM Décrypté

## Système de publication automatisé

Le blog fonctionne avec un **calendrier éditorial automatique**.
Les articles non encore publiés sont invisibles pour Google (balise `noindex`).
Chaque semaine, le script `publish.py` rend les bons articles visibles.

---

## 📅 Calendrier de publication

- **1er avril 2026** — Lancement avec 8 articles piliers
- **Mardi + Vendredi** — 2 nouveaux articles chaque semaine
- **28 juillet 2026** — Dernier article publié (stock épuisé → écrire de nouveaux articles)

Pour voir l'état complet du calendrier à tout moment :
```
python3 publish.py --status
```

---

## 🔧 Comment publier (méthode simple — 5 min/semaine)

### Étape 1 — Exécuter le script de publication
Ouvre un terminal dans le dossier MLM et tape :
```
python3 publish.py
```
Le script retire automatiquement le `noindex` des articles dont la date est atteinte.

### Étape 2 — Re-déployer sur Netlify
Va sur **app.netlify.com** → ton site → "Deploys" → glisse-dépose le dossier MLM complet.
En 30 secondes le site est à jour.

**C'est tout.** À faire chaque mardi et vendredi.

---

## ⚡ Méthode avancée — Automatisation complète (GitHub + Netlify)

Avec cette méthode, la publication est **100% automatique** sans aucune action manuelle.

### Configuration (une seule fois — 30 min)

**1. Créer un compte GitHub** (gratuit) sur github.com

**2. Créer un nouveau repository** nommé `mlm-decrypte`

**3. Pousser le dossier MLM sur GitHub** :
```bash
cd /chemin/vers/MLM
git init
git add .
git commit -m "Initial deploy — MLM Décrypté"
git remote add origin https://github.com/TON_USERNAME/mlm-decrypte.git
git push -u origin main
```

**4. Connecter Netlify à GitHub** :
- app.netlify.com → "Add new site" → "Import an existing project"
- Choisir GitHub → sélectionner `mlm-decrypte`
- Publish directory : laisser vide (racine)
- Deploy

**5. Créer un token Netlify** :
- app.netlify.com → User settings → Applications → New access token
- Copier le token

**6. Ajouter le token dans GitHub** :
- Ton repo → Settings → Secrets and variables → Actions → New secret
- Nom : `NETLIFY_AUTH_TOKEN`
- Valeur : le token copié
- Faire pareil pour `NETLIFY_SITE_ID` (trouvé dans Netlify → Site settings → General)

**7. Créer le fichier GitHub Actions** (déjà créé dans `.github/workflows/publish.yml`)

Ensuite : chaque mardi et vendredi à 8h00, GitHub publie automatiquement les bons articles et Netlify redéploie sans que tu aies quoi que ce soit à faire.

---

## 📊 Suivi des performances

Une fois le site en ligne, installe Google Search Console :
- search.google.com/search-console
- Ajouter ton site → vérification via fichier HTML
- Suivre l'indexation article par article

Objectif à 3 mois : les 8 articles piliers indexés et positionnés sur leurs mots-clés cibles.

