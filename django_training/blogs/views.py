from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from blogs.forms import BlogForm
from blogs.models import Blog


def add_new_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user_id = request.user
            blog.published_date = timezone.now()
            blog.save()
            return HttpResponse('<h2>Successfully added. To see click on <a href={}>Home</a></h2>'.format(reverse('home')))
    else:
        form = BlogForm()

    return render(request, 'blogs/create_blog.html', {'form': form})


def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return HttpResponse('<h2>Successfully Updated. To see click on <a href={}>Home</a></h2>'.format(reverse('home')))
    else:
        form = BlogForm(instance=blog)
        return render(request, 'blogs/edit_blog.html', {'form': form})


def delete_blog(request):
    blog_id = request.GET['blog_id']
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return HttpResponse('{} blog is successfully deleted'.format(blog))
