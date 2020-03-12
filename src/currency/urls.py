from django.contrib import admin
from django.urls import path

from currency.views import RateListView, RateCSV

app_name = 'currency'

urlpatterns = [
    path('rates/', RateListView.as_view(), name='rates'),
    path('download/rates/', RateCSV.as_view(), name='download-rates'),
]
