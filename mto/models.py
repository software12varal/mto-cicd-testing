from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class MTO(User):
    contact_number = PhoneNumberField(blank=True)
    location = models.CharField(max_length=20)
    job_category = models.CharField(max_length=500, null=True)
    paypal_id = models.CharField(max_length=100)
    token = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.full_name

    # def save(self, *args, **kwargs):
    #     super(MTO, self).save(using='vendor_os_db')
