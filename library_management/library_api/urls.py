from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name='lms_api'
urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('book/<int:pk>/', views.BookDetail.as_view()),
    path('accounts/signup/author/', views.AuthorSignup.as_view(),
        name='author_signup'),
    path('accounts/signup/publisher/', views.PubliserSignup.as_view(),
        name='publisher_signup'),
    path('login', obtain_auth_token, name='get_user_auth_token'),
    path('logout/', views.Logout.as_view(), name="log_out"),
]
