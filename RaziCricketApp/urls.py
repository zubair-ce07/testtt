"""RaziCricketApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from articles.views import ArticleList, ArticleDetail, SearchResults
from teams.views import TeamList, PlayerList, TeamDetail, PlayerDetail, TeamPlayersView, PlayersInsightsView, \
    BattingAverageList, BowlingAverageList
from users.views import UserList, UserDetail, ProfileList, ProfileDetail

urlpatterns = [
    path('comments/', include('comments.urls')),
    path('teams/', include('teams.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),

    path('profiles/', ProfileList.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('batting_averages/', BattingAverageList.as_view(), name='batting-averages-list'),
    path('bowling_averages/', BowlingAverageList.as_view(), name='bowling-averages-list'),
    path('players/search/', PlayersInsightsView.as_view(), name='players-format'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='player-detail'),
    path('players/', PlayerList.as_view(), name='players-list'),
    path('home/', ArticleList.as_view(), name='articles-list'),
    path('home/search/', SearchResults.as_view(), name='search'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
    path('teams/', TeamList.as_view(), name='teams-list'),
    path('teams/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    path('teams/<int:pk>/players/', TeamPlayersView.as_view(), name='team-players'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
