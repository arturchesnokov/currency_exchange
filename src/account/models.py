from uuid import uuid4
from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings

from account.tasks import send_email_async


def avatar_path(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    f_name = str(uuid4())
    filename = f'{f_name}.{ext}'
    return '/'.join(['avatar', str(instance.id), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    # send_email_async(subject, message, email_from, recipient_list)
    def send_activation_code(self):
        link = reverse('account:activate', args=(self.code,))
        subject = 'Activation code'
        message = f'Your code: http://127.0.0.1{link} '
        email_from = [settings.EMAIL_HOST_USER, ]
        recipient_list = [self.user.email, ]

        send_email_async.delay(subject, message, email_from, recipient_list)


