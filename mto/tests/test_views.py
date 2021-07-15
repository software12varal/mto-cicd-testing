# import json
#
# from model_bakery import baker
# from datetime import timedelta
#
# from django.conf import settings
# from django.conf.global_settings import *
# from django.test import TestCase, Client
# from django.urls import reverse
# from django.utils import timezone
#
# from jobs.models import MTOJob, Jobs, MicroTask
# from mto.forms import MTOUpdateProfileForm
#
# from mto.models import MTO
#
#
# class MTOTestDbMixin:
#     databases = {"vendor_os_db", "varal_job_posting_db"}
#
#
# # Demo view test class
# class TestViews(MTOTestDbMixin, TestCase):
#
#     # This will through a 302 error. The url returns a /mto/login/?next=/mto/ path instead of '/'
#     def test_dummy_home_view(self):
#         url = reverse('mto:home')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 302)
#
#
# class TestMTOProfileView(MTOTestDbMixin, TestCase):
#     def setUp(self):
#         self.profile_url = reverse('mto:profile')
#         # MicroTask.objects.create(microtask_name='develop website',
#         #                          microtask_category='Django',
#         #                          job_cost=140,
#         #                          time_required=24,
#         #                          skills='Django HTML CSS',
#         #                          people_required_for_valid_tc=2,
#         #                          job_sample='htmlcov\style.css',
#         #                          job_instructions='htmlcov\style.css')
#         baker.make(MicroTask, job_sample="test_py.txt", _quantity=3)
#         microtask = MicroTask.objects.all().first()
#         self.job = Jobs(
#             identification_number=123,
#             assembly_line_id=45,
#             assembly_line_name='Assembly line',
#             person_name='John Doe',
#             output='media/documents/job_documents/output',
#             job_name='Django Authentication',
#             cat_id=microtask,
#             target_date=timezone.now() + timedelta(days=3),
#             total_budget=200,
#             job_description='handle google authentication',
#             job_sample='Onkar_py.txt',
#             job_instructions='test_py.txt',
#             job_quantity=1,
#             input_folder='media/documents/job_documents/input')
#         self.mto = MTO(username="DjangoTesting", email='mto@gmail.com', paypal_id='paypal', token='mto-token',
#                        full_name='My name', contact_number="+2547123456789", location="Kenya",
#                        job_category=json.dumps(list(self.job)))
#         self.mto.set_password('password')
#         self.mto.save()
#         return
#
#     def test_profile_view_redirects_to_login_when_not_authenticated(self):
#         response = self.client.get(self.profile_url)
#         self.assertRedirects(response, reverse('login'), 302)
#
#     def test_profile_view_GET_response_when_authenticated(self):
#         self.client.force_login(self.mto)
#         response = self.client.get(self.profile_url)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mto/profile.html')
#
#     def test_profile_view_context_data(self):
#         self.client.force_login(self.mto)
#         response = self.client.get(self.profile_url)
#         json_dec = json.decoder.JSONDecoder()
#         mto_preferred_categories = json_dec.decode(self.mto.job_category)
#         job_categories = [Jobs.objects.get(id=job_id) for job_id in mto_preferred_categories]
#         self.assertEquals(response.context['mto'], self.mto)
#         self.assertEquals(response.context['job_categories', job_categories])
#         self.assertIsInstance(response.context['form'], MTOUpdateProfileForm)
#
#     def test_profile_view_post_method(self):
#         self.client.force_login(self.mto)
#         data = {'contact_number': '+2547123456788', 'location': 'India', 'paypal_id': 'payPal',
#                 'job_category': self.job}
#         response = self.client.post(self.profile_url, data=data, follow=True)
#         mto = MTO.objects.get(id=1)
#         print('MTO DETAILS ARE >>>>>', mto.location, mto.contact_number, mto.paypal_id)
#         self.assertTrue(True)
