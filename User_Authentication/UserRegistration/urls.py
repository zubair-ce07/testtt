from django.conf.urls import url
from . import views

app_name = "users"

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^signup$', views.SignUpView.as_view(), name='signup'),
    url(r'^profiles$', views.ProfileView.as_view(), name='profile'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^update', views.UpdateProfileView.as_view(), name='update'),
    url(r'^change_password', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^tasks', views.TasksView.as_view(), name='tasks'),
    url(r'^delete_task', views.DeleteTaskView.as_view(), name='delete_task'),
    url(r'^edit_task', views.UpdateTaskView.as_view(), name='edit_task'),
]