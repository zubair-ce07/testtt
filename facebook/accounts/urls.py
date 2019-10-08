from django.contrib.auth.decorators import login_required
from django.urls import path, include

from . import views

urlpatterns = [
    path('signup/', login_required(views.SignupView.as_view()), name='signup'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('', include('django.contrib.auth.urls')),
]
