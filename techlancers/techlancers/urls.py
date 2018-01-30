from django.contrib import admin
from django.urls import include, path
from techlancers.views.home import Home
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from techlancers.forms.admin_registration_form import AdminRegistrationForm

urlpatterns = [
    path('', Home.as_view()),
    path('admin/', admin.site.urls),
    path('freelancers/', include("freelancers.urls", namespace='freelancers')),
    path('recruiters/', include("recruiters.urls", namespace='recruiters')),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout,
         {'next_page': '/'}),
    path('register/admin', CreateView.as_view(
        template_name='registration/register.html',
        form_class=AdminRegistrationForm,
        success_url='/'
    )),
]
