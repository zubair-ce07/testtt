from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from malfunction_reporting import views

app_name = 'malfunction_reporting'

urlpatterns = [
    url(r'^$', login_required(views.Index.as_view()), name='index'),
    url(r'^tasks/$', login_required(views.list_tasks), name='list_tasks'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', login_required(views.TaskDetail.as_view()), name='task_detail'),
    url(r'^dashboard/$', login_required(views.dashboard), name='dashboard'),
    url(r'^movies/$', login_required(views.show_movies), name='movies'),
    url(r'^investigations/$', login_required(views.show_all_investigations), name='investigations'),
]
