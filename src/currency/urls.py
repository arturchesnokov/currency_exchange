from django.contrib import admin
from django.urls import path

from currency.views import RateListView

app_name = 'currency'

urlpatterns = [
    # path('rates/', rates, name='rates'),
    path('rates/', RateListView.as_view(), name='rates'),
]
