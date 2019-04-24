from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import BlogsForm
from django.db.models import Q

from django.shortcuts import render, redirect
from django.http import HttpResponse


from .models import Blog

def get_and_post_blogs(request):
    if request.method == 'POST':
        # if request.POST.get("form_type") == 'formOne':
        #     return redirect('data')
        # elif request.POST.get("form_type") == 'abc':
        form = BlogsForm(request.POST)
        if form.is_valid():
            form.save(request)
            #Contents.objects.filter(id=4).update(blog_text="aaaaaaaaaaaaaaaaaaaaaaaaaaaaa") [editing]
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
            #Contents.objects.filter(status = 1 , user_id= request.user.username)
            #Contents.objects.all()
        return render(request, 'data.html', {'list': Blog.objects.filter(Q(status = 1) | Q(user_id = request.user.id)), 'form': form, 'name' : username, 'id':id})
        #return render(request, 'data.html',{'list': Contents.objects.filter(Q(status=1) | Q(user_id=request.user.id)),'name': username})


def delete(request, id):
    #item.id as delete_url
    if request.method == 'POST':
        Blog.objects.filter(id=id).delete()
        return redirect('data')

def edit(request, id):
    #item.id as delete_url
    return render(request, 'data.html')
    # if request.method == 'POST':
    #     Contents.objects.filter(id=id).delete()
    #     return redirect('data')

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