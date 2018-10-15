"""
Contains the Filter for API.
"""
import django_filters

from .models import Saloon


class SaloonFilter(django_filters.FilterSet):
    class Meta:
        model = Saloon
        fields = {
            'name': ['iexact', 'icontains'],
            'address': ['iexact', 'icontains'],
            'opening_time': ['exact', 'lt', 'gt'],
            'closing_time': ['exact', 'lt', 'gt'],
            'area__name': ['iexact', 'icontains', ],
            'city__name': ['iexact', 'icontains', ],
            'country__name': ['iexact', 'icontains', ],
        }
