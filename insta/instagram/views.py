from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def newsfeed(request):
    user = request.user
    # username = request.POST.get('username')
    # print(username)
    # password = request.POST.get('password')
    # user = authenticate(username=username, password=password)

    if user.is_authenticated():
        # if user.is_active:
            # login(request, user)
        print('HUEHUE')
        return HttpResponse('Hi :3')
    else:
        # print(username, password)
        return HttpResponseRedirect('/login')


def index(request):
    return HttpResponseRedirect('login')


def logout_view(request):
    logout(request)

