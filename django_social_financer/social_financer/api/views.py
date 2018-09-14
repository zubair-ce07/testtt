from rest_framework.views import APIView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes, api_view

from . import serializers
from .renderers import UserJSONRenderer
from accounts.models import UserProfile, PairHistory, Category
from accounts import constants, helpers, permissions as local_permissions
from feedback.models import Feedback


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Account Views


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
        redirect(reverse('accounts:my_consumers'))
        # Return 200 Status Code


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


class ProfileView(generics.ListAPIView):
    serializer_class = serializers.UserProfileModelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        print(self.request.query_params.get('id',-1))
        return UserProfile.objects.filter(pk=self.request.user.id)


class FeedbackView(generics.ListAPIView):
    serializer_class = serializers.FeedbackModelSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        return Feedback.objects.filter(given_to_user=self.request.query_params.get('id', -1))

#Feedback views


class PostFeedbackView(APIView):
    serializer_class = serializers.FeedbackModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isPair)

    def post(self, request, pk, format='json',):
        pair_user = get_object_or_404(UserProfile, pk=pk)
        self.check_object_permissions(request, pair_user)
        serializer = serializers.FeedbackModelSerializer(instance=pair_user,
                                             data=request.data,
                                             context={'by_user' : request.user.id})
        if serializer.is_valid():
            feedback = serializer.save()
            return redirect(reverse('accounts:home')) if feedback else Http404


class GetFeedbackView(generics.ListAPIView):
    serializer_class = serializers.FeedbackModelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Feedback.objects.filter(given_to_user=self.request.query_params.get('id', -1))

# Report Views


class PostReportView(APIView):
    serializer_class = serializers.ReportModelSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isPair)

    def post(self, request, format='json'):
        pair_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        serializer = serializers.ReportModelSerializer(instance=pair_user,
                                           data=request.data,
                                           context={'by_user': self.request.user.id})
        if serializer.is_valid():
            report = serializer.save()
            return redirect(pair_user.role) if report else Http404

    def get_reverse_url(self, role):
        return 'accounts:my_consumers' if role == 'DN' else 'accounts:home'


class ViewReports(APIView):
    serializer_class = serializers.ViewReportsSerializer
    permission_classes = (permissions.IsAuthenticated, local_permissions.isAdmin)
    def get(self, request, pk):
        serializer = serializers.ViewReportsSerializer(instance=request.user.userprofile)
        return Response(serializer.data)

# Category


class GetCategories(generics.ListAPIView):
    serializer_class = serializers.GetCategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
