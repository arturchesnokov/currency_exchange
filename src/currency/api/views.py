from rest_framework import generics

from currency.models import Rate
from currency.api.serializers import RateSerializer


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
