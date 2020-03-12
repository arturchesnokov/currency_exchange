from uuid import uuid4

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
