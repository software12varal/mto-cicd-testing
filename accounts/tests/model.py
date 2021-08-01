from django.test import TestCase
from django.utils.html import DOTS
from accounts.models import MTOPaymentStatus
from mto.models import MTO
from model_bakery import baker
from pprint import pprint

# for connecting to Database
# class AccountsTestDbMixin:
    #databases = {"accounts_db", }


# Testing the models
class TestNew("accounts_db", TestCase,):

    '''without baker'''
    def test_model_str(self):
        description = MTOPaymentStatus.objects.create(description="DjangoTesting")
        print(description)
        self.assertEqual(str(description), "DjangoTesting")


    '''Using baker'''
    # def setUp(self):
    #     self.description = baker.make('accounts.MTOPaymentStatus')
    #     # pprint(self.description.__dict__)

    # def test_model_str(self):

    #     sample_status = baker.prepare('accounts.MTOPaymentStatus')
    #     print(sample_status)
    #     MTOPaymentStatus.objects.create(description= sample_status)
    #     self.assertEqual(str(sample_status), MTOPaymentStatus.objects.last().description)
