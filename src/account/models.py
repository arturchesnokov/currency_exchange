from uuid import uuid4
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from account.tasks import send_email_async


def avatar_path(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    f_name = str(uuid4())
    filename = f'{f_name}.{ext}'
    return '/'.join(['avatar', str(instance.id), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)
    phone = PhoneNumberField()


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)


def generate_sms_code():
    import random
    return random.randint(1000, 9999)


class ActivationCodeSms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.PositiveIntegerField(default=generate_sms_code)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 1

    # Here can be sms sending method
    def send_activation_code(self):
        subject = 'Activation code'
        message = f'Your code:{self.code} '
        email_from = [settings.EMAIL_HOST_USER, ]
        recipient_list = [self.user.email, ]

        send_email_async.delay(subject, message, email_from, recipient_list)
