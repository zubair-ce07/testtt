import tmdbsimple as tmdb
from movies.models import Genre


tmdb.API_KEY = '7b43db1b983b055bffd7534a06cafd6c'


def populate_genres():
    response = tmdb.Genres().list()

    for genre in response['genres']:
        Genre.objects.get_or_create(name=genre['name'], id=genre['id'])


def get_movie(tmdb_id):
    pass
