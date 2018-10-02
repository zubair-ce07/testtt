from django.urls import path, include
from rest_framework_nested import routers
from system.views import SignupAPI, ContactViewSet, TodoViewSet, \
    ItemViewSet


router = routers.SimpleRouter()
router.register('contacts', ContactViewSet, base_name='Contact')
router.register('todos', TodoViewSet, base_name='Todo')


urlpatterns = [
    path('signup',
         SignupAPI.as_view(), name='signup'),
    path('rest-auth/',
         include('rest_auth.urls'), name='login'),
    path('', include(router.urls)),

    path('items/',
         ItemViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='item-create'),
    path('items/<int:pk>',
         ItemViewSet.as_view(
             {'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}),
         name='item-RUD'
         ),
]
