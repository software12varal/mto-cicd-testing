from django.test import TestCase
from accounts.models import MTOPaymentStatus
from django.test.testcases import SerializeMixin, TransactionTestCase


class AccountsTestDbMixin:
    databases = {"accounts_db", }


class TestNew(AccountsTestDbMixin, TestCase):
    def test_model_str(self):
        description = MTOPaymentStatus.objects.create(description="DjangoTesting")
        self.assertEqual(str(description), "DjangoTesting")
