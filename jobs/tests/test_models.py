from django.test import TestCase
from jobs.models import MTOJobCategory, MTOAdminUser
from django.conf import settings
from django.conf.global_settings import *

"""
We overide the default orientation of DATABASE_ROUTERS settings so that
the test in the jobs app can run successfully.
"""

class JobsTestDbMixin:
    databases = {"varal_job_posting_db", }
    settings.DATABASE_ROUTERS = ['routers.db_routers.VaralJobPostingDBRouter', 'routers.db_routers.VendorOSRouter',
                                 'routers.db_routers.AccountsDBRouter']

class TestNew(JobsTestDbMixin, TestCase):

    def test_model_str(self):
        name = MTOJobCategory.objects.create(name="DjangoTesting")
        print(name)
        self.assertEqual(str(name), "DjangoTesting")

    def test_model_user_str(self):
        user = MTOAdminUser(full_name='test', )
        print(user)
        self.assertEqual(str(user), "test")