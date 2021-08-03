from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from mirage import fields

User = get_user_model()


class MTO(User):
    # contact_number = PhoneNumberField(blank=True)
    contact_number = fields.EncryptedCharField(blank=True)
    location = CountryField(blank_label="Select Location")
    job_category = models.CharField(max_length=500, null=True)
    # paypal_id = models.CharField(max_length=100)
    paypal_id = fields.EncryptedCharField(max_length=100)
    token = fields.EncryptedCharField(max_length=100, null=True)

    # token = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.full_name
