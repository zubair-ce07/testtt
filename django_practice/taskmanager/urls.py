from django.urls import path
from . import views

urlpatterns = [
    path("", views.redirect_task_index, name="redirect_task_index"),
    path("tasks/", views.task_index, name="task_index"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/task/", views.create_task, name="create_task"),
    path("tasks/task/<int:pk>/edit", views.edit_task, name="edit_task"),
    path("tasks/task/<int:pk>/", views.delete_task, name="delete_task"),
]
