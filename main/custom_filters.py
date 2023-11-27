from django_filters import rest_framework as filters

from .models import Stay


class StayFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    # min_rate = filters.NumberFilter(field_name='property_rate_stars', lookup_expr='lte')
    # max_rate = filters.NumberFilter(field_name='property_rate_stars', lookup_expr='gte')

    class Meta:
        model = Stay
        fields = ('name', 'slug')
