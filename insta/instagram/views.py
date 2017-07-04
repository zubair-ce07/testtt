from django.http import HttpResponse
from django.contrib.auth import authenticate, login


def index(request):
    # def my_view(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, password=password)
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         # Redirect to a success page.
    #     else:
    #         # Return a 'disabled account' error message
    #         return HttpResponse("Error: Disabled Account")
    # else:
    #     # Return an 'invalid login' error message.
    #     return HttpResponse("Error: Invalid Login")
    return HttpResponse("Hello, world. You're at the Instagram index.")


# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user:
#         login(request, user)
#     else:
#         return