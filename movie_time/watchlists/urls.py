from django.conf.urls import url
from watchlists import views


urlpatterns = [
    url(r'movies/(?P<movie_id>\d+)/watchlist/$', views.add_or_remove_from_watchlist),
    url(r'roles/(?P<role_id>\d+)/vote-up/$', views.change_best_actor_vote),
    url(r'activities/$', views.get_activities)

]
