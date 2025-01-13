import django_filters
from product.models import Product


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['title', 'description', 'price_min', 'price_max']
