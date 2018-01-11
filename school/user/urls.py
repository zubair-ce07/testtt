from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^users/$',
        views.UserList.as_view(),
        name='user-create'
    ),
    url(
        r'^group/(?P<group_id>[0-9]+)/users/$',
        views.UserList.as_view(),
        name='user-list'
    ),
    url(
        r'^users/(?P<user_id>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-update'
    ),
    url(
        r'^users/(?P<user_id>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'
    ),
]
