from django.test import TestCase
from django.conf import settings
from django.conf.global_settings import *
from django.urls import reverse

class JobsTestDbMixin:
    databases = {"varal_job_posting_db", }
    settings.DATABASE_ROUTERS = ['routers.db_routers.VaralJobPostingDBRouter', 'routers.db_routers.VendorOSRouter',
                                 'routers.db_routers.AccountsDBRouter']


class TestUrls(JobsTestDbMixin, TestCase):
    def test_testhome(self):
        url = reverse('jobs:admin_register')
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, 200)
