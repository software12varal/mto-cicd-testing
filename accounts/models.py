from django.db import models


class MTOPaymentStatus(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Payment(models.Model):
    job_id = models.IntegerField(help_text='related to micro task')
    assigned_to = models.IntegerField(help_text='related to MTO')
    payment_id = models.IntegerField()
    payment_date = models.DateField()
    fees = models.FloatField()
