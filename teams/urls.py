from django.urls import path

from . import views

urlpatterns = [
    path('teams/', views.team_index, name='teams_index'),
    path('players/', views.player_index, name='players_index'),
]
