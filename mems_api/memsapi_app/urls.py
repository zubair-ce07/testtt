from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from mems_api import settings
from memsapi_app.views import UserView,  MemoryListView, Logout, index, GetAllMems, \
                              ActivityListView, CreateAndListCategory, GetPublicMems, Login, SignUp
from rest_framework.authtoken import views

router = routers.DefaultRouter()


app_name = 'memoapp'
urlpatterns = [
    url(r'^$', include(router.urls)),
    url(r'^index/', index),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^signup/$', SignUp.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', UserView.as_view()),
    url(r'^mems/$', MemoryListView.as_view()),
    url(r'^categories/$', CreateAndListCategory.as_view()),
    url(r'^activities/$', ActivityListView.as_view()),
    url(r'^get-public-mems/$', GetPublicMems.as_view()),
    url(r'^get-api-token/$' , views.obtain_auth_token),
    url(r'^get-all-mems/$' , GetAllMems.as_view())
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)