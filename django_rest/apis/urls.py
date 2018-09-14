from django.urls import path, include
from .views import AuthenticateUser, RegisterUser


urlpatterns = [
    path('login', AuthenticateUser.as_view()),
    path('register', RegisterUser.as_view()),
    path('blogs/', include('apis.blog.urls')),
]
