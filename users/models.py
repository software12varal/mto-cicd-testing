from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    is_mto = models.BooleanField(default=True)  # by default the user is an MTO.
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        try:
            if self.is_staff:
                super(User, self).save(using='varal_job_posting_db')
            else:
                super(User, self).save(using='vendor_os_db')
        except:
            super(User, self).save(using='varal_job_posting_db')
