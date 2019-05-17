from django.views.generic.edit import UpdateView, CreateView

from blogs.forms import BlogForm
from blogs.models import Blog


class BlogCreate(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/create_blog.html'


class UpdateBlog(UpdateView):
    model = Blog
    fields = ['blog_title', 'blog_description', 'published_date', 'user_id']
    template_name = 'blogs/edit_blog.html'
