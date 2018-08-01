from django.urls import path

from taskmanager import views

app_name = 'taskmanager'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<int:pk>/edit/', views.EditTask.as_view(), name='edit'),
    path('<int:pk>/deletetask/', views.DeleteTask.as_view(), name='delete'),
    path('addtask/', views.AddTask.as_view(), name='add'),

]