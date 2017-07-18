from django.conf.urls import url
from .views import Login, SignupView


app_name = 'wblog'

urlpatterns = [
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'$', Login.as_view(), name='login'),
]
