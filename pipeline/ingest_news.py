import feedparser
import pandas as pd

def fetch_rss_news():
    url = "https://feeds.bbci.co.uk/news/business/rss.xml"

    feed = feedparser.parse(url)

    print("Fetching RSS...")
    print(f"Entries found: {len(feed.entries)}")

    records = []

    for entry in feed.entries[:10]:
        records.append({
            "date": entry.get("published", None),
            "title": entry.get("title", None),
            "text": entry.get("summary", None),
            "source": "news",
            "entity_type": "article",
            "company": None,
            "location": None,
            "value": None
        })

    return pd.DataFrame(records)