from django.http import HttpResponse
from movies.tasks import get_new_movie
from movies.utils import *


def index(request):
    #populate_genres()
    for tmdb_id in range(301, 401):
        get_new_movie.delay(tmdb_id)
    # create_movie(386)
    return HttpResponse('OK')
