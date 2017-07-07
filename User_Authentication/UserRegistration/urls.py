from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = "users"

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^signup$', views.SignUpView.as_view(), name='signup'),
    url(r'^profiles$', views.ProfileView.as_view(), name='profile'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^update', views.UpdateProfileView.as_view(), name='update'),
    url(r'^change_password', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^tasks', views.TasksView.as_view(), name='tasks'),
    url(r'^delete_task', views.DeleteTaskView.as_view(), name='delete_task'),
    url(r'^edit_task', views.UpdateTaskView.as_view(), name='edit_task'),
    url(r'^show_all_task', views.ShowAllTasksView.as_view(), name='show_all_task'),
    url(r'^add_task', login_required(views.AddNewTaskView.as_view()), name='add_task'),
    url(r'^add_user_task', login_required(views.AddUserTaskView.as_view()), name='add_user_task'),
]