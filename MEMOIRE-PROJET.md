# MLM Décrypté — Mémoire du projet (mise à jour : 25 mars 2026)

---

## 1. QUI EST LAURENT CONSTANTIN

- Ancien joueur professionnel de badminton, **équipe de France**
- Entraîneur, formateur de coachs, créateur de **Fuzions Badminton**
  (stages, contenu internet, formations coachs)
- Auteur : 1 livre "60 situations ludiques" + 2 guides PDF badminton
- Salarié ET entrepreneur en simultané
- MLM = activité complémentaire sérieuse (pas une reconversion)

### Parcours MLM
- **ACN** → échec (manque accompagnement sponsor + produits pas alignés + peu engagé)
- **Kyani** → échec (mêmes raisons + malaise à "vendre à ses amis")
- "Jamais plus" → puis retour par conviction
- **MWRlife** (MLM de services) → introduit par sa **belle-sœur**
  Depuis quelques mois, a construit une équipe
- Valeurs clés : bienveillance, transparence, aventure humaine avant business

### Philosophie MLM de Laurent
- Ce n'est pas le modèle, c'est ce qu'on en fait
- Le développement personnel dans le MLM est réel, pas du conditionnement
- Éducation financière manque = vraie cause des pertes, pas le modèle
- MLM de services = modèle d'avenir (pas de stock, abonnements récurrents)
- Le "1% réussit" s'applique partout : sport, entrepreneuriat, salariat

---

## 2. OBJECTIFS DU PROJET

**Objectif 1 — Blog MLM Décrypté**
- Partager des articles honnêtes et nuancés sur le MLM
- Éduquer les sceptiques, déconstruire les mythes
- Créer du positif autour du MLM sans être un outil de recrutement
- Valoriser indirectement les MLM de services (modèle MWRlife)

**Objectif 2 — Instagram (à démarrer après le blog)**
- Compte à créer from scratch
- Raconter le parcours MLM de Laurent en temps réel
- Victoires, échecs, doutes, zones d'ombre — authenticité totale

---

## 3. ÉTAT DU SITE (dossier /sessions/adoring-friendly-bell/mnt/MLM/)

