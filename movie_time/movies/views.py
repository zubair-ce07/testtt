from django.http import HttpResponse
from movies.tasks import get_new_movie
from movies.utils import *


def index(request):
    # populate_genres()
    unavailable_ids = [line.rstrip('\n') for line in open('unavailable_ids.txt')]
    for tmdb_id in range(20001, 50001):
        if str(tmdb_id) not in unavailable_ids:
            get_new_movie.delay(tmdb_id)
    return HttpResponse('OK')
