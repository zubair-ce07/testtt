from django.urls import path, re_path
from django.views.generic.edit import CreateView
from freelancers.forms.registration_form import RegistrationForm
from freelancers.views.list import ListView
from freelancers.views.detail import DetailView
from freelancers.views.profile import ProfileView
from freelancers.views.update_service import ServiceUpdateView
from freelancers.views.update_profile import ProfileUpdateView

app_name = 'freelancers'
urlpatterns = [
    path('register', CreateView.as_view(
        template_name='registration/register.html',
        form_class=RegistrationForm,
        success_url='/'
    ), name='register'),
    path('search', ListView.as_view(), name="search"),
    path('profile', ProfileView.as_view(), name="profile"),
    re_path('profile/(?P<slug>\w{0,50})/$',
            DetailView.as_view(), name="profile"),
    path('updateservice', ServiceUpdateView.as_view(), name="service_update"),
    path('updateprofile', ProfileUpdateView.as_view(), name="profile_update"),
]
