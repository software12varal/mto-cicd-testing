from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MTO(User):
    paypal_id = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    # def save(self, *args, **kwargs):
    #     super(MTO, self).save(using='vendor_os_db')
