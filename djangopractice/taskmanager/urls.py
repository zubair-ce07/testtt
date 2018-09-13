from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_view
from django.urls import path

from taskmanager import views

app_name = 'taskmanager'
urlpatterns = [
    path('login/', auth_view.login, {'redirect_authenticated_user' : True} , name='login'),
    path('', views.Index.as_view(), name='index'),
    path('error/', views.generic.TemplateView.as_view(template_name='taskmanager/error.html'), name='profile_error'),
    path('<int:pk>/status/', views.change_status, name='status'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:pk>/profile/', views.EditProfile.as_view(), name='profile'),
    path('<int:pk>/details', views.TaskDetails.as_view(), name='details'),
    path('<int:pk>/edit/', views.EditTask.as_view(), name='edit'),
    path('addtask/', views.AddTask.as_view(), name='add'),
]

urlpatterns += [
    path('taskmanager/validate_signup/', views.validate_username, name='validate_username'),
    path('<int:pk>/deletetask', views.delete_task, name='delete_task')
]

urlpatterns += staticfiles_urlpatterns()