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

#JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg3MzEyNTAxLCJqdGkiOiI1MWU5ZWNkNmNkOWY0OTdhYmY3M2I2ODM0N2EzODQ0OSIsInVzZXJfaWQiOjN9.MLZbc0IHoirDuk18EvBmSXb6N_5ghWUKtr2W4nyGwtY