import requests
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import lxml

app = Flask(__name__)

# SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Todo list
@app.route("/todo.html", methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("todo.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem.'

@app.route("/update/<int:id>", methods=['GET', 'POSsour T'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem.'
    else:
        return render_template('update.html', task=task)

# App routes
home_articles = [
               {
                   'tag': "PRIVACY",
                   'title': "Why You Should Always Use a VPN",
                   'summary':
                       "Explaining the importance of using VPNs these days and recommending some highly trusted VPN providers that are known to be secure and have a strict no-logs policy.",
                   'link': "/articles/why_use_a_vpn.html",
               },
               {
                   'tag': "REVIEW",
                   'title': "My Experience Using OpenSUSE",
                   'summary':
                       "A review on OpenSUSE after 1 week of use. Everything covered about the advantages, disadvantages and what can be improved as an enterprise linux distribution.",
                   'link': "/articles/opensuse-1week-review.html",
               },
               {
                   'tag': "ENSHITTIFICATION",
                   'title': "The Era of Heavy Bloated Web",
                   'summary':
                       "Explaining why modern websites are more bloated and resource hungry.",
                   'link': "/articles/bloated-web.html",
               },
               {
                   'tag': "NETWORK",
                   'title': "DNS: The Telephone Directory of the Internet",
                   'summary':
                       "Explaining how DNS works and why its important to choose a secure DNS provider!",
                   'link': "/articles/domain-name-system.html",
               },
    ]

@app.route("/")
def index():
    return render_template("index.html", home_articles=home_articles)

# late-binding closure fix
for home_article in home_articles:
    slug = home_article['link'].strip('/')
    def make_view(slug=slug, home_article=home_article):
        return render_template(f'{slug}')
    app.add_url_rule(home_article['link'], endpoint=f'home_article_{slug}', view_func=make_view)

@app.route("/articles")
def articles():
    return render_template("articles.html", articles=articles)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

articles = [
    {
        'tag': "PRIVACY",
        'title': "Why You Should Always Use a VPN",
        'summary':
            "Explaining the importance of using VPNs these days and recommending some highly trusted VPN providers that are known to be secure and have a strict no-logs policy.",
        'link': "/articles/why_use_a_vpn.html",
    },
    {
        'tag': "REVIEW",
        'title': "My Experience Using OpenSUSE",
        'summary':
            "A review on OpenSUSE after 1 week of use. Everything covered about the advantages, disadvantages and what can be improved as an enterprise linux distribution.",
        'link': "/articles/opensuse-1week-review.html",
    },
    {
        'tag': "ENSHITTIFICATION",
        'title': "The Era of Heavy Bloated Web",
        'summary':
            "Explaining why modern websites are more bloated and resource hungry.",
        'link': "/articles/bloated-web.html",
    },
    {
        'tag': "NETWORK",
        'title': "DNS: The Telephone Directory of the Internet",
        'summary':
            "Explaining how DNS works and why its important to choose a secure DNS provider!",
        'link': "/articles/domain-name-system.html",
    },
    {
        'tag': "SECURITY",
        'title': "How Encryption Powers the Internet.",
        'summary':
            "Taking a deep dive into the working of encryption on the modern web.",
        'link': "/articles/encryption.html",
    },
    {
        'tag': "PRIVACY",
        'title': "Fingerprinting: The Hidden Trap on the Modern Web",
        'summary':
            "Explained various fingerprinting methods used in the modern web and what to do about it.",
        'link': "/articles/fingerprinting.html",
    },
    {
        'tag': "RECOMMENDATION",
        'title': "Cool and Useful Firefox Add-ons I Use Daily",
        'summary': "Recommendation of some cool privacy-respecting Firefox add-ons.",
        'link': "/articles/firefox-addons.html",
    },
    {
        'tag': "REVIEW",
        'title': "Firefox Is Slowly Becoming Bloatware. Seriously...",
        'summary': "How Firefox has been slowly becoming bloatware from a goat.",
        'link': "/articles/firefox-browser-review.html",
    },
    {
        'tag': "ANALYSIS",
        'title': "Google Chrome: The Ultimate Weapon of Google Monopoly",
        'summary': "A case study on Google Chrome's worst privacy practices.",
        'link': "/articles/google-chrome-case-study.html",
    },
    {
        'tag': "PRIVACY",
        'title': "Beyond GPS: The Hidden Ways Your Phone Tracks You",
        'summary':
            "How carriers, governments, and data brokers log your physical movements without your knowledge.",
        'link': "/articles/location-tracking.html",
    },
    {
        'tag': "REVIEW",
        'title': "You Should Stop Using Meta (Facebook) Products at All Costs",
        'summary': "Why everyone should stop using Meta products at all costs.",
        'link': "/articles/meta-privacy.html",
    },
    {
        'tag': "PRIVACY",
        'title': "Effective Web Tracking Methods in 2026: Explained",
        'summary':
            "Explaining online tracking methods that are still effective in 2026.",
        'link': "/articles/online-tracking-methods.html",
    },
    {
        'tag': "DIGITAL WELLBEING",
        'title': "The Harmful Effects of Watching Short-Form Content.",
        'summary':
            "You should prioritize long-form contents over short-form contents. Here's why.",
        'link': "/articles/short-form-contents.html",
    },
    {
        'tag': "DIGITAL WELLBEING",
        'title': "Deleting Social Media Can Be a Good Treat for Your Brain.",
        'summary':
            "Why should you consider deleting social media for your mental health? Here is why...",
        'link': "/articles/social-media-detox.html",
    },
    {
        'tag': "PSYCHOLOGY",
        'title':
            "You Aren't Broken: A Clear Guide to Trauma, Overthinking, and Healing",
        'summary':
            "Explaining what trauma is, how it changes an individual's brain, and how it can be healed.",
        'link': "/articles/trauma.html",
    },
    {
        'tag': "REVIEW",
        'title': "I Tried Vivaldi on Linux Just to Find Out It's Not for Me",
        'summary': "Why vivaldi browser is not that great? What holds it back!",
        'link': "/articles/vivaldi-browser-review.html",
    },
    {
        'tag': "PHILOSOPHY",
        'title': "Nihilism: How I Saw the World",
        'summary':
            "My perspective on the philosophical theory 'nihilism' on modern society.",
        'link': "/articles/nihilism.html",
    },
]

# late-binding closure fix
for article in articles:
    slug = article['link'].strip('/')
    def make_view(slug=slug, article=article):
        return render_template(f'{slug}')
    app.add_url_rule(article['link'], endpoint=f'article_{slug}', view_func=make_view)

# Feed parsing
# pretend like a browser
def rss_feed():
    urls = [
        'https://9to5linux.com/feed/',
        'https://www.gamingonlinux.com/article_rss.php?newsonly',
        'https://www.phoronix.com/rss.php',
        'https://lwn.net/headlines/newrss',
        'https://9to5linux.com/feed',
        'https://archlinux.org/feeds/news/',
        'https://bits.debian.org/feeds/feed.rss',
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    Feeds = []
    seen = set()

    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.content, 'xml')
            # obtain all entries on the feed url
            items = soup.find_all('item')

            # RSS 2.0 format
            for item in items:
                link_tag = item.link
                title_tag = item.title
                pubdate_tag = item.pubDate
                category_tag = item.category

                if not link_tag or not link_tag.text:
                    continue
                if not title_tag or not title_tag.text:
                    continue
                if not pubdate_tag or not pubdate_tag.text:
                    continue

                # Filter duplicate posts
                link = link_tag.text
                if link in seen:
                    continue

                # date
                now = datetime.now(timezone.utc)
                formatted_date = datetime.strptime(pubdate_tag.text, '%a, %d %b %Y %H:%M:%S %z')
                date = formatted_date.strftime('%a, %d %b %Y %I:%M %p')

                if (now - formatted_date) > timedelta(hours=48):
                    continue

                # Skip promotional/paid posts
                title = title_tag.text
                if '[$]' in title:
                    continue

                seen.add(link)

                category = category_tag.text if category_tag else ''
                description = item.description

                # Double parsing (xml parsing + html parsing)
                text = ''
                if description:
                    desc_soup = BeautifulSoup(description.get_text(), 'html.parser')
                    for p in desc_soup.find_all('p'):
                        # Skip paragraphs that are empty or image-only
                        if p.get_text().strip():
                            text = p.get_text()
                            break  # first real text paragraph is the summary

                Feeds.append({'title': title, 'date': date, 'link': link, 'description': text, 'category': category, 'published': formatted_date})
        except Exception as e:
            print(f"Feed failed: {url} - {e}")

    # Sort output based on published date
    Feeds.sort(key=lambda x: x['published'], reverse=True)
    return Feeds

@app.route('/live-feed')
def live_feed():
    feeds = rss_feed()
    return render_template("live-feed.html", feeds=feeds)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)