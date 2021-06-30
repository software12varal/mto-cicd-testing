from django.test import TestCase, Client
from django.urls import reverse
from jobs.models import MTOJob
import json
from django.conf import settings
from django.conf.global_settings import *

class JobsTestDbMixin:
    databases = {"vendor_os_db", }
    

# Demo view test class
class TestViews(JobsTestDbMixin, TestCase):

    # This will through a 302 error. The url returns a /mto/login/?next=/mto/ path instead of '/'
    def test_dummy_home_view(self):
        client = Client()
        # use reverse to map the url
        url = reverse('mto:home')

        response = self.client.get(url)
        print(response)
        self.assertEquals(response.status_code, 200)
        # compares response to the template
        self.assertTemplateUsed(response, 'mto/index.html') 
