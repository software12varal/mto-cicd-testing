from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_mto = models.BooleanField(default=False)  # by default the user is an MTO.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # if self.pk is None:
        if self.is_admin or self.is_staff or self.is_super_admin and not self.is_mto:
            super(User, self).save(using='varal_job_posting_db')
        else:
            super(User, self).save(using="vendor_os_db")
        # else:
        #     if User.objects.using("varal_job_posting_db").filter(username=self.username).exists():
        #         super(User, self).save(using='varal_job_posting_db')
        #     elif User.objects.using("vendor_os_db").filter(username=self.username).exists():
        #         super(User, self).save(using="vendor_os_db")



