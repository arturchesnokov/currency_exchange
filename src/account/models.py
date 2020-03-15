from uuid import uuid4

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db import models
from django.contrib.auth.models import AbstractUser


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


# @receiver(post_save, sender=User)
# def remove_image(sender, instance, signal, **kwargs):
#     print("remove_image method!\n" * 10)
