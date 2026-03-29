#!/usr/bin/env python3
"""
Sitemap generator for MLM Décrypté
Reads schedule.json and generates a valid XML sitemap.xml
Only includes articles that have been published (publish_date <= today)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_today() -> datetime:
    """Get today's date."""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def load_schedule(schedule_path: Path) -> Dict:
    """Load and parse schedule.json file."""
    with open(schedule_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_published_articles(schedule: Dict) -> List[Tuple[str, Dict]]:
    """
    Filter articles that have been published (publish_date <= today).
    Returns list of (slug, article_data) tuples.
    """
    today = get_today()
    published = []

    for slug, article_data in schedule.items():
        publish_date = parse_date(article_data['publish_date'])
        if publish_date <= today:
            published.append((slug, article_data))

    return published


def generate_sitemap_xml(published_articles: List[Tuple[str, Dict]]) -> str:
    """Generate XML sitemap content."""

    # Static pages with their priorities and changefreq
    static_pages = [
        ('https://mlm-decrypte.fr/', 1.0, 'weekly'),
        ('https://mlm-decrypte.fr/a-propos.html', 0.6, 'monthly'),
        ('https://mlm-decrypte.fr/contact.html', 0.5, 'monthly'),
        ('https://mlm-decrypte.fr/categories/demystifier.html', 0.7, 'weekly'),
        ('https://mlm-decrypte.fr/categories/le-modele.html', 0.7, 'weekly'),
        ('https://mlm-decrypte.fr/categories/la-realite.html', 0.7, 'weekly'),
        ('https://mlm-decrypte.fr/categories/temoignages.html', 0.7, 'weekly'),
        ('https://mlm-decrypte.fr/categories/mon-regard.html', 0.7, 'weekly'),
        ('https://mlm-decrypte.fr/categories/sur-le-terrain.html', 0.7, 'weekly'),
    ]

    # Build XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    # Add static pages
    for url, priority, changefreq in static_pages:
        xml_lines.extend([
            '  <url>',
            f'    <loc>{url}</loc>',
            f'    <priority>{priority}</priority>',
            f'    <changefreq>{changefreq}</changefreq>',
            '  </url>',
        ])

    # Add published articles
    for slug, article_data in published_articles:
        url = f'https://mlm-decrypte.fr/articles/{slug}'
        lastmod = article_data['publish_date']
        priority = 0.8
        changefreq = 'monthly'

        xml_lines.extend([
            '  <url>',
            f'    <loc>{url}</loc>',
            f'    <lastmod>{lastmod}</lastmod>',
            f'    <priority>{priority}</priority>',
            f'    <changefreq>{changefreq}</changefreq>',
            '  </url>',
        ])

    xml_lines.append('</urlset>')

    return '\n'.join(xml_lines)


def main():
    """Main entry point."""
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    schedule_path = script_dir / 'schedule.json'
    sitemap_path = script_dir / 'sitemap.xml'

    # Load schedule
    print(f"Loading schedule from {schedule_path}...")
    schedule = load_schedule(schedule_path)

    # Get published articles
    published = get_published_articles(schedule)
    print(f"Found {len(published)} published articles out of {len(schedule)} total")

    # Generate sitemap XML
    sitemap_xml = generate_sitemap_xml(published)

    # Write sitemap to file
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)

    print(f"Sitemap written to {sitemap_path}")
    print(f"Total URLs in sitemap: {len(published) + 9} (9 static pages + {len(published)} articles)")


if __name__ == '__main__':
    main()
