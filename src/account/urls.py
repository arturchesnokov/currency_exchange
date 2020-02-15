from django.contrib import admin
from django.urls import path

from account.views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]