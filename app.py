from flask import Flask, render_template, request, redirect,url_for
from newscatcher import Newscatcher
from newsfetch.news import newspaper
import requests
from bs4 import BeautifulSoup
from newspaper import Article


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    nc = Newscatcher(website='tengrinews.kz')
    results = nc.get_news()
    
    # Limit to first 20 articles
    articles = results['articles'][:20]
    
    # Modify each article to include a local link for "Read more"
    for article in articles:
        article['local_link'] = "/article?url=" + article['link']
    
    return render_template("home.html", articles=articles)

@app.route("/article")
def article():
    article_url = request.args.get('url')

    if not article_url:
        return render_template("error.html", message="No article URL provided.")

    # Initialize Newspaper Article
    article = Article(article_url)

    try:
        # Download and parse the article
        article.download()
        article.parse()
        
        article_data = {
            'url': article_url,
            'content': article.text
        }
    except Exception as e:
        article_data = {
            'url': article_url,
            'content': f"An error occurred while fetching the article: {str(e)}"
        }
    
    return render_template("article.html", article=article_data)


if __name__ == "__main__":
    app.run(debug=True)
