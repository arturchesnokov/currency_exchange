from requests import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED

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
        return Contact.objects.filter(email=user.email)

    @api_view(['POST'])
    def send_email_on_save(request):
        if request.method == 'POST':
            email_from = [settings.EMAIL_HOST_USER, ]
            subject = request.data['title']
            message = request.data['text']
            recipient_list = [request.data['email'], ]
            send_email_async.delay(subject, message, email_from, ('emailds@sdfs.com',))
            return Response(HTTP_201_CREATED)
        return Response({"message": "Hello, world!"})



    # def post(self, request, *args, **kwargs):
    #     serializer = ContactSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #
    #     # email_from = [settings.EMAIL_HOST_USER, ]
    #     # subject = request.data['title']
    #     # message = request.data['text']
    #     # recipient_list = request.data['email']
    #     # send_email_async.delay(subject, message, email_from, recipient_list)
    #
    #     return Response(HTTP_201_CREATED)


class ContactView(generics.RetrieveUpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def save(self):
        pass
