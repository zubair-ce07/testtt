from api.views.user_view_set import UserViewSet
from api.views.freelancer_view_set import FreelancerViewSet

user = UserViewSet.as_view({
    'get': 'retrieve',
    'post': 'create'
})

freelancer = FreelancerViewSet.as_view({
    'get': 'list'
})
