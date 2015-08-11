from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from web.posts.views.all_posts import AllPostsView
from web.posts.views.my_posts import MyPostsView
from web.posts.views.my_requests import MyRequestsView
from web.posts.views.new_post import NewPostView
from web.users.views.account import AccountView
from web.users.views.login import LogInView
from web.users.views.sign_up import SignUpView


urlpatterns = [
    url(r'^new-post/$', login_required(NewPostView.as_view()), name='new_post'),
    url(r'^my-requests/$', login_required(MyRequestsView.as_view()), name='my_requests'),
    url(r'^my-posts/$', login_required(MyPostsView.as_view()), name='my_posts'),
    url(r'^all/$', login_required(AllPostsView.as_view()), name='all_posts'),
    ]