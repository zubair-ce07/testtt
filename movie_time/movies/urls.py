from django.conf.urls import url
from movies.views import *


urlpatterns = [
    url(r'movies/(?P<pk>\d+)/$', get_movie, name='movie-detail'),
    url(r'movies/released-on/$', GetMoviesReleasedOnDate.as_view()),
    url(r'search/$', search_movies),
    url(r'genres/$', GetGenres.as_view()),
    url(r'genres/(?P<pk>\d+)/movies/', GetGenresMovies.as_view())
]
