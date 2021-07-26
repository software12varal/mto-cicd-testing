from django.test import TestCase

# for connecting to Database
from super_admin.models import SuperAdmin


class SuperAdminTestDbMixin:
    databases = {}


# Testing the models
class TestNew(SuperAdminTestDbMixin, TestCase, ):
    '''without baker'''

    def test_model_str(self):
        full_name = SuperAdmin.objects.create(full_name="DjangoTesting")
        print(full_name)
        self.assertEqual(str(full_name), "DjangoTesting")

    '''Using baker'''
    # def setUp(self):
    #     self.description = baker.make('accounts.MTOPaymentStatus')
    #     # pprint(self.description.__dict__)

    # def test_model_str(self):

    #     sample_status = baker.prepare('accounts.MTOPaymentStatus')
    #     print(sample_status)
    #     MTOPaymentStatus.objects.create(description= sample_status)
    #     self.assertEqual(str(sample_status), MTOPaymentStatus.objects.last().description)
