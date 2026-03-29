#!/usr/bin/env python3
"""
RSS 2.0 feed generator for MLM Décrypté
Reads schedule.json and generates a valid RSS 2.0 feed (feed.xml)
Only includes articles that have been published (publish_date <= today and status != "planned")
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from email.utils import formatdate


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


def slug_to_category_name(category_slug: str) -> str:
    """Convert category slug to readable category name."""
    category_map = {
        'le-modele': 'Le Modèle MLM',
        'demystifier': 'Décrypter le MLM',
        'la-realite': 'La Réalité du MLM',
        'temoignages': 'Témoignages',
        'mon-regard': 'Mon Regard',
        'sur-le-terrain': 'Sur le Terrain',
    }
    return category_map.get(category_slug, category_slug)


def get_published_articles(schedule: Dict) -> List[Tuple[str, Dict]]:
    """
    Filter articles that have been published.
    Criteria: publish_date <= today AND status != "planned"
    Returns list of (slug, article_data) tuples, sorted by date (newest first).
    """
    today = get_today()
    published = []

    for slug, article_data in schedule.items():
        publish_date = parse_date(article_data['publish_date'])
        status = article_data.get('status', 'scheduled')

        # Include if date is published and status is not "planned"
        if publish_date <= today and status != 'planned':
            published.append((slug, article_data))

    # Sort by publish_date descending (newest first)
    published.sort(
        key=lambda x: parse_date(x[1]['publish_date']),
        reverse=True
    )

    return published


def date_to_rfc822(date_str: str) -> str:
    """
    Convert YYYY-MM-DD format to RFC 822 format for RSS.
    Uses noon UTC as the time for consistency.
    """
    dt = parse_date(date_str)
    # formatdate returns RFC 2822 format, which is compatible with RSS 2.0
    # Use localtime=False to get UTC time
    return formatdate(dt.timestamp(), usegmt=True)


def escape_xml(text: str) -> str:
    """Escape special characters for XML."""
    if not text:
        return text
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def generate_rss_xml(published_articles: List[Tuple[str, Dict]]) -> str:
    """Generate RSS 2.0 feed content."""

    blog_url = 'https://mlm-decrypte.fr'
    blog_title = 'MLM Décrypté'
    blog_description = (
        'Le blog qui décrypte le marketing de réseau sans tabou. '
        'Articles de fond, témoignages et retours d\'expérience terrain.'
    )
    language = 'fr'

    # Build XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '  <channel>',
        f'    <title>{escape_xml(blog_title)}</title>',
        f'    <link>{blog_url}</link>',
        f'    <description>{escape_xml(blog_description)}</description>',
        f'    <language>{language}</language>',
    ]

    # Add last build date (today)
    today = get_today()
    last_build_date = formatdate(today.timestamp(), usegmt=True)
    xml_lines.append(f'    <lastBuildDate>{last_build_date}</lastBuildDate>')

    # Add articles as items
    for slug, article_data in published_articles:
        title = article_data['title']
        category = article_data['category']
        publish_date = article_data['publish_date']

        # Use description if available, otherwise use title
        description = article_data.get('description', title)

        # Build article URL
        article_url = f'{blog_url}/articles/{slug}'

        # Convert publish date to RFC 822
        pub_date_rfc822 = date_to_rfc822(publish_date)

        # Get readable category name
        category_name = slug_to_category_name(category)

        xml_lines.extend([
            '    <item>',
            f'      <title>{escape_xml(title)}</title>',
            f'      <link>{article_url}</link>',
            f'      <description>{escape_xml(description)}</description>',
            f'      <pubDate>{pub_date_rfc822}</pubDate>',
            f'      <category>{escape_xml(category_name)}</category>',
            f'      <guid>{article_url}</guid>',
            '    </item>',
        ])

    xml_lines.extend([
        '  </channel>',
        '</rss>',
    ])

    return '\n'.join(xml_lines)


def main():
    """Main entry point."""
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    schedule_path = script_dir / 'schedule.json'
    feed_path = script_dir / 'feed.xml'

    # Load schedule
    print(f"Loading schedule from {schedule_path}...")
    schedule = load_schedule(schedule_path)
    print(f"Total articles in schedule: {len(schedule)}")

    # Get published articles
    published = get_published_articles(schedule)
    print(f"Found {len(published)} published articles")

    # Generate RSS feed XML
    rss_xml = generate_rss_xml(published)

    # Write feed to file
    with open(feed_path, 'w', encoding='utf-8') as f:
        f.write(rss_xml)

    print(f"RSS feed written to {feed_path}")
    print(f"Feed contains {len(published)} articles")


if __name__ == '__main__':
    main()
