from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from teams.models import Team, Player, Photo, LiveScore, BattingAverage, BowlingAverage
from teams.serializers import TeamSerializer, PlayerSerializer, PlayerFormatSearchSerializer, BattingAverageSerializer


class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerList(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TeamPlayersView(generics.ListAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        team_id = self.kwargs['pk']
        return Player.objects.filter(teams__id=team_id)


class BattingAverageList(ListAPIView):
    queryset = BattingAverage.objects.all()
    serializer_class = BattingAverageSerializer


class PlayersFormatWiseView(APIView):

    def get(self, request, format=None):
        serializer = PlayerFormatSearchSerializer(data={}, context={'search': request.query_params})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlayerFormatSearchSerializer(data={}, context={'search': request.query_params})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
