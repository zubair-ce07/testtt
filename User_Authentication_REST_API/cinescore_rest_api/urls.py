from django.conf.urls import url

from . import views


app_name = "cinescore"

urlpatterns = [
    url(r'^user/$', views.UserList.as_view(), name='user'),
    url(r'^movies/$', views.MovieListView.as_view(), name='movie'),
    url(r'^rate_movie/$', views.RateMovieView.as_view(), name='movie'),
    url(r'^fav_movie/$', views.FavoriteMoviesView.as_view(), name='movie'),
]
