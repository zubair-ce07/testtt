from django.urls import path

from teams.views import PlayerList, PlayerDetail, PlayersInsightsView, TeamList, TeamDetail, TeamPlayersView

urlpatterns = [
    path('players/', PlayerList.as_view(), name='players-list'),
    path('players/search/', PlayersInsightsView.as_view(), name='players-format'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='player-detail'),
    path('teams/', TeamList.as_view(), name='teams-list'),
    path('teams/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    path('teams/<int:pk>/players/', TeamPlayersView.as_view(), name='team-players'),
]
