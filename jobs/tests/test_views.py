# from django.conf import settings
# from django.contrib import auth
# from django.test import TestCase
# from django.urls import reverse
# from jobs.models import MTOAdminUser, AdminRoles  #
# from users.models import User


# class JobsTestDbMixin:
#     settings.UNDER_TESTING = True
#     databases = {"varal_job_posting_db", "vendor_os_db"}


# class TestViews(JobsTestDbMixin, TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         role = AdminRoles.objects.create(description="tester")
#         instance = MTOAdminUser.objects.create(email='admin@gmail.com', is_admin=True, is_active=True,
#                                                varal_role_id=role,
#                                                full_name='varalAdmin', username='bonnie')
#         instance.set_password('1234')
#         instance.save()

#     def test_home_GET(self):
#         url = reverse('jobs:home')
#         response = self.client.get(url)
#         print(response)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'jobs/index.html')

#     def test_job_form(self):
#         self.client.login(username='bonnie', password='1234')
#         user = auth.get_user(self.client)
#         print(AdminRoles.objects.all())
#         print(MTOAdminUser.objects.all())
#         print(user)
#         self.assert_(user.is_authenticated, 'Not Authenticated')
#         url = reverse('jobs:add_job')
#         response = self.client.get(url)
#         print(response)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'jobs/jobsform.html')
