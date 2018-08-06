from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from teams.models import Team, Player, Photo, LiveScore
from teams.serializers import TeamSerializer, PlayerSerializer, PlayerInsightsSearchSerializer


class TeamList(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerList(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TeamDetail(RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TeamPlayersView(ListAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        team_id = self.kwargs['pk']
        queryset = Player.objects.filter(teams__id=team_id)
        player_format = self.request.query_params.get('formats', None)
        if player_format is not None:
            queryset = queryset.filter(batting_averages__format__iexact=player_format).order_by('id')
        return queryset


class PlayersInsightsView(APIView):

    def get(self, request, format=None):
        serializer = PlayerInsightsSearchSerializer(data={}, context={'search': request.query_params})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlayerInsightsSearchSerializer(data={}, context={'search': request.query_params})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
