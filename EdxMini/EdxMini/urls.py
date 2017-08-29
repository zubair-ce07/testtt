"""EdxMini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from classes import views as classes_views

schema_view = get_schema_view(title='Pastebin API')
router = DefaultRouter()
router.register(r'students', classes_views.StudentViewSet)
router.register(r'courses', classes_views.CourseViewSet)
router.register(r'enrollments', classes_views.EnrollmentViewSet)
router.register(r'instructors', classes_views.InstructorViewSet)
router.register(r'users', classes_views.UserViewSet)

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^schema/$', schema_view),
    url(r'^', include('classes.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
