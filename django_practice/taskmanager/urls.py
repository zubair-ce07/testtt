from __future__ import absolute_import

from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers
from taskmanager import views

router = routers.DefaultRouter()
router.register(prefix='tasks', viewset=views.TasksAPIViewSet, basename='tasks')
router.register(prefix='users', viewset=views.UsersAPIViewSet, basename='users')

urlpatterns = [
    path("", views.redirect_task_index, name="redirect_task_index"),
    path("tasks/", views.task_index, name="task_index"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("user/<int:pk>/", views.user_detail, name="user_detail"),
    path("user/<int:pk>/edit/", views.edit_user, name="edit_user"),
    path("user/<int:pk>/password_change/", auth_views.PasswordChangeView.as_view(), name='password_change', ),
    path("tasks/task/", views.create_task, name="create_task"),
    path("tasks/<int:pk>/edit/", views.edit_task, name="edit_task"),
    path("tasks/<int:pk>/delete/", views.delete_task, name="delete_task"),
    path('register/', views.register, name="register" ),
    path('api/', include(router.urls))
]
