import feedparser
import json

# Identify the keys provided by feed
feed = feedparser.parse('https://feed.itsfoss.com/')
keys = feed.entries[0].keys()
values = feed.values()
entries = feed.entries

metadata = feed.feed
metadata_keys = metadata.keys()

articles = {}

for article in entries:
    items = {
        'Title: ': article.title,
        'Url: ' : article.link,
        'Description: ' : article.summary,
        'Written by: ' : article.author,
        'Date: ' : article.published,
        'Source: ' : metadata.link,
    }

    articles = items

for i in articles:
    for j in articles:
        print(j,':',articles[j])
    
print("Total number of articles fetched: ",len(entries))