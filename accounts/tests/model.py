from django.test import TestCase
from model_bakery import baker



<<<<<<< HEAD
from django.test import TestCase
from django.utils.html import DOTS
from accounts.models import MTOPaymentStatus
from mto.models import MTO
from model_bakery import baker
from pprint import pprint

class AccountsTestDbMixin:
    databases = {"accounts_db", }


class TestNew(AccountsTestDbMixin, TestCase,):

    # def test_model_str(self):
    #     description = MTOPaymentStatus.objects.create(description="DjangoTesting")
    #     print(description)
    #     self.assertEqual(str(description), "DjangoTesting")

    def setUp(self):
        self.description = baker.make('accounts.MTOPaymentStatus')
        # pprint(self.description.__dict__)

    def test_model_str(self):

        sample_status = baker.prepare('accounts.MTOPaymentStatus')
        print(sample_status)
        MTOPaymentStatus.objects.create(description= sample_status)
        self.assertEqual(str(sample_status), MTOPaymentStatus.objects.last().description)
=======
>>>>>>> 62fa89d8f3ec43be278fb87d4ffca9c13035266f
