from django.urls import path, include

from . import views, admin
import feedback.views, report.views

app_name = 'accounts'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='my_profile'),
    path('consumers_list/', views.UnpairedConsumersList.as_view(), name='consumers_list'),
    path('consumers_list/<int:pk>', views.ConsumerDetail.as_view()),
    path('my_consumers/', views.PairedConsumersList.as_view(), name='my_consumers'),
    path('my_donor/', views.HomeConsumer.as_view(), name='home_consumer'),
]
