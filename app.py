import feedparser
import json
import datetime
from datetime import timedelta


# Identify the keys provided by feed
feed = feedparser.parse('https://feed.itsfoss.com/')
keys = feed.entries[0].keys()
values = feed.values()
entries = feed.entries

metadata = feed.feed
metadata_keys = metadata.keys()

articles = []
fetched = 0
expired = 0

today = datetime.datetime.now(datetime.timezone.utc)
time_difference = timedelta(days=1)
expiration_limit = today - time_difference

existing_urls = set()

try:
    with open("posted.txt", "r") as file:
        for line in file:
            if line.startswith("Url"):
                url = line.replace("Url: ", "").strip()
                existing_urls.add(url)
except FileNotFoundError:
    print("File doesn't exist")

for article in entries:

    article_publish_time = datetime.datetime.strptime(article.published, "%a, %d %b %Y %H:%M:%S %z")

    if article_publish_time > expiration_limit:
        is_duplicate = False

        if article.link in existing_urls:
            is_duplicate = True
        else:
            for saved_article in articles:
                if saved_article['Url: '] == article.link:
                    is_duplicate = True
                    break

        if is_duplicate:
            print("Skipping duplicate entries...")
            continue


        article_publish_time = article_publish_time.date()

        items = {
            'Title: ': article.title,
            'Url: ' : article.link,
            'Description: ' : article.summary,
            'Written by: ' : article.author,
            'Date: ' : article_publish_time,
            'Source: ' : metadata.link,
            }
        
        articles.append(items)
        fetched = fetched + 1   
    else:
        expired = expired + 1

with open("posted.txt", "a") as file:
    for article in articles:
        for key, value in article.items():
            file.write(f"{key}{value}\n")
        file.write(f"\n")  

print("Total number of articles fetched: ",fetched)   
print("No. of expired articles skipped: ",expired)

