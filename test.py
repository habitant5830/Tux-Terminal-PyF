import requests
from bs4 import BeautifulSoup
import lxml

# pretend like a browser
urls = [
    'https://9to5linux.com/feed/',
    'https://www.gamingonlinux.com/article_rss.php?newsonly',
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '}
Feeds = []

for url in urls:
    resp = requests.get(url, headers=headers)

    soup = BeautifulSoup(resp.content, 'xml')

    # obtain all entries on the feed url
    items = soup.find_all('item')
    print(items)
    # RSS 2.0 format
    for item in items:
        title = item.title.text
        description = item.description # Prints none if nothing
        link = item.link.text #

        # Double parsing (xml parsing + html parsing)
        text = ''
        if description:
            desc_soup = BeautifulSoup(description.get_text(), 'html.parser')
            for p in desc_soup.find_all('p'):
                # Skip paragraphs that are empty or image-only
                if p.get_text().strip():
                    text = p.get_text()
                    break  # first real text paragraph is the summary

        Feeds.append({'Title': title, 'Link': link, 'Description': text})
