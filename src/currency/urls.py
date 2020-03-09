from django.contrib import admin
from django.urls import path

from currency.views import rates

app_name = 'currency'

urlpatterns = [
    path('rates/', rates, name='rates'),
]
