from django.contrib import admin
from django.urls import path

from account.views import SignUp, UserCreate, ContactForm, MyProfile

app_name = 'account'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', UserCreate.as_view(), name='registration'),
    path('contact/', ContactForm.as_view(), name='contact'),
    path('profile/<int:pk>/', MyProfile.as_view(), name='profile'),
]


