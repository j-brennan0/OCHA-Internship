"""Configuration for news scraper"""

# News sources configuration
NEWS_SOURCES = {
    'bbc': {
        'name': 'BBC News',
        'rss_url': 'http://feeds.bbc.co.uk/news/rss.xml',
        'type': 'rss'
    },
    'reuters': {
        'name': 'Reuters',
        'rss_url': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&output=rss',
        'type': 'rss'
    },
    'ap': {
        'name': 'Associated Press',
        'rss_url': 'https://apnews.com/apf-services/v2/news/rss',
        'type': 'rss'
    },
    'guardian': {
        'name': 'The Guardian',
        'rss_url': 'https://www.theguardian.com/international/rss',
        'type': 'rss'
    },
    'nyt': {
        'name': 'New York Times',
        'rss_url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
        'type': 'rss'
    },
}

# Output settings
OUTPUT_FORMATS = ['json', 'csv']
OUTPUT_DIR = './output'
LOG_DIR = './logs'

# Scraper settings
REQUEST_TIMEOUT = 10  # seconds
MAX_ARTICLES_PER_SOURCE = 50
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
