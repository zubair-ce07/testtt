import django_filters

from users.models import User


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last Name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
