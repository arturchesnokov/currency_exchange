from rest_framework import serializers
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

    def create(self, validated_data):
        subject = validated_data['title']
        message = validated_data['text']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [validated_data['email'], ]
        send_email_async.delay(subject, message, email_from, recipient_list)
        return super().create(validated_data)
