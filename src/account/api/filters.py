from django_filters import rest_framework as filters

from currency.models import Rate


class RatesFilter(filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'currency': ['exact'],
            'source': ['exact'],
            'created': ['exact', 'lt', 'lte', 'gt', 'gte', 'range']
        }
