from django.urls import path

from . import views

urlpatterns = [
    path('teams/', views.index, name='teams_index'),
    path('players/', views.index, name='players_index'),
]
