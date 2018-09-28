from django.urls import path, include
from rest_framework import routers
from ContactTodoManagement.Api.views import UserViewset, ContactViewset, TodoViewset, ItemViewset
app_name = 'api'

router = routers.DefaultRouter()
router.register(r'User', UserViewset, base_name='User')
router.register(r'Contact', ContactViewset, base_name='Contact')
router.register(r'Todo', TodoViewset, base_name='Todo')
router.register(r'Item', ItemViewset, base_name='Item')


urlpatterns = [
    path('', include(router.urls))
]
