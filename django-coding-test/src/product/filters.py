from django import forms
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
    variant = django_filters.CharFilter(field_name='productvariant__variant_title', lookup_expr='icontains',
                                        label='Variant contains')
    price_from = django_filters.NumberFilter(field_name='productvariantprice__price', lookup_expr='gte',
                                             label='Price from')
    price_to = django_filters.NumberFilter(field_name='productvariantprice__price', lookup_expr='lte', label='Price to')
    date = django_filters.DateFilter(field_name='created_at', label='Created date (YYYY-MM-DD)')

    class Meta:
        model = Product
        fields = ['title', 'variant', 'price_from', 'price_to', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['variant'].extra.update(
            {'widget': forms.Select(attrs={'class': 'form-control'})}
        )
