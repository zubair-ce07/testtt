from django.urls import path
from django.contrib.auth import views as auth_view

from taskmanager import views

app_name = 'taskmanager'
urlpatterns = [
    path('login/', auth_view.login, {'redirect_authenticated_user' : True} , name='login'),
    path('', views.Index.as_view(), name='index'),
    path('<int:pk>/status/', views.change_status, name='status'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:pk>/profile/', views.EditProfile.as_view(), name='profile'),
    path('<int:pk>/details', views.TaskDetails.as_view(), name='details'),
    path('<int:pk>/edit/', views.EditTask.as_view(), name='edit'),
    path('<int:pk>/deletetask/', views.DeleteTask.as_view(), name='delete'),
    path('addtask/', views.AddTask.as_view(), name='add'),
]