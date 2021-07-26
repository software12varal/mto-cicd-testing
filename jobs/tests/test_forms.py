from django.test import TestCase
from jobs.forms import JobForm, JobsForm
from django.conf import settings
from django.conf.global_settings import *
from django.utils import timezone

from jobs.models import MTOAdminUser, AdminRoles


class JobsTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"varal_job_posting_db", "vendor_os_db"}


class AddJobsTest(JobsTestDbMixin, TestCase):
    # def setUp(self):
    @classmethod
    def setUp(cls):
        role = AdminRoles.objects.create(description="tester")
        instance = MTOAdminUser.objects.create(email='admin@gmail.com', is_admin=True, is_active=True,
                                               varal_role_id=role,
                                               full_name='varalAdmin', username='fred')
        instance.set_password('1234')
        instance.save()

    def test_forms(self):
        upload_file = open(str(settings.MEDIA_ROOT) + '/' + 'test_py.txt', 'rb')
        form_data = {'identification_number': 'webdev', 'assembly_line_id': 'webdev', 'assembly_line_name': 'webdev',
                     'person_name': 1, 'output': 'media/documents/job_documents/output/requirements.txt',
                     'job_name': 'website', 'cat_id': 'websites', 'target_date': timezone.now(), 'total_budget': 22,
                     'job_description': 'develop website', 'job_quantity': 3, 'input_folder': 'documents',
                     'sample': upload_file.read(), 'instructions': upload_file.read()
                     }

        form = JobForm(data=form_data)
        # form.save()
        # print(form)
        self.assertTrue(form.is_valid())
