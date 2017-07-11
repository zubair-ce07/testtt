from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import SignUpForm
from instagram.forms import SignUpForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

login_url = reverse_lazy('login')


@login_required(login_url=login_url)
def newsfeed(request):
    user = request.user
    if user.is_authenticated():
        # return HttpResponse('Hi :3')
        return render(request, 'instagram/newsfeed.html', {'user':user, })
    else:
        # return HttpResponse(':3')
        return HttpResponseRedirect(reverse('login'))


def index(request):
    # return HttpResponse('Hi :3')
    return HttpResponseRedirect(reverse('login'))


def logout_view(request):
    messages = []
    # logout(request)
    print(request.user)
    logout(request)
    print(request.user)
    messages.append('User logged out successfully')
    return HttpResponseRedirect(reverse('login'))
    # return render(request, 'instagram/login.html', {'extra_context' : {'messages':messages}})
    # return HttpResponse('Bye :3')


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


@login_required(login_url=login_url)
def profile(request, pk):
    errors = []
    print(pk)
    # print(request.url)
    # if pk in request.GET:
        # print(request.GET)
    if not pk:
        errors.append('ERROR')
        user = None
    else:
        user = User.objects.filter(Q(pk=pk)).first()
        print(user.username)
    return render(request, 'instagram/profile.html',
                      {'errors': errors, 'user':user})
    # return HttpResponse('OOPS! :3')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            # username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=raw_password)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('newsfeed'))
    else:
        form = SignUpForm()
    return render(request, 'instagram/signup.html', {'form': form})
# def login_view(request):
#     return render(request, 'instagram/login.html')
#     # logout(request)
#     print(request.user)
#     logout(request)
#     print(request.user)
#     return HttpResponse('Bye :3')