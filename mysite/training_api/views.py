# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import Http404
from django.contrib.auth.models import User

from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from training.models import (
    Trainee, Trainer, UserProfile,
    Assignment, Technology
)
from training.signals import add_trainee_signal, add_trainer_signal
from .serializers import (
    UserSerializer, UserProfileSerializer,
    TraineeSerializer, TrainerSerializer,
    AssignmentSerializer,
    TechnologySerializer
)


class TrainerSignUp(generics.CreateAPIView):
    """
    Signs up Trainer and assigns a token
    """
    queryset = Trainer.objects.all()

    def create(self, request, *args, **kwargs):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        try:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name)
        except User:
            raise Http404("Username already exists")

        user.set_password(password)
        user.save()

        add_trainer_signal.send(sender=self.__class__, user=user)
        serializer = UserSerializer(user)

        return Response(serializer.data)


class TraineeSignUp(generics.CreateAPIView):
    """
    Signs up Trainee, assigns a token and a trainer as well
    """
    queryset = Trainee.objects.all()

    def create(self, request, *args, **kwargs):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        try:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name)
        except:
            raise Http404("Username already exists")

        user.set_password(password)
        user.save()

        add_trainee_signal.send(sender=self.__class__, user=user)
        serializer = UserSerializer(user)

        return Response(serializer.data)


class Profile(APIView):
    """
    Displays the profile of the user logged in
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)


class Search(generics.ListAPIView):
    """
    Searches for trainers/trainees
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    model = UserProfile
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        try:
            return UserProfile.objects.filter(
                name__contains=self.request.GET.get('q'))
        except:
            raise Http404("Query not given to search")


class TrainerAssigned(generics.RetrieveAPIView):
    """
    Displays the trainer assigned to the logged in trainee
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    def get_object(self):
        try:
            return self.request.user.trainee.trainer
        except:
            raise Http404("Logged in as a Trainer")


class TraineesAssigned(generics.ListAPIView):
    """
    Displays the trainees assigned to the logged in trainer
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = TraineeSerializer

    def get_queryset(self):
        try:
            return self.request.user.trainer.trainees
        except:
            raise Http404("Logged in as a Trainee")


class AssignmentsAssigned(generics.ListAPIView):
    """
    displays the assignments assigned to the logged trainee
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        try:
            return self.request.user.trainee.assignments
        except:
            raise Http404("Logged in as a Trainer")


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows assignments to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    """
    returns the technologies used by the selected assignment
    """
    @detail_route(methods=['get'])
    def technologies(self, request, pk):
        try:
            assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404("Assignment doesn't exist")

        serializer = TechnologySerializer(assignment.technology_used.all(),
                                          many=True)

        return Response(serializer.data)


class TrainerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that only allows viewing trainers
    and trainees assigned to them
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    """
    returns the trainees assigned to the selected trainer
    """
    @detail_route(methods=['get'])
    def trainees(self, request, pk):
        try:
            trainer = Trainer.objects.get(pk=pk)
        except Trainer.DoesNotExist:
            raise Http404("Trainer doesn't exist")

        serializer = TraineeSerializer(trainer.trainees.all(), many=True)

        return Response(serializer.data)


class TraineeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that only allows viewing trainees
    and the assigned trainers
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer

    """
    returns the trainer assigned to the selected trainee
    """
    @detail_route(methods=['get'])
    def trainer(self, request, pk):
        try:
            trainee = Trainee.objects.get(pk=pk)
        except Trainee.DoesNotExist:
            raise Http404("Trainee doesn't exist")

        serializer = TrainerSerializer(trainee.trainer)

        return Response(serializer.data)

    @detail_route(methods=['get'])
    def assignments(self, request, pk):
        try:
            trainee = Trainee.objects.get(pk=pk)
        except Trainee.DoesNotExist:
            raise Http404("Trainee doesn't exist")

        serializer = AssignmentSerializer(trainee.assignments, many=True)

        return Response(serializer.data)


class TechnologyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows technology to be viewed or edited
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
