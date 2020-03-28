from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from account.tasks import send_email_async
from currency_exchange import settings

from account.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'created',
            'email',
            'title',
            'text',
        )

        # extra_kwargs = {
        #     'email': {'write_only': True},
        # }

        def save(self):
            email_from = [settings.EMAIL_HOST_USER, ]
            subject = self.validated_data['title']
            message = self.validated_data['text']
            recipient_list = self.validated_data['email']
            send_email_async.delay(subject, message, email_from, recipient_list)
