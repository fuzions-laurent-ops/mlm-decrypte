# MLM Décrypté — Spécification API Chatbot

## Vue d'ensemble

Le widget frontend (`chatbot-widget.js`) est déjà intégré sur toutes les pages du site.
Il envoie les questions des visiteurs vers un endpoint backend et affiche la réponse + les liens vers les articles pertinents.

**Ton rôle** : créer le backend qui reçoit la question, interroge un LLM open source, et renvoie la réponse au bon format.

---

## Endpoint attendu

```
POST /api/chat
Content-Type: application/json
```

### Requête (envoyée par le widget)

```json
{
  "message": "Le MLM c'est une arnaque ?"
}
```

### Réponse attendue

```json
{
  "reply": "C'est une question fréquente ! Le MLM n'est pas une arnaque en soi, mais certaines entreprises utilisent des pratiques douteuses. Voici des articles qui t'aideront à y voir plus clair :",
  "articles": [
    {
      "title": "MLM arnaque ou opportunité ?",
      "url": "/articles/mlm-arnaque-ou-opportunite.html"
    },
    {
      "title": "Différence entre MLM et pyramide de Ponzi",
      "url": "/articles/mlm-vs-pyramide-de-ponzi.html"
    }
  ]
}
```

### Champs

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `reply` | string | ✅ | La réponse textuelle du bot |
| `articles` | array | ❌ | Liste d'articles suggérés (0 à 3 max recommandé) |
| `articles[].title` | string | ✅ (si articles) | Titre affiché de l'article |
| `articles[].url` | string | ✅ (si articles) | Chemin relatif vers l'article |

---

## Configuration côté widget

Dans `chatbot-widget.js`, modifier la constante en haut du fichier :

```javascript
const CHATBOT_API_URL = '/api/chat';  // ← Remplacer par l'URL réelle de ton API
```

Par exemple :
- En local : `http://localhost:8000/api/chat`
- En production : `https://api.mlm-decrypte.fr/api/chat` ou via un proxy Netlify

---

## Architecture recommandée

```
Visiteur → Widget (JS frontend)
              ↓ POST /api/chat
         Backend (Python/Node)
              ↓
         LLM Open Source (Mistral, Llama, etc.)
              +
         Index des articles (embeddings ou simple recherche)
              ↓
         Réponse JSON → Widget affiche le message + liens
```

### Stack suggérée

- **Backend** : FastAPI (Python) ou Express (Node.js)
- **LLM** : Mistral 7B, Llama 3, ou Phi-3 via Ollama
- **Index articles** : Embeddings avec FAISS/ChromaDB, ou recherche simple par mots-clés
- **Hébergement** : Railway, Render, ou VPS avec Ollama

---

## Liste des articles disponibles

Le bot doit connaître les articles pour pouvoir les recommander.
Voici la liste complète (à intégrer dans ton index) :

### Catégorie : Démystifier
- `/articles/mlm-arnaque-ou-opportunite.html` — MLM arnaque ou opportunité ?
- `/articles/mlm-vs-pyramide-de-ponzi.html` — MLM vs Pyramide de Ponzi
- `/articles/mlm-france-legal.html` — Le MLM est-il légal en France ?
- `/articles/mlm-et-secte.html` — MLM et secte : où est la limite ?
- `/articles/mlm-manipulation.html` — MLM et manipulation
- `/articles/mlm-mauvaise-reputation.html` — Pourquoi le MLM a mauvaise réputation
- `/articles/signaux-alarme-mlm-douteux.html` — Signaux d'alarme d'un MLM douteux
- `/articles/produits-mlm-trop-chers.html` — Les produits MLM sont-ils trop chers ?

