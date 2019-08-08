from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import BlogsForm
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Blog

def get_and_post_blogs(request):
    if request.method == 'POST':
        form = BlogsForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('blogs_detail')
    elif request.method == 'PUT':
        return redirect('blogs_detail')

    else:
        form = BlogsForm(request.POST)
        username = None
        id = 0
        if request.user.is_authenticated:
            username = request.user.username
            id = request.user.id
        return render(request, 'data.html', {'list': Blog.objects.filter(Q(status = 1) | Q(user_id = request.user.id)), 'form': form, 'name' : username, 'id':id})

def delete(request, id):
    if request.method == 'POST':
        Blog.objects.filter(id=id).delete()
        return redirect('data')

def blog_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('data')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def blog_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})