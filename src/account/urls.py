from django.contrib import admin
from django.urls import path

from account.views import smoke

urlpatterns = [
    path('smoke/', smoke),
]