import feedparser

# Identify the keys provided by feed
feed = feedparser.parse('https://feed.itsfoss.com/')
keys = feed.entries[0].keys()
values = feed.values()
entries = feed.entries

metadata = feed.feed
metadata_keys = metadata.keys()

print('Available feed keys: ',keys)
print('Available metadata keys: ',metadata_keys)

for article in entries:
    print('Title: ',article.title)
    print('Url: ',article.link)
    print('Description: ',article.summary)
    print('Written by: ',article.author)
    print('Date: ',article.published)
    print('Source: ',metadata.link)
    print('')
    
print("Total number of articles fetched: ",len(entries))