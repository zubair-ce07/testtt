from django.conf.urls import url

from api import views

app_name = 'api'

urlpatterns = [
    url(r'^user_list/$', views.UserListView.as_view(), name='list-api'),
    url(r'^user_create/$', views.CreateUserView.as_view(), name='create-api'),
    url(r'^users/$', views.RetrieveUpdateDeleteUserView.as_view(), name='details-api'),
    url(r'^users/search/$', views.SearchUserView.as_view(), name='search-api'),

    url(r'^details/$', views.UserProfileDetailView.as_view(), name='details'),
    url(r'^edit/$', views.UpdateUserProfileView.as_view(), name='edit'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
