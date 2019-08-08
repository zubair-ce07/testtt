from django.shortcuts import render, redirect


def index(request):
    # Check if user is login
    if not request.user.is_authenticated:
        return redirect('signin')

    return render(request, 'dashboard/index.html')
