#!/usr/bin/env python3
"""
MLM Décrypté — Mise à jour automatique de la page d'accueil

Ce script met à jour dynamiquement :
1. Le compteur d'articles publiés (hero section)
2. L'article à la une (le dernier article publié)
3. La grille des 6 derniers articles

Usage :
  python3 update-homepage.py           → met à jour la page d'accueil
  python3 update-homepage.py --dry-run → affiche les changements sans modifier

S'intègre dans le workflow GitHub Actions existant.
"""

import json
import re
import sys
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent
INDEX_FILE = BASE / "index.html"
SCHEDULE_FILE = BASE / "schedule.json"
ARTICLES_DIR = BASE / "articles"

# ═══════════════════════════════════════════
#  Mapping catégorie → tag CSS + emoji
# ═══════════════════════════════════════════
CATEGORY_MAP = {
    "demystifier":     {"tag": "tag--red",    "label": "Démystifier",       "emoji": "🔎", "img": "img-green"},
    "le-modele":       {"tag": "tag--blue",   "label": "Le modèle",        "emoji": "📊", "img": "img-blue"},
    "la-realite":      {"tag": "tag--amber",  "label": "La réalité",       "emoji": "⚖️", "img": "img-amber"},
    "temoignages":     {"tag": "tag--purple", "label": "Témoignage",       "emoji": "🗣️", "img": "img-purple"},
    "mon-regard":      {"tag": "tag--purple", "label": "Mon regard",       "emoji": "✍️", "img": "img-teal"},
    "sur-le-terrain":  {"tag": "tag--green",  "label": "Sur le terrain",   "emoji": "🏕️", "img": "img-teal"},
    "mlm-digital":     {"tag": "tag--blue",   "label": "MLM Digital",      "emoji": "💻", "img": "img-blue"},
    "guides-pratiques":{"tag": "tag--green",  "label": "Guide pratique",   "emoji": "📋", "img": "img-green"},
    "psychologie":     {"tag": "tag--amber",  "label": "Psychologie",      "emoji": "🧠", "img": "img-amber"},
    "mlm-monde":       {"tag": "tag--blue",   "label": "MLM dans le monde","emoji": "🌍", "img": "img-blue"},
    "business":        {"tag": "tag--green",  "label": "Business",         "emoji": "💼", "img": "img-green"},
}

DEFAULT_CATEGORY = {"tag": "tag--green", "label": "Article", "emoji": "📄", "img": "img-green"}


