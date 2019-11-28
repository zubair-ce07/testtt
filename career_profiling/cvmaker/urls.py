from .views import (
    EducationView,
    ExperienceView,
    SkillView,
    ProfileView,
    UserView
)
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('education', EducationView)
router.register('experience', ExperienceView)
router.register('skill', SkillView)
router.register('profile', ProfileView)
router.register('user', UserView)
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]
