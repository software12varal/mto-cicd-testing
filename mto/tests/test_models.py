from django.test import TestCase
# from model_bakery import baker

from mto.models import MTO


class MtoTestDbMixin:
    # maps to the vendor_os_db
    databases = {"vendor_os_db", }

# Mixin should always come first
class TestNew(MtoTestDbMixin, TestCase):

    def test_model_str(self):
        mto = MTO(username="DjangoTesting", email='mto@gmail.com', paypal_id='paypal', token='mto-token',
                  full_name='My name')
        mto.set_password('password')
        mto.save()
        self.assertEqual(str(mto), "My name")

