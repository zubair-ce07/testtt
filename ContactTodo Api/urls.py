from django.urls import path, include
from ContactTodoManagement.Api.views import UserViewset, ContactViewset, TodoViewset, ItemViewset
from rest_framework.authtoken import views
app_name = 'api'

urlpatterns = [
    path('get_token/', views.obtain_auth_token),

    path('get_users/', UserViewset.as_view({'get': 'list'})),
    path('get_user/<int:pk>', UserViewset.as_view({'get': 'retrieve'})),
    path('create_user/', UserViewset.as_view({'post': 'create'})),
    path('update_user/<int:pk>', UserViewset.as_view({'put': 'update'})),

    path('get_contacts/', ContactViewset.as_view({'get': 'list'})),
    path('get_contact/<int:pk>', ContactViewset.as_view({'get': 'retrieve'})),
    path('create_contact/', ContactViewset.as_view({'post': 'create'})),
    path('update_contact/<int:pk>', ContactViewset.as_view({'put': 'update'})),

    path('get_todos/', TodoViewset.as_view({'get': 'list'})),
    path('get_todo/<int:pk>', TodoViewset.as_view({'get': 'retrieve'})),
    path('create_todo/', TodoViewset.as_view({'post': 'create'})),
    path('update_todo/<int:pk>', TodoViewset.as_view({'put': 'update'})),

    path('get_items/', ItemViewset.as_view({'get': 'list'})),
    path('get_item/<int:pk>', ItemViewset.as_view({'get': 'retrieve'})),
    path('create_item/', ItemViewset.as_view({'post': 'create'})),
    path('update_item/<int:pk>', ItemViewset.as_view({'put': 'update'})),
]
