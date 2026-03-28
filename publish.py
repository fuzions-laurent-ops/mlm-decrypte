#!/usr/bin/env python3
"""
MLM Décrypté — Script de publication automatique
Usage:
  python3 publish.py          → publie les articles dont la date est passée
  python3 publish.py --status → affiche le calendrier éditorial complet
  python3 publish.py --init   → initialise : ajoute noindex aux articles futurs
"""

import json
import sys
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent
ARTICLES_DIR = BASE / "articles"
SCHEDULE_FILE = BASE / "schedule.json"

NOINDEX_TAG = '<meta name="robots" content="noindex,nofollow">'
NOINDEX_MARKER = '<!-- publication-pending -->'


def load_schedule():
    with open(SCHEDULE_FILE, encoding="utf-8") as f:
        return json.load(f)


def has_noindex(content):
    return NOINDEX_MARKER in content


def add_noindex(content):
    if has_noindex(content):
        return content
    return content.replace(
        "<head>",
        "<head>\n  " + NOINDEX_MARKER + "\n  " + NOINDEX_TAG,
        1
    )


def remove_noindex(content):
    content = content.replace("  " + NOINDEX_MARKER + "\n  " + NOINDEX_TAG + "\n", "")
    content = content.replace(NOINDEX_MARKER + "\n  " + NOINDEX_TAG + "\n", "")
    return content


def init():
    schedule = load_schedule()
    today = date.today()
    added = 0
    already = 0

    for slug, data in schedule.items():
        pub_date = date.fromisoformat(data["publish_date"])
        article_path = ARTICLES_DIR / slug
        if not article_path.exists():
            print(f"Warning: {slug} not found")
            continue

        content = article_path.read_text(encoding="utf-8")
        if pub_date > today:
            if not has_noindex(content):
                article_path.write_text(add_noindex(content), encoding="utf-8")
                added += 1
            else:
                already += 1
        else:
            if has_noindex(content):
                article_path.write_text(remove_noindex(content), encoding="utf-8")
                print(f"  Retiré noindex (date passée) : {slug}")

    print(f"\n{added} articles marqués noindex (publication future)")
    print(f"{already} déjà marqués")


def publish():
    schedule = load_schedule()
    today = date.today()
    published = []
    upcoming = []

    for slug, data in schedule.items():
        pub_date = date.fromisoformat(data["publish_date"])
        article_path = ARTICLES_DIR / slug
        if not article_path.exists():
            continue

        content = article_path.read_text(encoding="utf-8")
        if pub_date <= today:
            if has_noindex(content):
                article_path.write_text(remove_noindex(content), encoding="utf-8")
                published.append((slug, data["title"], pub_date))
        else:
            upcoming.append((slug, data["title"], pub_date))

    if published:
        print(f"\n{len(published)} article(s) publiés aujourd'hui :")
        for slug, title, d in published:
            print(f"  OK  {d}  {title}")
    else:
        print("\nAucun nouvel article à publier aujourd'hui.")

    if upcoming:
        next3 = sorted(upcoming, key=lambda x: x[2])[:3]
        print(f"\nProchaines publications :")
        for slug, title, d in next3:
            delta = (d - today).days
            print(f"  --> {d}  (dans {delta}j)  {title}")

    print("\nN'oublie pas de re-déployer le site sur Netlify apres execution !")


def status():
    schedule = load_schedule()
    today = date.today()
    live = []
    pending = []

    for slug, data in schedule.items():
        pub_date = date.fromisoformat(data["publish_date"])
        if pub_date <= today:
            live.append((pub_date, data["title"], data["category"]))
        else:
            pending.append((pub_date, data["title"], data["category"]))

    live.sort()
    pending.sort()

    print(f"\nCALENDRIER EDITORIAL — MLM Décrypté")
    print(f"Aujourd'hui : {today}")
    print(f"Articles en ligne : {len(live)}")
    print(f"Articles planifies : {len(pending)}")

    if live:
        print(f"\nEN LIGNE ({len(live)}) :")
        for d, title, cat in live:
            print(f"  {d}  [{cat:<15}]  {title}")

    if pending:
        print(f"\nPLANIFIES ({len(pending)}) :")
        for d, title, cat in pending:
            delta = (d - today).days
            print(f"  {d}  +{delta:>3}j  [{cat:<15}]  {title}")


if __name__ == "__main__":
    if "--init" in sys.argv:
        init()
    elif "--status" in sys.argv:
        status()
    else:
        publish()
