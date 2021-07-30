from django.conf import settings
# Client mimiks how our client would access our views
from django.test import TestCase, Client
from django.urls import reverse

from jobs.forms import MTOAdminSignUpForm
from jobs.models import AdminRoles, MTOAdminUser
from super_admin.models import SuperAdmin


class SuperAdminTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"varal_job_posting_db", "vendor_os_db"}


class TestViews(SuperAdminTestDbMixin, TestCase):
    @classmethod
    def setUp(cls):
        # creating our client instance
        cls.client = Client()
        # create varal admin url
        cls.create_admin_url = reverse('jobs:admin_register')
        role = AdminRoles.objects.create(description="tester")
        cls.instance = MTOAdminUser.objects.create(email='admin@gmail.com', is_admin=True, is_active=True,
                                                   varal_role_id=role,
                                                   full_name='varalAdmin', username='fred')
        cls.instance.set_password('1234')
        cls.instance.save()

    def test_create_mto_admin(self):
        # MTOAdminSignUpForm.objects.create(
        #
        # )
        form_data = {'full_name': ' Super Admin', 'username': 'admin108', 'email': 'super@gmail.com',
                     'varal_role_id': '1234', 'contact_number': '+254721212112',
                     'designation': 'Managing Director', 'department': 'habot'}
        form = MTOAdminSignUpForm(form_data)

        response = self.client.post(self.create_admin_url,
                                    {'full_name': 'admin 108', 'username': 'admin108', 'email': 'admin108@gmail.com',
                                     'varal_role_id': '1234'})

        self.assertEquals(response.status_code, 200)
        print(response.status_code)
        print(form)
        # self.assertTrue(form.is_valid())
