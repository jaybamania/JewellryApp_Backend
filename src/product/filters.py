from django_filters import rest_framework as filters
from .models import Product


class ProductFilters(filters.FilterSet):
    trade = filters.CharFilter(field_name='trade', lookup_expr='icontains')
    purity = filters.NumberFilter(field_name='metal_purity')
    time = filters.NumberFilter(field_name='delivery_time')
    m_type = filters.NumberFilter(field_name='metal_category')
    pay = filters.NumberFilter(field_name='payment_type')
    metal = filters.NumberFilter(field_name='metal')

    class Meta():
        model = Product
        fields = ['trade', 'metal', 'm_type', 'purity', 'time', 'pay']
