from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from currency.models import Rate

from currency.api.filters import RatesFilter
from currency.api.serializers import RateSerializer

from rest_framework import generics


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filterset_class = RatesFilter
    pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