### Catégorie : Le Modèle
- `/articles/comment-fonctionne-mlm.html` — Comment fonctionne le MLM
- `/articles/plan-de-compensation-mlm.html` — Plan de compensation MLM
- `/articles/comprendre-distributeur-mlm.html` — Comprendre le rôle du distributeur
- `/articles/difference-vente-directe-mlm.html` — Différence vente directe et MLM
- `/articles/plus-grandes-entreprises-mlm.html` — Les plus grandes entreprises MLM
- `/articles/mlm-recrutement-ou-vente.html` — MLM : recrutement ou vente ?
- `/articles/avenir-mlm.html` — L'avenir du MLM

### Catégorie : La Réalité
- `/articles/vivre-du-mlm-statistiques.html` — Peut-on vivre du MLM ? Statistiques
- `/articles/erreurs-debutant-mlm.html` — Les erreurs du débutant en MLM
- `/articles/pourquoi-echouer-mlm.html` — Pourquoi on échoue en MLM
- `/articles/mlm-impots-france.html` — MLM et impôts en France
- `/articles/mlm-fonctionnaire-cumul-activite.html` — MLM et fonctionnaire
- `/articles/quitter-emploi-pour-mlm.html` — Quitter son emploi pour le MLM
- `/articles/competences-developpees-mlm.html` — Compétences développées en MLM
- `/articles/mlm-developpement-personnel.html` — MLM et développement personnel
- `/articles/regard-famille-amis-mlm.html` — Le regard de la famille et des amis

### Catégorie : Témoignages
- `/articles/perdre-argent-mlm-temoignage.html` — Témoignage : perdre de l'argent en MLM
- `/articles/temoignage-mlm-argent.html` — Témoignage MLM et argent
- `/articles/portrait-mere-famille-mlm.html` — Portrait d'une mère de famille en MLM
- `/articles/quitter-le-mlm.html` — Quitter le MLM

### Catégorie : Mon Regard
- `/articles/pourquoi-blog-mlm-decrypte.html` — Pourquoi ce blog
- `/articles/terrain-manifeste.html` — Mon manifeste
- `/articles/terrain-philosophie-mlm-france.html` — Ma philosophie du MLM en France

### Catégorie : Sur le Terrain
- `/articles/terrain-premiers-jours-mwr.html` — Mes premiers jours chez MWR
- `/articles/terrain-pourquoi-mwr-life.html` — Pourquoi j'ai choisi MWR Life
- `/articles/terrain-premier-echec.html` — Mon premier échec
- `/articles/terrain-entourage.html` — L'entourage et le MLM
- `/articles/terrain-erreurs.html` — Mes erreurs sur le terrain
- `/articles/terrain-lecons-echec.html` — Leçons de mes échecs
- `/articles/terrain-methode-invitation.html` — Ma méthode d'invitation
- `/articles/terrain-deux-mlm.html` — Deux MLM en même temps ?
- `/articles/terrain-70-collaborateurs.html` — 70 collaborateurs : bilan
- `/articles/terrain-bilan-4-mois.html` — Bilan après 4 mois

---

## CORS

Si le backend est sur un domaine différent, penser à activer CORS :

```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mlm-decrypte.fr", "http://localhost:8080"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

---

## Test rapide (mock)

Pour tester le widget sans backend, tu peux temporairement remplacer la fonction `callAPI` dans `chatbot-widget.js` :

```javascript
function callAPI(message) {
  return new Promise(function(resolve) {
    setTimeout(function() {
      resolve({
        reply: "Bonne question ! Voici un article qui pourrait t'intéresser :",
        articles: [
          { title: "Comment fonctionne le MLM", url: "/articles/comment-fonctionne-mlm.html" }
        ]
      });
    }, 1000);
  });
}
```

---

## Proxy Netlify (optionnel)

Si tu héberges sur Netlify, tu peux rediriger `/api/chat` vers ton backend via `netlify.toml` :

```toml
[[redirects]]
  from = "/api/chat"
  to = "https://ton-backend.railway.app/api/chat"
  status = 200
  force = true
```

Comme ça, pas de problème CORS et l'URL `/api/chat` fonctionne directement.
