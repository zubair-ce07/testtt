from django.conf.urls import url
from users import views


urlpatterns = [
    url(r'^authenticate/$', views.obtain_auth_token),
    url(r'^notifications/$', views.GetNotifications.as_view()),
    url(r'^notifications/(?P<notification_id>\d+)/$', views.delete_notification),
    url(r'^users/(?P<receiver_id>\d+)/send-request/$', views.send_follow_request),
    url(r'^requests/(?P<request_id>\d+)/(?P<action>\w+)/$', views.accept_or_block_request),
]
