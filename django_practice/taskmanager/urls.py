from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_index, name="task_index"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("task/", views.create_task, name="create_task"),
    path("task/<int:pk>/edit", views.edit_task, name="edit_task"),
    path("task/<int:pk>/update", views.update_task, name="update_task"),
    path("task/<int:pk>/delete", views.delete_task, name="delete_task"),
]
