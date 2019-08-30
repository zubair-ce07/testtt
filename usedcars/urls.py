from django.urls import path
from . import views


app_name = 'usedcars'
urlpatterns = [
    # /usedcars/
    path('', views.IndexView.as_view(), name='index')

]