def load_schedule():
    with open(SCHEDULE_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_published_articles(schedule):
    """Retourne les articles publiés (date <= aujourd'hui), triés du plus récent au plus ancien."""
    today = date.today()
    published = []
    for slug, data in schedule.items():
        pub_date = date.fromisoformat(data["publish_date"])
        article_path = ARTICLES_DIR / slug
        if pub_date <= today and article_path.exists():
            published.append({
                "slug": slug,
                "title": data["title"],
                "category": data["category"],
                "date": pub_date,
            })
    published.sort(key=lambda x: x["date"], reverse=True)
    return published


def extract_reading_time(slug):
    """Tente d'extraire le temps de lecture depuis le fichier article."""
    article_path = ARTICLES_DIR / slug
    if not article_path.exists():
        return "5 min"
    content = article_path.read_text(encoding="utf-8")
    # Cherche un pattern comme "⏱ X min" ou "X min de lecture"
    match = re.search(r'(\d+)\s*min', content[:3000])
    if match:
        return f"{match.group(1)} min"
    # Fallback: estimer par nombre de mots
    text_only = re.sub(r'<[^>]+>', '', content)
    words = len(text_only.split())
    minutes = max(3, round(words / 200))
    return f"{minutes} min"


def extract_excerpt(slug):
    """Extrait la meta description comme excerpt."""
    article_path = ARTICLES_DIR / slug
    if not article_path.exists():
        return ""
    content = article_path.read_text(encoding="utf-8")
    match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if match:
        return match.group(1)
    return ""


def format_date_fr(d):
    """Formate une date en français court : '15 mars 2026'."""
    MOIS = {
        1: "jan.", 2: "fév.", 3: "mars", 4: "avr.", 5: "mai", 6: "juin",
        7: "juil.", 8: "août", 9: "sept.", 10: "oct.", 11: "nov.", 12: "déc."
    }
    return f"{d.day} {MOIS[d.month]} {d.year}"


def update_stat_counter(html, count):
    """Met à jour le compteur '41' dans hero__stat-num."""
    pattern = r'(<div class="hero__stat-num">)\d+(</div>\s*<div class="hero__stat-label">Articles publiés)'
    replacement = rf'\g<1>{count}\g<2>'
    return re.sub(pattern, replacement, html)


def update_hero_card(html, article):
    """Met à jour l'article à la une dans le hero."""
    cat_info = CATEGORY_MAP.get(article["category"], DEFAULT_CATEGORY)
    reading_time = extract_reading_time(article["slug"])
    excerpt = extract_excerpt(article["slug"])

    pattern = (
        r'(<aside class="hero__card" aria-label="Article à la une">\s*'
        r'<div class="hero__card-label">Article à la une</div>\s*)'
        r'<h2 class="hero__card-title">[^<]+</h2>\s*'
        r'<p class="hero__card-meta">[^<]+</p>\s*'
        r'<p class="hero__card-excerpt">[^<]+</p>\s*'
        r'<a href="[^"]+" class="read-more">Lire l\'article</a>'
    )

    replacement = (
        rf'\g<1>'
        rf'<h2 class="hero__card-title">{article["title"]}</h2>\n'
        rf'          <p class="hero__card-meta">{reading_time} de lecture · {cat_info["label"]}</p>\n'
        rf'          <p class="hero__card-excerpt">{excerpt}</p>\n'
        rf'          <a href="articles/{article["slug"]}" class="read-more">Lire l\'article</a>'
    )

    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def build_article_card(article, is_large=False):
    """Génère le HTML d'une carte article."""
    cat_info = CATEGORY_MAP.get(article["category"], DEFAULT_CATEGORY)
    reading_time = extract_reading_time(article["slug"])
    excerpt = extract_excerpt(article["slug"])
    date_str = format_date_fr(article["date"])

    large_class = " article-card--large" if is_large else ""
    excerpt_html = f'\n            <p class="article-card__excerpt">{excerpt}</p>' if excerpt else ""

    return f"""        <article class="article-card{large_class}">
          <div class="article-card__img-placeholder {cat_info['img']}">{cat_info['emoji']}</div>
          <div class="article-card__body">
            <span class="tag {cat_info['tag']}">{cat_info['label']}</span>
            <h3 class="article-card__title">{article['title']}</h3>
            <div class="article-card__meta"><span>📅 {date_str}</span><span>⏱ {reading_time}</span></div>{excerpt_html}
            <a href="articles/{article['slug']}" class="read-more">Lire l'article</a>
          </div>
        </article>"""


def update_articles_grid(html, articles):
    """Met à jour la grille des 6 derniers articles."""
    latest_6 = articles[:6]
    cards_html = "\n".join(build_article_card(a) for a in latest_6)

    pattern = r'(<div class="articles__grid">).*?(</div>\s*</div>\s*</section>\s*<!-- ═══ ABOUT STRIP)'
    replacement = rf'\g<1>\n{cards_html}\n      \g<2>'

    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def update_featured_section(html, articles):
    """Met à jour les 3 articles 'essentiels' (featured section)."""
    if len(articles) < 3:
        return html

    # Prendre les 3 derniers articles de catégories différentes pour varier
    seen_cats = set()
    featured = []
    for a in articles:
        if a["category"] not in seen_cats and len(featured) < 3:
            featured.append(a)
            seen_cats.add(a["category"])
    # Compléter si on n'a pas 3 catégories différentes
    for a in articles:
        if len(featured) >= 3:
            break
        if a not in featured:
            featured.append(a)

    main_article = featured[0]
    secondary_1 = featured[1]
    secondary_2 = featured[2]

    main_cat = CATEGORY_MAP.get(main_article["category"], DEFAULT_CATEGORY)
    sec1_cat = CATEGORY_MAP.get(secondary_1["category"], DEFAULT_CATEGORY)
    sec2_cat = CATEGORY_MAP.get(secondary_2["category"], DEFAULT_CATEGORY)

    main_excerpt = extract_excerpt(main_article["slug"])
    main_reading = extract_reading_time(main_article["slug"])
    sec1_reading = extract_reading_time(secondary_1["slug"])
    sec2_reading = extract_reading_time(secondary_2["slug"])

    main_date = format_date_fr(main_article["date"])
    sec1_date = format_date_fr(secondary_1["date"])
    sec2_date = format_date_fr(secondary_2["date"])

    new_featured = f"""      <div class="featured__grid">
        <article class="article-card article-card--large">
          <div class="article-card__img-placeholder {main_cat['img']}">{main_cat['emoji']}</div>
          <div class="article-card__body">
            <span class="tag {main_cat['tag']}">{main_cat['label']}</span>
            <h3 class="article-card__title">{main_article['title']}</h3>
            <div class="article-card__meta"><span>📅 {main_date}</span><span>⏱ {main_reading}</span></div>
            <p class="article-card__excerpt">{main_excerpt}</p>
            <a href="articles/{main_article['slug']}" class="read-more">Lire l'article</a>
          </div>
        </article>
        <div style="display:flex;flex-direction:column;gap:20px;">
          <article class="article-card">
            <div class="article-card__img-placeholder {sec1_cat['img']}" style="aspect-ratio:16/7">{sec1_cat['emoji']}</div>
            <div class="article-card__body">
              <span class="tag {sec1_cat['tag']}">{sec1_cat['label']}</span>
              <h3 class="article-card__title">{secondary_1['title']}</h3>
              <div class="article-card__meta"><span>📅 {sec1_date}</span><span>⏱ {sec1_reading}</span></div>
              <a href="articles/{secondary_1['slug']}" class="read-more">Lire l'article</a>
            </div>
          </article>
          <article class="article-card">
            <div class="article-card__img-placeholder {sec2_cat['img']}" style="aspect-ratio:16/7">{sec2_cat['emoji']}</div>
            <div class="article-card__body">
              <span class="tag {sec2_cat['tag']}">{sec2_cat['label']}</span>
              <h3 class="article-card__title">{secondary_2['title']}</h3>
              <div class="article-card__meta"><span>📅 {sec2_date}</span><span>⏱ {sec2_reading}</span></div>
              <a href="articles/{secondary_2['slug']}" class="read-more">Lire l'article</a>
            </div>
          </article>
        </div>
      </div>"""

    pattern = r'<div class="featured__grid">.*?</div>\s*</div>\s*</div>\s*</section>\s*<!-- ═══ MYTH BUSTERS'
    replacement = new_featured + '\n    </div>\n  </section>\n\n  <!-- ═══ MYTH BUSTERS'

    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def main():
    dry_run = "--dry-run" in sys.argv

    schedule = load_schedule()
    published = get_published_articles(schedule)

    if not published:
        print("Aucun article publié trouvé.")
        return

    count = len(published)
    latest = published[0]

    print(f"\n{'[DRY RUN] ' if dry_run else ''}MLM Décrypté — Mise à jour page d'accueil")
    print(f"  Articles publiés : {count}")
    print(f"  Dernier article  : {latest['title']} ({latest['date']})")
    print(f"  Article à la une : {latest['title']}")

    html = INDEX_FILE.read_text(encoding="utf-8")
    original = html

    # 1. Mettre à jour le compteur
    html = update_stat_counter(html, count)
    print(f"  ✅ Compteur mis à jour → {count} articles")

    # 2. Mettre à jour l'article à la une (hero card)
    html = update_hero_card(html, latest)
    print(f"  ✅ Article à la une → {latest['title']}")

    # 3. Mettre à jour la section featured (3 articles essentiels)
    html = update_featured_section(html, published)
    print(f"  ✅ Section 'Articles essentiels' mise à jour")

    # 4. Mettre à jour la grille des derniers articles
    html = update_articles_grid(html, published)
    print(f"  ✅ Grille des 6 derniers articles mise à jour")

    if html != original:
        if dry_run:
            print(f"\n  → {len(html) - len(original):+d} caractères de différence")
            print("  → Mode dry-run : aucune modification effectuée")
        else:
            INDEX_FILE.write_text(html, encoding="utf-8")
            print(f"\n  → index.html mis à jour avec succès !")
    else:
        print("\n  → Aucune modification nécessaire (déjà à jour)")


if __name__ == "__main__":
    main()
