"""techlancers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function viewsAuthenication
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic.edit import CreateView
from recruiters.forms.registration_form import RegistrationForm
from recruiters.views.job_list import JobListView
from recruiters.views.job_create import JobCreateView

app_name = 'recruiters'
urlpatterns = [
    path('register', CreateView.as_view(
        template_name='registration/register.html',
        form_class=RegistrationForm,
        success_url='/'
    ), name="register"),
    path('jobs', JobListView.as_view(), name="jobs"),
    path('postjob', JobCreateView.as_view(), name="postjob"),
]
