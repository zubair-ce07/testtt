from django.shortcuts import render, redirect


def index(request):
    if request.user.is_buyer:
        return redirect('/')
    return render(request, 'seller/index.html')
