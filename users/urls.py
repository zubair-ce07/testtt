from django.urls import path
from users.views import UserList, UserDetail, ProfileList, ProfileDetail, CreateUserView

urlpatterns = [
    path('profiles/', ProfileList.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('register/', CreateUserView.as_view(), name='sign-up'),
]
