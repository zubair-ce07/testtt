from __future__ import absolute_import
from django.urls import path
from taskmanager import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.redirect_task_index, name="redirect_task_index"),
    path("tasks/", views.TaskIndexView.as_view(), name="task_index"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/task/", views.CreateTaskView.as_view(), name="create_task"),
    path("tasks/task/<int:pk>/edit/", views.EditTaskView.as_view(), name="edit_task"),
    path("tasks/task/<int:pk>/", views.DeleteTaskView.as_view(), name="delete_task"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/edit/", views.EditUserView.as_view(), name="edit_user"),
    path("user/<int:pk>/password_change/", auth_views.PasswordChangeView.as_view(), name='password_change', ),
    path('register/', views.register, name="register")
]
