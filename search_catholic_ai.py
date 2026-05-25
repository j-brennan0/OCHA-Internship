"""Script to search for Catholic Church and AI articles from NYT"""

import feedparser
from datetime import datetime
import json
from pathlib import Path

def search_nyt_for_catholic_ai():
    """Search New York Times RSS feed for Catholic Church and AI articles"""
    
    nyt_rss_url = 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'
    
    print("📰 Fetching New York Times articles...")
    print(f"   URL: {nyt_rss_url}\n")
    
    feed = feedparser.parse(nyt_rss_url)
    
    if feed.bozo:
        print(f"⚠️  Warning: Feed parsing issue: {feed.bozo_exception}")
    
    # Search for articles mentioning Catholic Church and AI
    matching_articles = []
    all_articles = []
    
    for entry in feed.entries:
        title = entry.get('title', '').lower()
        summary = entry.get('summary', '').lower()
        
        all_articles.append({
            'title': entry.get('title', 'No title'),
            'link': entry.get('link', ''),
            'published': entry.get('published', 'Unknown'),
            'summary': entry.get('summary', '')[:500],
        })
        
        # Check if article contains relevant terms
        content = f"{title} {summary}"
        
        # Look for articles about Catholic Church/Pope AND AI/technology
        has_catholic = any(term in content for term in ['catholic', 'church', 'pope', 'vatican'])
        has_ai = any(term in content for term in ['ai', 'artificial intelligence', 'technology', 'algorithm'])
        
        if has_catholic and has_ai:
            matching_articles.append({
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', 'Unknown'),
                'summary': entry.get('summary', '')[:500],
                'author': entry.get('author', 'Unknown'),
                'scraped_at': datetime.now().isoformat()
            })
    
    print(f"✅ Found {len(matching_articles)} articles about Catholic Church & AI")
    print(f"   (from {len(all_articles)} total articles in NYT World feed)\n")
    
    if matching_articles:
        print("=" * 80)
        print("MATCHING ARTICLES:")
        print("=" * 80)
        
        for i, article in enumerate(matching_articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Published: {article['published']}")
            print(f"   Author: {article['author']}")
            print(f"   Link: {article['link']}")
            print(f"   Summary: {article['summary'][:300]}...")
            print("-" * 80)
        
        # Save to JSON
        output_dir = Path('./output')
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"nyt_catholic_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(matching_articles, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Results saved to: {output_file}")
    else:
        print("❌ No articles found matching 'Catholic Church' and 'AI'")
        print("\n📰 Recent NY Times World articles:")
        print("=" * 80)
        
        for i, article in enumerate(all_articles[:10], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Published: {article['published']}")
            print(f"   Link: {article['link']}")
            print(f"   Summary: {article['summary'][:200]}...")
        
        print("\nNote: The NY Times RSS feed has limited articles.")
        print("For more comprehensive search, consider using:")
        print("  - NY Times API (requires key)")
        print("  - Guardian API (free tier available)")
        print("  - Custom web scraping with BeautifulSoup")

if __name__ == '__main__':
    search_nyt_for_catholic_ai()
