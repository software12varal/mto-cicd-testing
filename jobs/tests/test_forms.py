from django.test import TestCase
from jobs.forms import JobsForm


class add_jobs_test(TestCase):
    def test_forms(self):
       
        form_data = {'identification_number':'webdev','assembly_line_id':'webdev','assembly_line_name':'webdev','person_name':'','output':'','job_name':'website','cat_id':'','target_date':'2021-10-25 14:30:59','total_budget':'22','job_description':'develop website','job_quantity':'3','input_folder':'','sample':'','instructions':''}

