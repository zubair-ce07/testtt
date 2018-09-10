from django.urls import path, reverse
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'my_user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.UserLoginFormView.as_view(), name='login'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', login_required(views.UserEditFormView.as_view(), login_url='/login'),
         name='edit'),
    path('change-password/', login_required(views.UserEditPassword.as_view(), login_url='/login'),
         name='change_password'),
]
