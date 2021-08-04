# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

User = get_user_model()


class SuperAdmin(User):
    contact_number = PhoneNumberField(blank=True)
    designation = models.CharField(max_length=500, blank=True)
    # department = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.full_name

    # def save(self, *args, **kwargs):
    #     super(MTO, self).save(using='vendor_os_db')
