from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.conf.global_settings import *

class JobsTestDbMixin:
    databases = {"varal_job_posting_db", }
    settings.DATABASE_ROUTERS = ['routers.db_routers.VaralJobPostingDBRouter', 'routers.db_routers.VendorOSRouter',
                                 'routers.db_routers.AccountsDBRouter']



class TestViews(JobsTestDbMixin, TestCase):
    def test_home_GET(self):
        client = Client()
        url = reverse('jobs:home')

        response = self.client.get(url)
        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/index.html')
