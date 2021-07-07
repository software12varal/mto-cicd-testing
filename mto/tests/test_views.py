
from django.test import TestCase, Client
from django.urls import reverse
from jobs.models import MTOJob,Jobs,PaymentStatus,Jobstatus,EvaluationStatus,MALRequirement
from mto.models import MTO
import json
from django.conf import settings
from django.conf.global_settings import *

class JobsTestDbMixin:
    databases = {"vendor_os_db", "varal_job_posting_db"}
    

# Demo view test class
class TestDashboardViews(JobsTestDbMixin, TestCase):

    # This will through a 302 error. The url returns a /mto/login/?next=/mto/ path instead of '/'
    def setUp(self):
        catid = MALRequirement.objects.create(identification_number = 'jhgfd56y',assembly_line_id='bght67f',assembly_line_name = 'devs',person_name = 'Sam',person_email = 'django@gmail.com',output = 'htmlcov/style.css',micro_task = 'Developer',micro_task_category = json.dumps([1]),target_date = '2020-04-04',total_budget = '20', job_description = 'Create website',job_sample = 'images/job_documents/job_samples/CURRICULUM_VITAE.docx',job_instructions = '/images/job_documents/job_instructions/CURRICULUM_VITAE.docx',job_quantity = '1',input_folder = 'htmlcov/style.css')
        
        jobid = Jobs.objects.create(job_name = 'Developer',cat_id = catid,target_date=2020-4-10 12:20:00,job_description = 'Create website',job_sample = 'images/job_documents/job_samples/CURRICULUM_VITAE.docx',job_instructions = 'htmlcov/style.css',job_quantity = 1,people_required ='2',skills = 'python',job_cost= 10)
        
        paymentstatus = PaymentStatus.objects.create(payment_status = 'paid')
        jobstatus = Jobstatus.objects.create(job_status = 'Submitted')
        evaluationstatus = EvaluationStatus.objects.create(description = 'None')
        
        mtojob = MTOJob.objects.create(job_id = jobid.primarykey,assigned_to='1',due_date='2020-04-10 12:20',fees=10.00,rating_evaluation= 2,paymentstatus=paymentstatus,jobstatus=jobstatus,completed_date='2020-04-10 12:20',output_path='htmlcov/style.css',is_submitted='True',evaluationstatus = evaluationstatus)

        self.mto = MTO(username="DjangoTesting", email='mto@gmail.com', paypal_id='paypal', token='mto-token',full_name='My name', is_active=True, contact_number='+2547123456789', location="Kenya",job_category=json.dumps([1]), is_mto=True)
        self.mto.set_password('password')
        self.mto.save()

    def test_dummy_home_view_redirects_when_not_authenticated(self):
        
        # use reverse to map the url
        url = reverse('mto:home')

        response = self.client.get(url)
        print(response)
        self.assertEquals(response.status_code, 302)
       
        # compares response to the template
    
    def test_dashboard_page(self):
        self.client.force_login(user=self.mto)
        url = reverse('mto:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'mto/mto_dashboard.html')
        self.assertIsInstance(response.context['jobs','jobs_submitted','jobs_completed','jobs_approved','total'], dashboard)


        
