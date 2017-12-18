from django.conf.urls import url
from watchlists import views


urlpatterns = [
    url(r'^movies/(?P<movie_id>\d+)/watchlist/$', views.add_or_remove_from_watchlist),
    url(r'^movies/(?P<movie_id>\d+)/ratings/(?P<action>\w+)/$', views.rate_movie),
    url(r'^movies/(?P<movie_id>\d+)/(?P<action_type>\w+)/$', views.changed_watchlist_status),
    url(r'^roles/(?P<role_id>\d+)/vote-up/$', views.change_best_actor_vote),
    url(r'^activities/$', views.GetActivities.as_view()),
    url(r'^users/(?P<user_id>\d+)/activities/$', views.GetUserActivities.as_view()),
    url(r'^to-watch/$', views.GetToWatchList.as_view()),
    url(r'^watched/$', views.GetWatchedList.as_view()),
    url(r'^upcoming/$', views.GetUpcomingList.as_view()),
]
