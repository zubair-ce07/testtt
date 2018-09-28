from rest_framework import viewsets, status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.permissions import StaffPermission

from .serializers import BallotSerializer, VoteSerializer
from .models import Ballot, Vote, Choice


class BallotReadView(viewsets.ReadOnlyModelViewSet):
    """
    This viewset provides `profile-data` and allows to `update` it.
    """
    serializer_class = BallotSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Ballot.objects.get_active_ballots()


class BallotView(UpdateAPIView, DestroyAPIView):
    """
    Retrieve Update or Destroy
    """
    serializer_class = BallotSerializer
    permission_classes = (IsAuthenticated, StaffPermission)
    queryset = Ballot.objects.get_active_ballots()


class BallotCreate(CreateAPIView):
    """
    Creates a Ballot
    """
    serializer_class = BallotSerializer
    permission_classes = (IsAuthenticated, StaffPermission)


class BallotVote(APIView):
    """
    Vote a Ballot
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)

        if serializer.is_valid():
            choice = Choice.objects.get(id=serializer.data['choice_id'])
            already_voted = request.user.vote_set.filter(choice__ballot_id=choice.ballot.id)

            if already_voted:
                return Response({"error": "Already voted"}, status=status.HTTP_400_BAD_REQUEST)

            Vote.objects.create(choice=choice, user=self.request.user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
