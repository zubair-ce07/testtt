"""Contains urls patterns for app 'user'"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from user import views
from user.helper import username_exist, email_exist

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='user/index'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^login/$', views.SignInView.as_view(), name='login'),
    url(r'^logout/$', views.SignoutView.as_view(), name='logout'),
    url(r'^new_product/$', views.NewProductView.as_view(), name='new_product'),
    url(
        r'^view_products/$',
        views.ViewProductsView.as_view(),
        name='view_products'
    ),
    url(
        r'^view_all_products/$',
        views.ViewAllProductsView.as_view(),
        name='view_all_products'
    ),
    url(
        r'^view_product_detail/(?P<pk>\d+)$',
        views.ProductDetailView.as_view(),
        name='view_product_detail'
    ),

    url(
        r'^user_profile/(?P<pk>\d+)$',
        views.UserProfileView.as_view(),
        name='user_profile'
    ),
    url(
        r'^users_list/$',
        views.UserListView.as_view(),
        name='users_list'
    ),
    url(
        r'^authenticate_without_password/(?P<username>.*)$',
        views.WithoutPasswordAuthticationView.as_view(),
        name='auth_no_password'
    ),
    url(
        r'^api/users_list/$',
        views.UserListAPI.as_view(),
    ),
    url(
        r'^api/login/$',
        views.TokenAuthenticationAPI.as_view(),
    ),
    url(
        r'^api/product_list/$',
        views.ProductListAPI.as_view(),
    ),
    url(
        r'^api/user_product_list/(?P<owner>\d+)$',
        views.UserProductListAPI.as_view(),
    ),
    url(
        r'^api/product_detail/(?P<pk>\d+)$',
        views.ProductDetailAPI.as_view(),
    ),
    url(
        r'^api/update_product/(?P<pk>\d+)$',
        views.UpdateProductAPI.as_view(),
    ),
    url(
        r'^api/user_profile/(?P<user>\d+)$',
        views.UserProfileAPI.as_view(),
    ),
    url(
        r'^api/create_product/$',
        views.CreateProductAPI.as_view(),
    ),
    url(
        r'^api/signup/$',
        views.SignUpAPI.as_view(),
    ),
    url(
        r'^api/signout/$',
        views.SignoutAPI.as_view(),
    ),
    url(
        r'^username_exist/$',
        username_exist,
    ),
    url(
        r'^email_exist/$',
        email_exist,
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
