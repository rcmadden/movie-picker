'''
Integrate the "movie picker" OO code from Exercise 4 into the simple Flask web app
we wrote during class #3.

Five views:
  /                    -> Display a list of categories
  /movies/<category>   -> Display a list of all movies for a given category
  /movie/<title>       -> Display movie details from omdbapi.com for the given title
  /random              -> Display a random movie's details from a random category, ask if the user wants to save it to their list
  /user                -> Show a list of the user's saved movies

For saving the random movie we don't actually need to save anything yet. Same goes for
the list of the user's saved movies, just hardcode the list of titles for now.

Bonus: Use Jinja2's "extends" and "block" directives to have all of your templates
inherit from a "base" template.

Bonus: Grab a Bootstrap theme from https://bootswatch.com/ and put that into your
base template so that your app looks nicer!
'''
from urllib.request import urlopen

from flask import Flask, render_template, request

from movies import Movie, fetch_omdb_info, fetch_wikipedia_titles #, MoviePicker

app = Flask(__name__)

CATEGORIES = [
    'American_action_thriller_films',
    'American_biographical_films',
    'American_crime_drama_films',
    'American_drama_films',
    'American_epic_films',
    'American_romantic_comedy_films',
    'American_satirical_films',
    'American_science_fiction_films',
]

@app.route('/')
def index():
    categories = "\n".join(['<li><a href="/movies/{0}">{0}</a></li>'.format(c) for c in CATEGORIES])
    return "<ul>{}</ul>".format(categories)


@app.route('/movies/<category>')
def show_movies(category):
    titles = fetch_wikipedia_titles(category)
    return render_template("movies.html", category=category, titles=titles)


@app.route('/movie/<title>')
def show_movie(title):
    movie = Movie(fetch_omdb_info(title))
    return render_template("movie.html", movie=movie, movie_poster_url=movie.poster_url)

@app.route('/rehost_image')
def rehost_image():
    image = urlopen(request.args['url'])
    # return image #'HTTPResponse' object is not callable must read it
    # return (image.read(), '200 OK', {'Content-type': 'image/jpeg'})
    return image.read()


# @app.route('/movie/<details>')
# def show_details(details):
#     info = movies.fetch_omdb_info(details)
#     return render_template("movie.html", info=info)


if __name__ == '__main__':
    debug = True # TODO: set to False when pushed to production
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(host='0.0.0.0', use_reloader=True)