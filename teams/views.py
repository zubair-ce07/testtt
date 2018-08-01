from django.shortcuts import render
from django.http import HttpResponse
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import generics

from common.pagination import LimitPagination
from teams.models import Team, Player, Photo, LiveScore
from teams.serializers import TeamSerializer, PlayerSerializer


def team_index(request):
    return HttpResponse("Hello, world. You're at the teams index.")


def player_index(request):
    return HttpResponse("Hello, world. You're at the player index.")


class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerList(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
