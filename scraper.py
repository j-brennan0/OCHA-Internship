"""News scraper module for fetching articles from multiple sources"""

import logging
import requests
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from config import (
    NEWS_SOURCES, 
    REQUEST_TIMEOUT, 
    MAX_ARTICLES_PER_SOURCE,
    USER_AGENT,
    LOG_LEVEL,
    LOG_FORMAT,
    OUTPUT_DIR,
    LOG_DIR
)

# Setup logging
Path(LOG_DIR).mkdir(exist_ok=True)
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(f'{LOG_DIR}/scraper_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NewsScraper:
    """Main news scraper class"""
    
    def __init__(self):
        self.articles = []
        self.headers = {'User-Agent': USER_AGENT}
        
    def scrape_rss(self, source_name: str, rss_url: str, search_query: Optional[str] = None) -> List[Dict]:
        """Scrape articles from RSS feed, optionally filtering by search query"""
        try:
            logger.info(f"Scraping RSS feed: {source_name}")
            feed = feedparser.parse(rss_url)
            
            if feed.bozo:
                logger.warning(f"Feed parsing issue for {source_name}: {feed.bozo_exception}")
            
            articles = []
            for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
                # If search query provided, filter articles
                if search_query:
                    title_lower = entry.get('title', '').lower()
                    summary_lower = entry.get('summary', '').lower()
                    query_lower = search_query.lower()
                    
                    # Skip if query not found in title or summary
                    if query_lower not in title_lower and query_lower not in summary_lower:
                        continue
                
                article = {
                    'source': source_name,
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', 'Unknown'),
                    'summary': entry.get('summary', '')[:500],  # Limit summary length
                    'author': entry.get('author', 'Unknown'),
                    'scraped_at': datetime.now().isoformat()
                }
                articles.append(article)
            
            logger.info(f"Successfully scraped {len(articles)} articles from {source_name}")
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {str(e)}")
            return []
    
    def scrape_all_sources(self, search_query: Optional[str] = None) -> List[Dict]:
        """Scrape all configured news sources, optionally filtering by search query"""
        logger.info("Starting scrape of all sources")
        all_articles = []
        
        for source_key, source_config in NEWS_SOURCES.items():
            try:
                if source_config['type'] == 'rss':
                    articles = self.scrape_rss(
                        source_config['name'],
                        source_config['rss_url'],
                        search_query=search_query
                    )
                    all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Failed to scrape {source_config['name']}: {str(e)}")
        
        self.articles = all_articles
        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles
    
    def scrape_single_source(self, source_key: str, search_query: Optional[str] = None) -> List[Dict]:
        """Scrape a single news source by key"""
        if source_key not in NEWS_SOURCES:
            logger.error(f"Source '{source_key}' not found in configuration")
            return []
        
        source_config = NEWS_SOURCES[source_key]
        
        try:
            if source_config['type'] == 'rss':
                articles = self.scrape_rss(
                    source_config['name'],
                    source_config['rss_url'],
                    search_query=search_query
                )
                self.articles = articles
                return articles
        except Exception as e:
            logger.error(f"Failed to scrape {source_config['name']}: {str(e)}")
            return []
    
    def save_to_json(self, filename: Optional[str] = None) -> str:
        """Save articles to JSON file"""
        import json
        
        if not self.articles:
            logger.warning("No articles to save")
            return ""
        
        if filename is None:
            filename = f"articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = Path(OUTPUT_DIR) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.articles)} articles to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")
            return ""
    
    def save_to_csv(self, filename: Optional[str] = None) -> str:
        """Save articles to CSV file"""
        import csv
        
        if not self.articles:
            logger.warning("No articles to save")
            return ""
        
        if filename is None:
            filename = f"articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        output_path = Path(OUTPUT_DIR) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.articles[0].keys())
                writer.writeheader()
                writer.writerows(self.articles)
            logger.info(f"Saved {len(self.articles)} articles to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            return ""
    
    def get_articles_by_source(self, source: str) -> List[Dict]:
        """Filter articles by source"""
        return [a for a in self.articles if a['source'] == source]
    
    def get_articles_count(self) -> Dict[str, int]:
        """Get count of articles per source"""
        counts = {}
        for article in self.articles:
            source = article['source']
            counts[source] = counts.get(source, 0) + 1
        return counts


if __name__ == '__main__':
    scraper = NewsScraper()
    scraper.scrape_all_sources()
    scraper.save_to_json()
    scraper.save_to_csv()
    print(f"Articles by source: {scraper.get_articles_count()}")
