from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

login = reverse_lazy('login')


@login_required(login_url=login)
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


@login_required(login_url=login)
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
# def login_view(request):
#     return render(request, 'instagram/login.html')
#     # logout(request)
#     print(request.user)
#     logout(request)
#     print(request.user)
#     return HttpResponse('Bye :3')