### Structure technique
- Site HTML statique (meilleur SEO qu'un SPA React)
- CSS variables : --green-dark, --green-mid, --amber, --amber-light, --cream, --grey-light, --grey-mid
- Fonts : Inter + Playfair Display (Google Fonts)
- Hamburger menu avec drawer, overlay, animation 3 lignes → X
- Responsive : 1024px, 768px, 400px
- Serveur local de test : `python3 -m http.server 8080`

### Pages principales
- `index.html` — Homepage complète
- `a-propos.html` — Page À propos avec parcours complet de Laurent + timeline MLM
- `article-template.html` — Template réutilisable
- `plan-editorial.md` — Plan SEO des 28 articles
- `newsletter-automation.md` — Séquences email Brevo

### Rubriques (dossier categories/)
| Fichier | Couleur | Nb articles |
|---------|---------|-------------|
| demystifier.html | Rouge | 8 |
| le-modele.html | Bleu | 7 |
| la-realite.html | Vert | 6 |
| temoignages.html | Ambre | 4 |
| mon-regard.html | Violet | 3 |
| **sur-le-terrain.html** | **Teal** | **10 (à écrire)** |

---

## 4. ARTICLES — ÉTAT D'AVANCEMENT

### ✅ Articles rédigés (contenu complet intégré)

**Démystifier**
- `pourquoi-blog-mlm-decrypte.html` — Pourquoi ce blog
- `mlm-vs-pyramide-de-ponzi.html` — MLM vs pyramide de Ponzi
- `mlm-arnaque-ou-opportunite.html` — Arnaque ou opportunité ?
- `mlm-mauvaise-reputation.html` — Pourquoi le MLM a mauvaise réputation
- `signaux-alarme-mlm-douteux.html` — 7 signaux d'alarme
- `mlm-recrutement-ou-vente.html` — Recrutement ou vente ?
- `produits-mlm-trop-chers.html` — Produits MLM trop chers ?
- `mlm-manipulation.html` — MLM et manipulation
- `mlm-et-secte.html` — MLM et secte

**Le modèle**
- `comment-fonctionne-mlm.html` — Comment fonctionne le MLM
- `plan-de-compensation-mlm.html` — Plan de compensation
- `difference-vente-directe-mlm.html` — Vente directe vs MLM
- `mlm-france-legal.html` — MLM légal en France
- `vivre-du-mlm-statistiques.html` — Statistiques de revenus
- `mlm-impots-france.html` — MLM et impôts

**La réalité**
- `pourquoi-echouer-mlm.html` — Pourquoi les gens échouent
- `regard-famille-amis-mlm.html` — Le regard de l'entourage
- `competences-developpees-mlm.html` — Compétences développées
- `mlm-developpement-personnel.html` — MLM et développement perso
- `erreurs-debutant-mlm.html` — Erreurs du débutant (personnel ACN/Kyani)
- `quitter-le-mlm.html` — Quitter le MLM

**Mon regard**
- `comprendre-distributeur-mlm.html` — Vie d'un distributeur
- `avenir-mlm.html` — L'avenir du MLM

### ⏳ Articles restants à rédiger

**Démystifier**
- `mlm-et-secte.html` ← déjà fait ci-dessus (vérifier)
- `plus-grandes-entreprises-mlm.html` ← attention : ne pas citer de marques négativement

**Témoignages (4 articles)** ← nécessitent histoires réelles ou composites
- `temoignage-mlm-argent.html`
- `portrait-mere-famille-mlm.html`
- `perdre-argent-mlm-temoignage.html`
- `quitter-emploi-pour-mlm.html`

**Sur le terrain (10 articles — NOUVELLE RUBRIQUE)**
1. La posture du distributeur
2. L'art de l'invitation
3. Gérer les 7 objections
4. La duplication
5. Devenir leader d'équipe (lien sport haut niveau de Laurent)
6. Psychologie achat / refus
7. Présence réseaux sociaux
8. Rituels quotidiens
9. Surmonter les phases de doute
10. Faire du MLM avec 1h par jour

---

## 5. RÈGLES ÉDITORIALES

### Ton
- Tutoiement (proximité avec le lecteur)
- Honnête, nuancé, jamais "vendeur"
- Personnel quand Laurent peut parler de son vécu (ACN, Kyani, MWRlife)
- Jamais condescendant envers les sceptiques

### Noms à gérer
- ✅ Citer : Charles Ponzi, Bernie Madoff (personnages historiques)
- ✅ Citer en contexte personnel : ACN, Kyani (expériences propres de Laurent)
- ❌ Ne pas citer négativement : Herbalife, LuLaRoe, toute autre marque MLM active

### Structure article type
- TOC (table des matières avec ancres)
- 4-5 H2
- highlight-box (vert) + alert-box (ambre) pour les points clés
- FAQ accordion (3 questions) avec toggleFaq() JS
- Author box en bas
- Maillage interne vers autres articles du blog

### MLM de services
- Valoriser subtilement les MLM de services (pas de stock, abonnements récurrents)
- Ne pas nommer MWRlife directement dans les articles — laisser le lecteur faire le lien
- Le mentionner peut venir naturellement dans "Mon regard" et "Sur le terrain"

---

## 6. NEWSLETTER (Brevo)

- Fournisseur : Brevo (ex-Sendinblue) — gratuit jusqu'à 300 emails/jour
- 4 séquences documentées dans `newsletter-automation.md`
- Séquence 1 : Bienvenue (J0, J+3, J+7)
- Séquence 2 : Éducation (5 emails sur 20 jours)
- Séquence 3 : Hebdomadaire (chaque lundi 8h)
- Séquence 4 : Réengagement (60 jours inactif)
- API key à intégrer dans les formulaires newsletter du site

---

## 7. PROCHAINES ÉTAPES (dans l'ordre)

1. **Relire les articles avec Laurent** pour personnaliser les formulations
2. **Écrire les 4 articles Témoignages** (histoires réelles ou composites à valider)
3. **Écrire les 10 articles "Sur le terrain"** (demande input de Laurent sur ses méthodes)
4. **Vérifier et mettre à jour la navigation** de toutes les pages pour inclure "Sur le terrain"
5. **Déployer sur Netlify** (gratuit, en 10 min avec le dossier MLM)
6. **Configurer Brevo** et intégrer l'API key dans les formulaires
7. **Démarrer Instagram** (after blog completion)

---

## 8. NOTES TECHNIQUES IMPORTANTES

- Tous les fichiers articles ont les mêmes classes CSS ajoutées : `.toc`, `.highlight-box`, `.alert-box`, `.faq`, `.author-box`
- La fonction `toggleFaq()` est dans tous les fichiers articles écrits
- Les liens utilisent des chemins relatifs (pas absolus) pour navigation locale
- Chaque article a : canonical URL, og:title, meta description, tag de rubrique
