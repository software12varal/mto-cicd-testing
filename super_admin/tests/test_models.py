from django.test import TestCase

# for connecting to Database
from core import settings
from super_admin.models import SuperAdmin


class SuperAdminModelTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"varal_job_posting_db", "vendor_os_db"}


# Testing the models
class SuperAdminModelTest(SuperAdminModelTestDbMixin, TestCase, ):
    '''without baker'''

    def test_model_str(self):
        full_name = SuperAdmin.objects.create(full_name="Super Admin")
        print(full_name)
        self.assertEqual(str(full_name), "Super Admin")

