
from django.urls import include, path

from users import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/author/',
         views.AuthorSignup.as_view(),
         name='author_signup'),
    path('accounts/signup/publisher/',
         views.PubliserSignup.as_view(),
         name='publisher_signup'),
    path('login', views.LogIn.as_view(), name='get_user_auth_token'),
    path('logout/', views.Logout.as_view(), name="log_out"),
]
