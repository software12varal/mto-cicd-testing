import json

from model_bakery import baker
from datetime import timedelta

from django.conf import settings
from django.conf.global_settings import *
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from jobs.models import MTOJob, Jobs, MicroTask, AdminRoles, MTOAdminUser
from mto.forms import MTOUpdateProfileForm

from mto.models import MTO


class MTOTestMixin:
    settings.UNDER_TESTING = True
    databases = {"vendor_os_db", "varal_job_posting_db"}
    # settings.DATABASE_ROUTERS = ['routers.db_routers.VendorOSRouter', 'routers.db_routers.VaralJobPostingDBRouter',
    #                              'routers.db_routers.AccountsDBRouter']


# Demo view test class
class TestViews(MTOTestMixin, TestCase):

    # This will through a 302 error. The url returns a /mto/login/?next=/mto/ path instead of '/'
    def test_dummy_home_view(self):
        url = reverse('mto:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)


class TestMTOProfileView(MTOTestMixin, TestCase):
    def setUp(self):
        self.profile_url = reverse('mto:profile')
        # # MicroTask.objects.create(microtask_name='develop website',
        # #                          microtask_category='Django',
        # #                          job_cost=140,
        # #                          time_required=24,
        # #                          skills='Django HTML CSS',
        # #                          people_required_for_valid_tc=2,
        # #                          sample='htmlcov\style.css',
        # #                          instructions='htmlcov\style.css')
        # baker.make(MicroTask, _quantity=1)
        # microtask = MicroTask.objects.all().first()
        admin_role = AdminRoles.objects.create(description='Tester')
        self.mto_admin = MTOAdminUser.objects.create(username="MTOAdmin", email='mtoadmin@gmail.com',
                                                     full_name='John MTOAdmin',
                                                     department='habot', varal_role_id=admin_role, designation='TC',
                                                     is_admin=True, is_active=True)
        self.mto_admin.set_password('testpassword')
        self.mto_admin.save()
        # baker.make(MTOAdminUser, _quantity=5)
        print('>>>>>> ALL THE MTO ADMINS .>>>>>>', MTOAdminUser.objects.using('vendor_os_db').all())
        self.job = Jobs(
            identification_number=123,
            assembly_line_id=45,
            assembly_line_name='Assembly line',
            person_name=self.mto_admin,
            output='media/documents/job_documents/output',
            job_name='Django Authentication',
            job_status='cr',
            cat_id=1,
            target_date=timezone.now() + timedelta(days=3),
            total_budget=200,
            job_description='handle google authentication',
            sample='Onkar_py_f0eh8Uo.txt',
            instructions='test_py.txt',
            job_quantity=1,
            input_folder='media/documents/job_documents/input')
        self.job.save(using='varal_job_posting_db')
        print('>>>>> THE JOB IS >>>>>', Jobs.objects.all())
        self.mto = MTO(username="DjangoTesting", email='mto@gmail.com', paypal_id='paypal', token='mto-token',
                       full_name='James MTO', contact_number="+2547123456789", location="Kenya",
                       job_category=json.dumps("[1]"), is_mto=True, is_admin=False, is_active=True)
        self.mto.set_password('password')
        self.mto.save()
        return

    def test_profile_view_redirects_to_login_when_not_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, '/mto/login/?next=%2Fmto%2Fprofile%2F', status_code=302)

    def test_profile_view_GET_response_when_authenticated(self):
        self.client.force_login(self.mto)
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mto/profile.html')

    # def test_profile_view_context_data(self):
    #     self.client.force_login(self.mto)
    #     response = self.client.get(self.profile_url)
    #     json_dec = json.decoder.JSONDecoder()
    #     mto_preferred_categories = json_dec.decode(self.mto.job_category)
    #     job_categories = [Jobs.objects.get(id=job_id) for job_id in mto_preferred_categories]
    #     self.assertEquals(response.context['mto'], self.mto)
    #     self.assertEquals(response.context['job_categories', job_categories])
    #     self.assertIsInstance(response.context['form'], MTOUpdateProfileForm)
    #
    # def test_profile_view_post_method(self):
    #     self.client.force_login(self.mto)
    #     data = {'contact_number': '+2547123456788', 'location': 'India', 'paypal_id': 'payPal',
    #             'job_category': self.job}
    #     response = self.client.post(self.profile_url, data=data, follow=True)
    #     mto = MTO.objects.get(id=1)
    #     print('MTO DETAILS ARE >>>>>', mto.location, mto.contact_number, mto.paypal_id)
    #     self.assertTrue(True)
