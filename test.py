from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_info(choice):
    site = requests.get(f"https://xn------nzebcaa6hd5qde3bpjch.myciima-weciima.shop/search/{choice}/")
    soup = BeautifulSoup(site.content, "lxml")
    main_div = soup.find_all("div", {"class": "Grid--WecimaPosts"})
    return main_div

def get_movie_info(main_div):
    movies = []
    for movie in main_div[0].find_all("div", {'class': 'GridItem'}):
        movie_title = movie.find('strong').text
        movie_year = movie.find('span').text
        movie_link = movie.find('a')['href']
        downloads = []
        down_list = movie.find_all("ul", {"class": "List--Download--Wecima--Single"})
        for down_div in down_list:
            all_qual = down_div.find_all("a", {'class': 'hoverable activable'})
            for link in all_qual:
                quality = link.find("resolution").text
                download_link = link['href']
                downloads.append({'quality': quality, 'link': download_link})
        movies.append({'title': f"{movie_title} {movie_year}", 'link': movie_link, 'downloads': downloads})
    return movies

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    choice = request.form['choice']
    return redirect(url_for('movies', choice=choice))

@app.route('/movies/<choice>')
def movies(choice):
    main_div = get_info(choice)
    movies = get_movie_info(main_div)
    return render_template('movies.html', movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
