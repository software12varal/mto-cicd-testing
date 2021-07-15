from django.conf import settings
from django.test import TestCase
# from model_bakery import baker

from mto.models import MTO


class MtoTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"vendor_os_db", "varal_job_posting_db"}


# Mixin should always come first
class TestNew(MtoTestDbMixin, TestCase):

    def test_model_str(self):
        mto = MTO(username="DjangoTesting", email='mto@gmail.com', paypal_id='paypal', token='mto-token',
                  full_name='My name')
        mto.set_password('password')
        mto.save()
        self.assertEqual(str(mto), "My name")

