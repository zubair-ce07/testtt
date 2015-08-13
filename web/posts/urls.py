from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from web.posts.views.accept_request import AcceptRequestView

from web.posts.views.all_posts import AllPostsView
from web.posts.views.file_upload import FileUploadView, my_post
from web.posts.views.my_post_details import MyPostDetailsView
from web.posts.views.my_posts import MyPostsView
from web.posts.views.my_requests import MyRequestsView
from web.posts.views.new_post import NewPostView
from web.posts.views.new_request import NewRequestView
from web.posts.views.post_details import PostDetailsView
from web.posts.views.reject_request import RejectRequestView


urlpatterns = [
    url(r'^new/$', login_required(NewPostView.as_view()), name='new_post'),
    url(r'^my-requests/$', login_required(MyRequestsView.as_view()), name='my_requests'),
    url(r'^my-posts/$', login_required(MyPostsView.as_view()), name='my_posts'),
    url(r'^all/$', login_required(AllPostsView.as_view()), name='all_posts'),
    url(r'^(?P<post_id>\d+)/$', login_required(PostDetailsView.as_view()), name='post_details'),
    url(r'^(?P<post_id>\d+)/request/$', login_required(NewRequestView.as_view()), name='new_request'),
    url(r'^my-post/(?P<post_id>\d+)/$', login_required(MyPostDetailsView.as_view()), name='my_post_details'),
    url(r'^(?P<post_id>\d+)/request/(?P<request_id>\d+)/accept/$', login_required(AcceptRequestView.as_view()),
        name='accept_request'),
    url(r'^post/(?P<post_id>\d+)/request/(?P<request_id>\d+)/reject/$', login_required(RejectRequestView.as_view()),
        name='reject_request'),
    url(r'^upload/$', my_post, name='file_upload')
]