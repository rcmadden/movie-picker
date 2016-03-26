import json
import random
from urllib.request import urlopen
from urllib.parse import quote
# import urllib
# import urllib.request
# from urllib.parse import urlparse
import pprint

DEFAULT_CATEGORY = "American_science_fiction_action_films"
WIKIPEDIA_CATEGORY_URL = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{}&format=json&cmlimit=250&cmcontinue={}"
OMDBAPI_TITLE_URL = "http://www.omdbapi.com/?t={}&y=&plot=short&r=json&tomatoes=true"

#have the user pick this many movies before quitting
NUM_MOVIES = 3

#use this to build the URL to the movie on IMDB, e.g.: http://www.imdb.com/title/tt0093773
IMDB_URL = "http://www.imdb.com/title/{}"

## API code ###################################################################
# https://www.mediawiki.org/wiki/API:Main_page

def clean_title(title):
    '''
    Removes "(film)", "(serial)", "(1998 film)", etc. from the given Wikipedia
    page title.
    >>> clean_title('Beowulf (1999 film)')
    'Beowulf'
    '''
    title = title.replace("(film)", "")
    # title = title.replace("(serial)", "")
    # title = title.replace("(series)", "")
    if "film)" in title:
        # import pdb; pdb.set_trace()
        #"Godzilla (2014 film)" -> ['Godzilla ', '2014 film)']
        title, year_of_film = title.split("(", 1)
        #if this assert fails, then I need to think of another way to split this text off the title...
        assert "film)" in year_of_film
    return title.strip()

def filter_titles(members):
    '''
    Filter and clean the raw page titles from Wikipedia categorymembers call.
    '''
    titles = []
    for m in members:
        title = m['title']
        if 'Category:' in title:
            continue #ignore sub-categories
        title = clean_title(title)
        titles.append(title)
    return titles

def fetch_wikipedia_titles(category):
    '''
    Returns a list of dictionaries returned by the Wikipedia categorymembers API call.
    '''
    cmcontinue = ''
    out = []
    while True:
        #1. build the URL using WIKIPEDIA_CATEGORY_URL
        url = WIKIPEDIA_CATEGORY_URL.format(category, cmcontinue)
        #2. use urllib.urlopen on that URL for python 3 use urllib.request
        #3. use json.loads to parse the response
        with urlopen(url) as response:
            html = response.read().decode('utf8')
            data = json.loads(html)
        #4. return only the titles from the JSON response (which are inside 'categorymembers')
        # pprint.pprint(data.get('query'))
        out.extend(data['query']['categorymembers']) # list of dictionaries
        if 'continue' not in data:
            break
        #5. (bonus) figure out how to implement retrieving the next page of results (using the 'cmcontinue' value)
        cmcontinue = data['continue']['cmcontinue']
    return filter_titles(out)

def fetch_omdb_info(title):
    '''
    Retrieve movie information from OMDb API's title search. and encode url spaces https://docs.python.org/3/library/urllib.parse.html
    '''
    # import pdb; pdb.set_trace()
    #TODO: Similar to fetch_wikipedia_titles, but a little simpler:
    #1. build the URL using OMDBAPI_TITLE_URL iterate through list of titles here or in main?
    omdb_url = OMDBAPI_TITLE_URL.format(quote(title))
    #2. use urllib.urlopen on that URL
    with urlopen(omdb_url) as response:
            html = response.read().decode('utf8')
            data = json.loads(html)
    # if data.get('Error'):
        # raise RuntimeError("OMDb API returned {!r} when looking up {!r}".format(data['Error'], title))
    #3. use json.loads to parse the response
    #4. return that data (it will be a python dictionary)
    return data


## classes ####################################################################

class Movie(object):
    '''
    Represents a movie with data from the omdbapi.com.
    '''
    def __init__(self, data):
        self.data = data

    @property
    def title(self):
        return self.data['Title']

    def __str__(self):
        #TODO: Move your formatting code from ex3.py into this __str__ method.
        #When you `print` an object, its __str__ method (if it has one) is called to
        #turn the object into a string. Instead of directly printing it, just build
        #up the string and return it. Note that str needs to return a bytestring, while
        #the strings inside self.data are unicode, so we use encode('utf8') before returning
        #the result.
        txt = u"Title: {}".format(self.data['Title'])
        return txt.encode('utf8')

class MoviePicker(object):
    '''
    Random movie picker functionality. Returns random movies and keeps track of picked movies.
    '''
    def __init__(self, titles):
        '''
        Initializes the MoviePicker with a list of `titles` that will be picked from randomly.
        '''
        # self.titles = random.sample(titles, len(titles))
        # self.picked = []
        pass

    def get_random_movie(self):
        '''
        Pick a random title, fetch its data from OMDB, and return it as a Movie object.
        '''
        #TODO: Move your "get a random movie" logic from ex3.py into this method. Instead of
        #picking from the JSON, you will pick from self.titles, then call `fetch_omdb_info`
        #to get the movie data, pass that data into Movie() to turn it into a Movie object,
        #the return that object.
        pass

    def add_to_list(self, m):
        '''Add the given Movie object `m` to the list of picked movies.'''
        #TODO: just append the given Movie object to self.picked
        pass

    def get_list(self):
        '''Returns a list of picked titles.'''
        #TODO: return `m.title` for each of the movies in self.picked
        pass

## main #######################################################################

def main():
    # picker = MoviePicker(fetch_wikipedia_titles(DEFAULT_CATEGORY))
    # return picker
    # fetch_wikipedia_titles(DEFAULT_CATEGORY)
    wiki_titles = fetch_wikipedia_titles(DEFAULT_CATEGORY)
    return fetch_omdb_info(wiki_titles[0])

    # pprint.pprint(wiki_titles)
    # pprint.pprint(wiki_tites)
    # num_picked = 0
    # while num_picked < NppUM_MOVIES:
    #     movie = picker.get_random_movie()
    #     print(movie)
    #     answer = raw_input("Add movie to your list? ")
    #     if answer.lower().startswith('y'):
    #         picker.add_to_list(movie)
    #         num_picked += 1
    # print("\n== Your movies ==\n")
    # for title in picker.get_list():
    #     print(title)

if __name__ == "__main__":
    #TODO: (bonus) Use sys.argv to get a category name on the command line (but
    #defaulting to DEFAULT_CATEGORY if nothing is passed in)
    main()