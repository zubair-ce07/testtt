from django.conf.urls import url
from memsapi_app.views import UserListView, UserView, MemoryListView, MemoryView, \
                              ActivityListView, ActivityView, CategoryListView, CategoryView

app_name = 'memoapp'
urlpatterns = [
    url(r'^users/$', UserListView.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', UserView.as_view()),
    url(r'^mems/$', MemoryListView.as_view()),
    url(r'^mem/(?P<pk>[0-9]+)/$', MemoryView.as_view()),
    url(r'^categories/$', CategoryListView.as_view()),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryView.as_view()),
    url(r'^activities/$', ActivityListView.as_view()),
    url(r'^activity/(?P<pk>[0-9]+)/$', ActivityView.as_view())
]