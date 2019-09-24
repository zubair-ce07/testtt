from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import SignUpView, ProfileView, CartView


urlpatterns = [
    url(r'^signup/', SignUpView.as_view(), name="sign_up"),
    url(r'^login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^logout', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
    url(r'^profile/', login_required(ProfileView.as_view()), name="profile"),
    url(r'^cart/', CartView.as_view(), name='view-cart')
]
