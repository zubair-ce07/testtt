from django.urls import path
from . import views



app_name = 'my_user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.UserLoginFormView.as_view(), name='login'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/<int:user_id>', views.UserEditFormView.as_view(), name='edit'),
]