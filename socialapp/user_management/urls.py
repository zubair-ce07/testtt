from django.urls import path, include
from user_management import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),

    path('', views.UsersView.as_view({
        'post': 'create',
        'get': 'list',
    })),

    path('<int:pk>/', views.UsersView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),


    path('work-information/(?P<username>/w+|)/$', views.WorkInformationView.as_view({
        'get': 'list',
    })),
    path('work-information/', views.WorkInformationView.as_view({
        'get': 'list',
        'post':  'create',
    }), name='work-information'),
    path('work-information/<int:pk>/', views.WorkInformationView.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),


    path('academic-information/(?P< username>/w+|)/$', views.AcademicInformationView.as_view({
        'get': 'list',
    })),
    path('academic-information/', views.AcademicInformationView.as_view({
        'get': 'list',
        'post':  'create',
    }), name='academic-information'),
    path('academic-information/<int:pk>/', views.AcademicInformationView.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),


    path('groups/', views.GroupsView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('groups/<int:pk>/', views.GroupsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),


    path('<int:pk>/group-requests/', views.GroupRequestView.as_view({
        'get': 'list',
    })),
    path('<int:user_id>/group-requests/<int:group_id>/', views.GroupRequestView.as_view({
        'post': 'create',
        'delete': 'destroy',
    }), name='cancel-group-request'),


    path('<int:pk>/friend-requests/', views.FriendRequestView.as_view({
        'get': 'list',
    })),
    path('<int:request_to_id>/friend-request/<int:request_from_id>/', views.FriendRequestView.as_view({
        'post': 'create',
        'delete': 'destroy',
    }), name='cancel-friend-request'),


    path('<int:pk_user>/group-join/', views.JoinGroupsView.as_view({
        'get': 'list',
    })),
    path('<int:pk_user>/group-join/<int:pk_group>/', views.JoinGroupsView.as_view({
        'get': 'retrieve',
        'post': 'create',
        'delete': 'destroy',
    }), name='add-group'),


    path('<int:pk_user>/friends/', views.FriendsView.as_view({
        'get': 'list',
    })),
    path('<int:pk_user>/add-friend/<int:pk_friend>/', views.FriendsView.as_view({
        'get': 'retrieve',
        'post': 'create',
        'delete': 'destroy'
    }), name='add-friend'),

]
