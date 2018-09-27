from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(title='Ballot API')

urlpatterns = [
    url(r'^schema/$', schema_view),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('', include('user.urls')),
]
