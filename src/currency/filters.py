import django_filters
from django.forms import DateInput

from currency.models import Rate


class RateFilter(django_filters.FilterSet):
    # created_date = django_filters.DateFilter(field_name='created', lookup_expr='date')
    created_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='date',
        widget=DateInput(attrs={
            'type': 'date',
            'class': 'datepicker'
        }
        ))

    class Meta:
        model = Rate
        fields = ['buy', 'sale', 'source', 'created_date']
