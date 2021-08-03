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

    # def save(self, *args, **kwargs):
    #     super(MTO, self).save(using='vendor_os_db')


class MTOLoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'user: {}, attempts: {}'.format(self.user.username, self.login_attempts)
