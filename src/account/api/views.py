from requests import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from account.models import Contact
from account.tasks import send_email_async
from currency_exchange import settings

from account.api.serializers import ContactSerializer

from rest_framework import generics, status


class ContactsView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(email=user.email)


class ContactView(generics.RetrieveUpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
