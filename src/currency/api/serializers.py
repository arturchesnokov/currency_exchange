from rest_framework import serializers

from currency.models import Rate


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'created',
            'currency',
            'get_currency_display',
            'buy',
            'sale',
            'get_source_display',
            'source',
        )
        extra_kwargs = {
            'currency': {'write_only': True},
            'source': {'write_only': True},
        }
