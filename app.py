# authors: Arjun Singh Brar - 1001189
#          Dhanya Laxmi Janaki - 1001288

from flask import Flask, render_template, send_file
import feedparser
import unicodedata
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='/static', static_folder='static')
Bootstrap(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/feed')
def feed():
    RSS_URLS = ['http://www.polygon.com/rss/group/news/index.xml']
    entries = []
    for url in RSS_URLS:
        entries.extend(feedparser.parse(url).entries)

    entries_sorted = sorted(
                           entries,
                           key=lambda e: e.published_parsed,
                           reverse=True)
    return render_template(
            'feed.html',
            entries=entries_sorted
            )


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')


