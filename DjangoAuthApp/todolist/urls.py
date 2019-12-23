
from django.urls import path
from . import views

urlpatterns = [
    path('todoList/', views.TodoListView.as_view(), name='todoList'),
    path('todoList/<pk>/', views.TodoListEdit.as_view(), name='todoListEdit'),
    path('todoList/<pk>/delete/', views.TodoListDelete.as_view(), name='todoListDelete'),
]
