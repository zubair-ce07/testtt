import debug_toolbar
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='ShopCity API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^payment/', include('payment.urls')),
    url('^user/', include('users.urls')),
    url('^shopcity/', include('shopcity.urls')),
    url(r'^api/user/', include('rest_framework.urls')),
    url('^api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('^api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('^api/', include('api.urls')),
    url(r'^$', schema_view),
]

urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
