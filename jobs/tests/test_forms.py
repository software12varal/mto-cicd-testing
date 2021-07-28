from django.test import TestCase
from jobs.forms import JobForm,JobsForm
from django.conf import settings
from django.conf.global_settings import *
from django.utils import timezone
from jobs.models import MTOAdminUser,AdminRoles

class JobsTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"varal_job_posting_db", "vendor_os_db"}



class AddJobsTest(JobsTestDbMixin, TestCase):
    @classmethod
    def setUp(cls):
        role = AdminRoles.objects.create(description="tester")
        instance = MTOAdminUser.objects.create(email='admin2@gmail.com', is_admin=True, is_active=True,varal_role_id=role,
        full_name='varalsAdmin', username='stl')
        instance.set_password('1234')
        instance.save()
    
    def test_job_form(self):
        upload_file = open(str(settings.MEDIA_ROOT) + '/' + 'test_py.txt', 'rb')
        form_data = {'identification_number':'webdev','assembly_line_id':'webdev','assembly_line_name':'webdev','person_name':1,'output':'media/documents/job_documents/output/requirements.txt','job_name':'website','cat_id':'websites','target_date': timezone.now(),'total_budget':22,'job_description':'develop website','job_quantity':3,'input_folder':'documents','sample':upload_file.read(),'instructions':upload_file.read()
        }
        
        form = JobForm(data=form_data)
        
        self.assertTrue(form.is_valid())



    def test_jobs_form_success(self):
        
        upload_file = open(str(settings.MEDIA_ROOT) + '/' + 'Onkar_py.txt', 'rb')
        form_data = {'microtask_name':'develop website','microtask_category': 'cw','job_cost':22,'time_required':23,'skills':'coding','people_required_for_valid_tc':2,'sample':upload_file.read(),'instructions':upload_file.read(),'tc_type': 'M','updated_date':timezone.now()}

        form = JobsForm(data=form_data)
        print(f"This is executing {form.errors}")
        self.assertTrue(form.is_valid())


