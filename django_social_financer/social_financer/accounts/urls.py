from django.urls import path, include

from . import views, admin
import feedback.views, report.views

app_name = 'accounts'
urlpatterns = [

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('my_consumers/', views.donors_pairs, name='my_consumers'),
    path('profile/', views.ProfileView.as_view(), name='my_profile'),
    path('', views.home_view, name='home'),

]