from django.test import TestCase
from model_bakery import baker
from mto.models import MTO

class AccountsTestDbMixin:
    databases = {"accounts_db", }


class TestNew(AccountsTestDbMixin, TestCase):
    def test_model_str(self):
        mto = MTO(username="DjangoTesting", email='mto@gmail.com', paypal_id='paypal', token='mto-token')
        self.assertEqual(str(mto), "DjangoTesting")