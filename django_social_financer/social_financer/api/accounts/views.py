from rest_framework.views import APIView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes, api_view

from . import serializers
from api.renderers import UserJSONRenderer
from accounts.models import UserProfile, PairHistory
from accounts import constants, helpers, permissions as local_permissions


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    serializer_class = serializers.SignUpSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, format='json'):
        print(request.data.get('body', ''))
        serializer = serializers.SignUpSerializer(data=request.data.get('body', ''))
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
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isDonor)

    def post(self, request, *args, **kwargs):
        pair_id = int(request.data.get('pair_id', -1))
        pair_user = get_object_or_404(UserProfile, pk=pair_id)
        pair_user.pair = request.user.userprofile
        pair_user.save()
        new_pair_history = PairHistory(donor=request.user.userprofile,
                                       consumer=pair_user,
                                       was_paired=True)
        new_pair_history.save()
        return Response({'detail' : 'Successful'}, status.HTTP_200_OK)


class PairedConsumersList(generics.ListAPIView):
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isDonor)

    def get_queryset(self):
        return self.request.user.userprofile.pairs.all()


class HomeConsumer(generics.ListAPIView):
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isConsumer)

    def get_queryset(self):
        print(self.request.user.userprofile.pair.id)
        return UserProfile.objects.filter(pk=self.request.user.userprofile.pair.id)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserProfile.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        print(instance)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

