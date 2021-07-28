from django.conf import settings
from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse
from mto.models import MTO
from jobs.models import AdminRoles,MTOAdminUser,Jobs,MTOJob,MicroTask


class MtoTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"vendor_os_db", "varal_job_posting_db"}


# Mixin should always come first
class TestNew(MtoTestDbMixin, TestCase):

    def setUp(self):

        MicroTask.objects.create(microtask_name="NewJob",microtask_category='["cw","de"]',skills="GK",people_required_for_valid_tc=1,tc_type='["M"]')
        
        MTO.objects.create(username='admin',email='admin@mail.com',full_name='Shakeel',contact_number='+918989208001',
            location="Bangalore",paypal_id='Abc123',password='Varal2021',is_mto=True,job_category = '["cw","de"]',token='p0o9i8u7y6')
        data = MTO.objects.get(username='admin')
        data.set_password('Varal456')
        data.save()

        AdminRoles.objects.create(description='Developer')
        
        MTOAdminUser.objects.create(username='varalAdmin',email='varal@mail.com',full_name='varalAdmin',is_admin = True,is_active = True,varal_role_id=AdminRoles.objects.get(id=1))
        mtoadmin = MTOAdminUser.objects.get(full_name='varalAdmin')
        mtoadmin.set_password('Varal2021')
        mtoadmin.save()
        
        Jobs.objects.create(person_name=MTOAdminUser.objects.get(username='varalAdmin'),output='shak.txt',job_name='NewJob',cat_id='["cw"]',total_budget=5,job_description="na",job_quantity=1,input_folder = 'Shakeel/nawaz/')
        
        MTOJob.objects.create(job_id=Jobs.objects.get(id=1),assigned_to=1,due_date='2021-10-25 14:30:59',fees=500,output_path='Nawaz.txt')

        return self.client.login(username='admin',password='Varal456')

    def test_login_test(self):
        user = auth.get_user(self.client)
        self.assert_(user.is_authenticated,'Not Authenticated')

    def test_dummy_home_view(self):
        url = reverse('mto:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/index.html")

    def test_dashboard(self):
        url = reverse('mto:dashboard')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/mto_dashboard.html")

    def test_viewjobs(self):
        url = reverse('mto:view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/mto_viewjob.html")
  
    def test_view_applied_jobs(self):
        url = reverse('mto:applied')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/appliedjobs.html")
    
    def test_notification(self):
        url = reverse('mto:notification')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/notification.html")

    def test_view_payment_status(self):
        url = reverse('mto:view_payment_status')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/view_payment_status.html")

    def test_view_job_deadline(self):
        url = reverse('mto:job_deadline')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/job_deadline.html")
        
    def test_MTOProfileView(self):
        url = reverse('mto:profile')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/profile.html")
    
    def test_view_applied_details(self):
        mto = MTO.objects.get(id=1)
        job = MTO.objects.get(id=1)
        url = reverse('mto:view_applied_details', kwargs={'mto_id':mto.id ,'job_id':job.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/applied_jobs_details.html")

    def test_job_detail(self):
        jobsdata = Jobs.objects.get(id=1)
        url = reverse('mto:job_detail', kwargs={'slug':jobsdata.id})         
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/apply_job.html")

    def test_recommended_jobs(self):
        url = reverse('mto:recommended_jobs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"mto/recommended_jobs.html")

    def test_verify_valid_token(self):
        url = reverse('verify',kwargs={'token':'p0o9i8u7y6'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
   
    def test_verify_invalid_token(self):
        url = reverse('verify',kwargs={'token':'p0o9i8u'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
   
    def test_submit_job(self):
        url = reverse('mto:submit_job')
        response = self.client.post(url,data={'job_id':1,'output_path':'Na'})
        print(response)
        self.assertEquals(response.status_code,302)

    def test_submit_job_2(self):
        Jobs.objects.create(person_name=MTOAdminUser.objects.get(username='varalAdmin'),output='shak2.txt',job_name='NewJob2',cat_id='["cw"]',total_budget=5,job_description="na",job_quantity=1,input_folder = 'Shakeel2/nawaz2/team/')
        MTOJob.objects.create(job_id=Jobs.objects.get(id=2),assigned_to=1,due_date='2021-10-25 14:30:59',fees=500,output_path='Nawaz.txt',job_status='sub')
        url = reverse('mto:submit_job')
        response = self.client.post(url,data={'job_id':2,'output_path':'Na'})
        print(response)
        self.assertEquals(response.status_code,302)
    
    def test_submit_job_3(self):
        Jobs.objects.create(person_name=MTOAdminUser.objects.get(username='varalAdmin'),output='shak3.txt',job_name='NewJob2',cat_id='["cw"]',total_budget=5,job_description="na",job_quantity=1,input_folder = 'Shakeel2/nawaz2/team/')
        MTOJob.objects.create(job_id=Jobs.objects.get(id=2),assigned_to=1,due_date='2021-10-25 14:30:59',fees=500,output_path='Nawaz.txt',job_status='co')
        url = reverse('mto:submit_job')
        response = self.client.post(url,data={'job_id':2,'output_path':'Na'})
        self.assertEquals(response.status_code,302)

    def test_apply_jobs(self):
        url = reverse('mto:apply',kwargs={'id':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,reverse('mto:view'),302,200)

    def test_apply_jobs_2(self):
        self.client.logout()
        
        MTO.objects.create(username='admin2',email='admin2@mail.com',full_name='ShakeelNawaz',contact_number='+918989208999',
            location="Bangalore",paypal_id='Abc123',password='Varal2021',is_mto=True,job_category = '["cw","de"]')
        mtoadmin = MTO.objects.get(full_name='ShakeelNawaz')
        mtoadmin.set_password('Varal456')
        mtoadmin.save()
        self.client.login(username='admin2',password='Varal456')
        
        Jobs.objects.create(person_name=MTOAdminUser.objects.get(username='varalAdmin'),output='shak3.txt',job_name='NewJob',cat_id='["cw"]',total_budget=5,job_description="na",job_quantity=1,input_folder = 'Shakeel2/nawaz2/team/',target_date='2021-10-25 14:30:59')

        url = reverse('mto:apply',kwargs={'id':2})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,reverse('mto:view'),302,200)

    def test_MTOProfileView2(self):
        url = reverse('mto:profile')
        data = {
        # 'contact_number': '+918553208001',
        # 'location':'India',
        # 'paypal_id':'ABC123',
        # 'job_category':'["de"]',
        }
        response = self.client.post(url,data)
        self.assertEquals(response.status_code, 302)

    def test_signup_form(self):
        url = reverse('mto:sign_up')
        response = self.client.post(url,{})
        self.assertEquals(response.status_code, 200)
        # self.assertTemplateNotUsed(response,"mto/profile.html")



