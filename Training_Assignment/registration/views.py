from django.shortcuts import render
from django.contrib.auth.models import User


def show_profile(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'users/register.html', {'user': user})
