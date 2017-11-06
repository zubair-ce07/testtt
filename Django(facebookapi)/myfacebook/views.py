import datetime

from django.contrib.auth import (
    authenticate, login as django_login,
    logout as django_logout
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.authentication import TokenAuthentication

from .forms import StatusForm, UserCreationForm
from .models import UserStatus, UserFollowers, News
from .serializers import NewsSerializer


class SignIn(View):
    template_name = 'myfacebook/signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('myfacebook:profile')

        form = AuthenticationForm(None)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        message = ''
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                return redirect('myfacebook:profile')

            message += 'SignIn failed'
        context = {
            'error': message,
            'form': form
        }
        return render(request, self.template_name, context)


class Signup(View):
    template_name = 'myfacebook/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('myfacebook:profile')

        context = {
            'form': UserCreationForm(None)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        message = ''
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                return redirect('myfacebook:profile')
            else:
                message += '\nSignIn failed'

        context = {
            'form': form,
            'error': message
        }
        return render(request, self.template_name, context)


class Logout(View):
    def get(self, request):
        django_logout(request)
        return redirect('myfacebook:signin')


class Profile(View):
    template_name = 'myfacebook/profile.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            statuses = UserStatus.objects.filter(status_author=user).order_by('-pub_date')
            context = {
                'user': user,
                'statuses': statuses,
                'form': StatusForm(None)
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')

    def post(self, request):
        user = request.user
        form = StatusForm(request.POST)
        if form.is_valid():
            status = UserStatus(status_text=form.cleaned_data['status'],
                                status_author=user,
                                pub_date=datetime.datetime.now())
            status.save()
            return redirect('myfacebook:profile')

        context = {
            'form': StatusForm(None),
            'user': user,
            'message': 'status is invalid',
        }
        return render(request, self.template_name, context)


class FindPeople(View):
    template_name = 'myfacebook/find.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            users = User.objects.exclude(Q(id=user.id) | Q(is_superuser=1))
            context = {
                'users': users
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')


class UserDetails(View):
    template_name = 'myfacebook/detail.html'

    def get(self, request, user_id):
        current_user = request.user
        if current_user.is_authenticated:
            if int(user_id) == current_user.id:
                return redirect('myfacebook:profile')

            try:
                user = User.objects.get(id=user_id)
            except ObjectDoesNotExist:
                return redirect('myfacebook:profile')

            statuses = UserStatus.objects.filter(status_author=user).order_by('-pub_date')
            is_following = UserFollowers.objects.filter(followee=user, follower=current_user).count()
            context = {
                'user': user,
                'statuses': statuses,
                'is_following': is_following
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')


def follow(request, user_id):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return redirect('myfacebook:profile')

        user_follow = UserFollowers(followee=user, follower=current_user)
        user_follow.save()
        return redirect('myfacebook:detail', user_id)

    return redirect('myfacebook:signin')


class HomePage(View):
    template_name = 'myfacebook/home.html'

    def get(self, request):
        current_user = request.user
        if current_user.is_authenticated:
            followings = UserFollowers.objects.filter(follower=current_user)
            statuses = []
            for following in followings:
                statuses += UserStatus.objects.filter(status_author=following.followee)
            statuses = sorted(statuses, key=lambda status: status.pub_date, reverse=True)
            context = {
                'statuses': statuses
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')


class NewsFeed(View):
    template_name = 'myfacebook/news.html'

    def get(self, request):
        latest_news = News.objects.only('id', 'title')

        context = {
            'latest_news': latest_news
        }
        return render(request, self.template_name, context)


class NewsDetail(View):
    template_name = 'myfacebook/news_detail.html'

    def get(self, request, news_id):
        try:
            news = News.objects.get(id=news_id)
        except ObjectDoesNotExist:
            return redirect('myfacebook:latest')

        context = {
            'news': news
        }
        return render(request, self.template_name, context)


class NewsListAPI(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        news = {
            'author_id': request.user.id, 'title': request.data['title'],
            'description': request.data['description'], 'detail': request.data['detail'],
            'link': request.data['link'], 'image_url': request.data['image_url'],
            'date': request.data['date']
        }

        news_serializer = NewsSerializer(data=news)

        if news_serializer.is_valid():
            news_serializer.save()
            return JsonResponse(news_serializer.data)

        return HttpResponse([news_serializer.errors], status=status.HTTP_400_BAD_REQUEST)


class NewsDetailAPI(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @detail_route(methods=['get'])
    def user_news(self, request, pk):
        news = News.objects.filter(author_id=pk)
        news_serializer = NewsSerializer(news.all(), many=True)
        return Response(news_serializer.data)
