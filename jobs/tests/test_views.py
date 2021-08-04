from django.conf import settings
from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from jobs.models import MTOAdminUser, AdminRoles, Jobs, MTOJob, MTO, MicroTask
from super_admin.models import SuperAdmin  #
from users.models import User


class JobsTestDbMixin:
    settings.UNDER_TESTING = True
    databases = {"varal_job_posting_db", "vendor_os_db"}


class TestViews(JobsTestDbMixin, TestCase):
    def setUp(self):
        MicroTask.objects.create(microtask_name="NewJob", microtask_category='["cw","de"]', skills="GK",
                                 people_required_for_valid_tc=1, tc_type='["M"]')

        role = AdminRoles.objects.create(description="tester")
        instance = MTOAdminUser.objects.create(email='admin@gmail.com', is_admin=True, is_active=True,
                                               varal_role_id=role,
                                               full_name='varalAdmin', username='bonnie')
        instance.set_password('1234')
        instance.save()

        super = SuperAdmin.objects.create(email='a@gmail.com', is_admin=True, is_active=True, is_super_admin=True,
                                          full_name='Super Admin', username='super')
        super.set_password('1234')
        super.save()

        MTO.objects.create(username='Alexa', email='admin@mail.com', full_name='Alexa',
                           contact_number='+919876543210',
                           location="Pune", paypal_id='Abc123', password='Varal2021', is_mto=True,
                           job_category='["cw","de"]', token='p0o9i8u7y6')
        data = MTO.objects.get(username='Alexa')
        data.set_password('1234')
        data.save()
        Jobs.objects.create(person_name=MTOAdminUser.objects.get(username='bonnie'), output='shak.txt',
                            job_name='NewJob', cat_id='["cw"]', total_budget=5, job_description="na", job_quantity=1,
                            input_folder='Shakeel/nawaz/')

        MTOJob.objects.create(job_id=Jobs.objects.get(id=1), assigned_to=1, due_date='2021-10-25 14:30:59', fees=500,
                              output_path='Nawaz.txt')

        return self.client.login(username='bonnie', password='1234')

    def test_login_test(self):
        user = auth.get_user(self.client)
        self.assert_(user.is_authenticated, 'Not Authenticated')

    def test_home_GET(self):
        url = reverse('jobs:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_home2_GET(self):
        self.client.logout()
        url = reverse('jobs:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/index.html')

    def test_add_job(self):
        url = reverse('jobs:add_job')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/jobsform.html')

    def test_add_job_2(self):
        url = reverse('jobs:add_job')
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/jobsform.html')

    def test_add_paymentstatus(self):
        url = reverse('jobs:paymentstatus', kwargs={'job_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_add_paymentstatus_2(self):
        url = reverse('jobs:paymentstatus', kwargs={'job_id': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 302)

    def test_add_jobstatus(self):
        url = reverse('jobs:jobstatus', kwargs={'job_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_add_jobstatus_2(self):
        url = reverse('jobs:jobstatus', kwargs={'job_id': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 302)

    def test_appliedjobs(self):
        url = reverse('jobs:appliedjobs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_appliedjobs_2(self):
        self.client.logout()
        self.client.login(username='super', password='1234')
        url = reverse('jobs:appliedjobs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_alljobs(self):
        url = reverse('jobs:alljobs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_alljobs_2(self):
        self.client.logout()
        self.client.login(username='super', password='1234')
        url = reverse('jobs:alljobs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_microtask_job_details(self):
        url = reverse('jobs:microtask_job_details', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_admin_dashboard(self):
        url = reverse('jobs:adminDashboard')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/admin_dashboard.html')

    def test_mto_bank(self):
        url = reverse('jobs:mto_bank')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/MTOBank.html')

    def test_view_mto(self):
        url = reverse('jobs:viewMto', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/view_mto.html')

    def test_admin_profile(self):
        url = reverse('jobs:admin_profile')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/admin_profile.html')

    def test_admin_profile_1(self):
        # self.client.logout()
        # self.client.login(username='super', password='1234')
        url = reverse('jobs:admin_profile')
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_create_jobs(self):
        url = reverse('jobs:add_mal')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/mal_requirement_creation.html')

    def test_create_jobs_2(self):
        self.client.logout()
        self.client.login(username='super', password='1234')
        url = reverse('jobs:add_mal')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/mal_requirement_creation.html')

    def test_create_jobs_3(self):
        url = reverse('jobs:add_mal')
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/mal_requirement_creation.html')

    def test_microtask_page(self):
        url = reverse('jobs:microtask')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/Microtask.html')

    def test_mal_requirement(self):
        url = reverse('jobs:requirements')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/MAL_requirement.html')

    def test_deleteMto(self):
        url = reverse('jobs:deleteMto', kwargs={'id': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 302)

    def test_view_admin(self):
        url = reverse('jobs:viewAdmin', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/view_admin.html')

    def test_admin_monitoring(self):
        url = reverse('jobs:admin_monitoring')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/admin_monitoring.html')

    # def test_displaying_categories(self):
    #     url = reverse('jobs:displaying_categories')
    #     response = self.client.get(url)
    #     print(f'hey--------------------{response}')
    #     self.assertEquals(response.status_code, 200)

    def test_displaying_microtask(self):
        url = reverse('jobs:displaying_microtask')
        response = self.client.get(url, {'cat_ide': 'cw'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/cat_name.html')

    def test_displaying_files(self):
        url = reverse('jobs:displaying_microtask2')
        response = self.client.get(url, {'jb_name': 'NewJob'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/cat_name.html')
