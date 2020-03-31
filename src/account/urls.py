from django.urls import path

from account.views import SignUp, UserCreate, ContactForm, MyProfile, SignUpView, Activate

app_name = 'account'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    path('registration/', UserCreate.as_view(), name='registration'),
    path('contact/', ContactForm.as_view(), name='contact'),
    path('profile/<int:pk>/', MyProfile.as_view(), name='profile'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('activate/<uuid:activation_code>', Activate.as_view(), name='activate'),
]
