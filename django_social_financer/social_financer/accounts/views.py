from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from .models import UserProfile, PairHistory
from . import constants, helpers, serializers, permissions as local_permissions


class SignUpView(APIView):
    serializer_class = serializers.SignUpSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, format='json'):
        serializer = serializers.SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return HttpResponseRedirect(reverse_lazy('accounts:home')) if user else Http404

@api_view(['GET'])
@login_required()
def home_view(request):
    role = request.user.userprofile.role
    if role == UserProfile.DONOR:
        return redirect(reverse('accounts:consumers_list'))
    elif role == UserProfile.CONSUMER:
        return redirect(reverse('accounts:home_consumer'))
    elif request.user.is_staff:
        return redirect(request.build_absolute_uri() + 'admin/')
    return HttpResponse("Home l{}l".format(role))


class UnpairedConsumersList(generics.ListAPIView):
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isDonor)

    def get_queryset(self):
        consumers = UserProfile.objects.filter(
            city=self.request.user.userprofile.city.lower(),
            country=self.request.user.userprofile.country.lower(),
            role=UserProfile.CONSUMER)
        consumers = consumers.exclude(id=self.request.user.userprofile.id)
        return consumers.exclude(id__in=self.request.user.userprofile.pairs.values('id'))


class ConsumerDetail(APIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isDonor)

    def get(self, request, *args, **kwargs):
        serializer = serializers.UserDetailSerializer(instance=User.objects.get(id=kwargs['pk']))
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pair_id = int(kwargs.get('pair_id', -1))
        pair_user = get_object_or_404(UserProfile, pk=pair_id)
        pair_user.pair = request.user.userprofile
        pair_user.save()
        new_pair_history = PairHistory(donor=request.user.userprofile,
                                       consumer=pair_user,
                                       was_paired=True)
        new_pair_history.save()
        redirect(reverse('accounts:my_consumers'))


class PairedConsumersList(generics.ListAPIView):
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isDonor)

    def get_queryset(self):
        return self.request.user.userprofile.pairs.all()


class HomeConsumer(APIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isConsumer)

    def get(self, request, *args, **kwargs):
        serializer = serializers.UserDetailSerializer(instance=request.user.userprofile.pair.user)
        return Response(serializer.data)


class ProfileView(APIView):
    serializer_class = serializers.ProfileViewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = serializers.ProfileViewSerializer(instance=self.request.user)
        return Response(serializer.data)
