from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_mto = models.BooleanField(default=False)  # by default the user is an MTO.
    timestamp = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save()
