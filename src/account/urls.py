from django.contrib import admin
from django.urls import path

from account.views import SignUp, UserCreate

app_name = 'account'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', UserCreate.as_view(), name='registration'),
]
