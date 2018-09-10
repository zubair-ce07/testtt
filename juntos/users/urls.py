from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('', login_required(views.IndexDetailView.as_view()), name='index'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view()), name='logout'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('update/profile/', login_required(views.ProfileUpdate.as_view()), name='edit_profile'),
    path('update/user/', login_required(views.UserUpdate.as_view()), name='edit_basic_info'),
    path('update/user/complete', views.update_profile, name='edit_all_info'),
]
