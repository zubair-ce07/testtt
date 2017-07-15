from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import SignUpForm
from instagram.forms import SignUpForm, LoginForm
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
from django.db.models import Q
from instagram.models import User # Profile, Comment, Like, Post

login_url = reverse_lazy('login')


@login_required(login_url=login_url)
def newsfeed(request):
    user = request.user
    print('User: ', user)
    if user.is_authenticated():
        # followers = User.all_followers.get_queryset(user.username).all()
        # following =
        followers, following = get_followers_and_following(user)
        print(followers, following)
        # following = User.objects.filter(user__username=user.username).values('following__user__username')
        return render(request, 'instagram/newsfeed.html',
                      {'user': user, 'followers': followers,
                       'following': following,})
    else:
        return HttpResponseRedirect(reverse('login'))


def get_followers_and_following(user):
    # no_following = False
    followers = User.all_followers.get_queryset(user.username).all()
    following = User.all_following.filter(username=user.username)
    # print('hey', User.objects.none())
    for followee in following:
        if followee['following'] is None:
            # no_following = True
            following = User.objects.none()
            # following.count = 0
            break
    # if no_following:
    #     return followers,
    # else:
    return followers, following


def index(request):
    return HttpResponseRedirect('login')
    # return HttpResponse('Hi :3')


def logout(request):
    messages = []
    # logout(request)
    print('Logout: ', request.user)
    auth_logout(request)
    print('Logout: ', request.user)
    messages.append('User logged out successfully')
    return HttpResponseRedirect(reverse('login'))
    # return render(request, 'instagram/login.html', {'extra_context' : {'messages':messages}})
    # return HttpResponse('Bye :3')
#
#
@login_required(login_url=login_url)
def search(request):
    errors = []
    if 'query' in request.GET:
        query = request.GET['query']
        if not query:
            errors.append('Enter a search term')
            # return render(request, 'instagram/search_form.html',
            # {'error': error})
        elif len(query) > 20:
            errors.append('Please enter at most 20 characters')
        else:
            users = User.objects.filter(Q(username__icontains=query) |
                                        Q(first_name__icontains=query) |
                                        Q(last_name__icontains=query))
            return render(request, 'instagram/search_results.html',
                          {'users': users, 'query': query})
    return render(request, 'instagram/search_form.html',
                  {'errors': errors})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('newsfeed'))
    form = LoginForm()
    return render(request, 'instagram/login.html', {'form': form,})

#
#
@login_required(login_url=login_url)
def profile(request, pk):
    errors = []
    print('Profile: ', pk)
    # followers = []
    # following = []
    # print(request.url)
    # if pk in request.GET:
    # print(request.GET)
    if not pk:
        errors.append('ERROR')
        profile_owner = None
        logged_in_profile = None
    else:
        profile_owner = get_object_or_404(User, pk=pk)
        user = request.user
            # User.objects.filter(Q(pk=pk)).first()
        already_followed = False

        # followers = User.objects.filter('followed_by')
        # print('Profile: ', user.username)
        logged_in_profile = profile_owner.username == user.username
        if logged_in_profile:
            followers, following = get_followers_and_following(user)
        else:
            followers, following = get_followers_and_following(profile_owner)
        # followers = Profile.objects.filter(following__user__username=user.username)
        print('FOLLOWERS', len(followers), followers)
        print('FOLLOWING', following)
        # following = Profile.objects.filter(user__username=user.username).values('following__user__username')
        # following = Profile.objects.filter(profile__user__username=user.username).values('following')
        for followee in following:
            if followee['following'] == profile_owner.pk:
                already_followed = True
                print('ALREADY FOLLOWING :3')
                break

        # already_followed = request.user in followers
    return render(request, 'instagram/profile.html',
                  {'errors': errors,
                   'user': profile_owner,
                   'logged_in_profile': logged_in_profile,
                   'already_followed': already_followed,
                   'following': following,
                   'followers': followers,
                   })
    # return HttpResponse('OOPS! :3')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.bio = form.cleaned_data.get('bio')
            user.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # username = form.cleaned_data.get('username')
            # user = authenticate(username=username, password=raw_password)
            print('Signup: ', user)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('newsfeed'))
    else:
        form = SignUpForm()
    return render(request, 'instagram/signup.html', {'form': form})


@login_required(login_url=login_url)
def follow_profile(request, pk):
    errors = []
    user = request.user
    to_follow = get_object_or_404(User, pk=pk)
    print('found:', to_follow)
    user.following.add(to_follow)
    user.save()
    # print(user.profile.following)
    to_follow.refresh_from_db()
    followers, following = get_followers_and_following(to_follow)
    # followers = Profile.objects.filter(following__user__username=to_follow.user.username)
    print('FOLLOWERS', len(followers), followers)
    # following = Profile.objects.filter(user__username=to_follow.user.username).values('following__user__username')
    # following = Profile.objects.filter(profile__user__username=user.username).values('following')
    # already_followed = True
    # for followee in following:
    #     if followee['following__user__username'] == to_follow.username:
    #         already_followed = True
    #         print('ALREADY FOLLOWING :3')
    #         break

            # already_followed = request.user in followers
    return render(request, 'instagram/profile.html',
                  {'errors': errors,
                   'user': to_follow,
                   'logged_in_profile': False,
                   'already_followed': True,
                   'following': following,
                   'followers': followers,
                   })


@login_required(login_url=login_url)
def unfollow_profile(request, pk):
    errors = []
    user = request.user
    to_unfollow = get_object_or_404(User, pk=pk)
    print('found:', to_unfollow)
    user.following.remove(to_unfollow)
    user.save()
    # print(user.profile.following)
    to_unfollow.refresh_from_db()
    followers, following = get_followers_and_following(to_unfollow)
    # followers = Profile.objects.filter(following__user__username=to_unfollow.user.username)
    print('FOLLOWERS', len(followers), followers)
    # following = Profile.objects.filter(user__username=to_unfollow.user.username).values('following__user__username')
    return render(request, 'instagram/profile.html',
                  {'errors': errors,
                   'user': to_unfollow,
                   'logged_in_profile': False,
                   'already_followed': False,
                   'following': following,
                   'followers': followers,
                   })


@login_required(login_url=login_url)
def show_followers(request, pk):
    user = request.user
    target_profile = get_object_or_404(User, pk=pk)
    followers, following = get_followers_and_following(target_profile)
    return render(request, 'instagram/show_followers.html',
                        {'followers': followers})


@login_required(login_url=login_url)
def show_following(request, pk):
    # print('\n\n\n\n\n\n', len(pk))
    user = request.user
    target_profile = get_object_or_404(User, pk=pk)
    followers, following = get_followers_and_following(target_profile)
    following = get_user_objects(following, 'following')
    print(following)
    return render(request, 'instagram/show_followers.html',
                        {'followers': following})


def get_user_objects(query_set, key):
    users = []
    for item in query_set:
        try:
            user = get_object_or_404(User, pk=int(item[key]))
            users.append(user)
        except KeyError:
            print('ERROR')
    return users