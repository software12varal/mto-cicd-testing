# from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from mto.models import MTO
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

def sample_directory_path(instance, filename):
    job = instance.id
    return f"images/job_documents/job_samples/sample_{job}.{filename.split('.')[-1]}"


def instructions_directory_path(instance, filename):
    job = instance.id
    return f"images/job_documents/job_instructions/instructions_{job}.{filename.split('.')[-1]}"


class MicroTask(models.Model):
    type_of_tc = [('M', 'Manual'),
                  ('A', 'Automatic')
                  ]
    # If you are adding job category choice here kindly add in filters.py
    job_category = [
        ('cw', 'Content Writing'),
        ('da', 'Document Analysis'),
        ('de', 'Data Entry'),
        ('cr', 'Combining Rules from Semi-Legal documents'),
        ('df', 'Data Entry(Fields)'),
        ('cd', 'Collecting copies of documents'),
        ('cp', 'Content Copy & Paste'),
        ('cf', 'Combining Data Entry Fields'),
        ('fn', 'Find Non-Copyrighted Images and Uploading'),
        ('ac', 'Apply Compliance to Fields'),
        ('ng', 'Naming'),
        ('ce', 'Compliance Extraction'),
        ('id', 'Identifying One Line Decision'),
        ('ab', 'A+B TC For Document Extraction'),
        ('tc', 'TC For One Line Decision'),
    ]
    # If you are adding job category choice kindly add in filters.py

    microtask_name = models.CharField(
        max_length=300, help_text='e.g develop website')
    microtask_category = models.CharField(
        _('microtask category dropdown'), max_length=2, choices=job_category, default='Content Writing')
    job_cost = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)], help_text="currency AED")
    time_required = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], help_text="In Hours")
    skills = models.CharField(
        _('skills'), max_length=500, help_text='e.g coding, data entry')
    people_required_for_valid_tc = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                                               help_text='number of people required e.g 2')
    sample = models.FileField(
        upload_to=sample_directory_path, default='Onkar_py.txt')
    instructions = models.FileField(
        upload_to=instructions_directory_path, default='Onkar_py.txt')
    tc_type = models.CharField(_('type of tc to be done'), max_length=1, choices=type_of_tc, default='Manual',
                               help_text='e.g Senior developer, tester & client')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.microtask_category}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_sample = self.sample
            saved_instructions = self.instructions
            self.sample = None
            self.instructions = None
            super(MicroTask, self).save(*args, **kwargs)
            self.sample = saved_sample
            self.instructions = saved_instructions
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(MicroTask, self).save(*args, **kwargs)


class EvaluationStatus(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


# class Jobstatus(models.Model):
#     job_status = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.job_status
class AdminRoles(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    # def save(self, *args, **kwargs):
    #     super(AdminRoles, self).save(using='varal_job_posting_db')


class MTOAdminUser(User):
    varal_role_id = models.ForeignKey(AdminRoles, on_delete=models.PROTECT)
    contact_number = PhoneNumberField(blank=True)
    designation = models.CharField(max_length=500, blank=True)
    department = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'MTO Admin Users'

    # def save(self, *args, **kwargs):
    #     super(MTOAdminUser, self).save(using='varal_job_posting_db')


# trial session


class Jobs(models.Model):
    JOB_STATUS = [('cr', 'Created'),
                  ('as', 'Assigned'),
                  ('ur', 'Under review'),
                  ('co', 'Completed'),
                  ]
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    identification_number = models.CharField(
        max_length=50, blank=True, validators=[alphanumeric])
    assembly_line_id = models.CharField(
        max_length=50, blank=True, validators=[alphanumeric])
    assembly_line_name = models.TextField(blank=True)
    person_name = models.ForeignKey(MTOAdminUser, on_delete=models.CASCADE)
    # as per predecesor 2 there is no need of person_email
    # person_email = models.EmailField(null=True)
    output = models.FilePathField(
        path='media/documents/job_documents/output', help_text="Link of the output folder")
    # models.ForeignKey(MicroTask, on_delete=models.CASCADE)
    job_name = models.CharField(
        max_length=300, help_text='e.g develop website')
    cat_id = models.CharField(max_length=50) #models.ForeignKey(MicroTask, on_delete=models.CASCADE)
    target_date = models.DateTimeField(
        null=True, help_text='e.g 2021-10-25 14:30:59')
    total_budget = models.PositiveIntegerField(help_text="e.g currency AED")
    job_description = models.CharField(
        _('job description'), max_length=1000, help_text='e.g car website')
    job_quantity = models.IntegerField(help_text="e.g Quantity of Job")
    input_folder = models.CharField(_("input folder"), max_length=300)
    sample = models.FileField(
        upload_to=sample_directory_path, default='Varal.txt')
    instructions = models.FileField(
        upload_to=instructions_directory_path, default='Varal.txt')
    job_status = models.CharField(
        max_length=100, choices=JOB_STATUS, default="cr")
    updated_date = models.DateTimeField(auto_now=True)
    posted_date = models.DateTimeField(auto_now_add=True)


    @property
    def job(self):
        job = MicroTask.objects.filter(microtask_name=self.job_name).first()
        return job

    def __str__(self):
        return self.job_name

    @property
    def instructions_filename(self):
        return os.path.basename(self.instructions.name)

    @property
    def sample_filename(self):
        return os.path.basename(self.sample.name)


def output_directory_path(instance, filename):
    job = instance.job_id.job_name
    mto = MTO.objects.filter(id=instance.assigned_to).first()
    mto_username = mto.username
    return f"images/job_documents/job_submissions/{mto_username}_{job}.{filename.split('.')[-1]}"


class MTOJob(models.Model):
    JOB_STATUS = [('in', 'in progress'),
                  ('sub', 'submitted'),
                  ('co', 'Completed'),
                  ]
    PAYMENT_CHOICES = [('uninitiated', 'uninitiated'),
                       ('pending', 'pending'),
                       ('paid', 'paid'),
                       ]

    job_id = models.ForeignKey(Jobs, on_delete=models.PROTECT, null=True)
    assigned_to = models.IntegerField(help_text='related to MTO')
    due_date = models.DateTimeField()
    assigned_date = models.DateTimeField(auto_now_add=True)
    fees = models.FloatField()
    updated_date = models.DateTimeField(auto_now=True)  # Submitted
    rating_evaluation = models.IntegerField(null=True)
    payment_status = models.CharField(
        max_length=100, choices=PAYMENT_CHOICES, default="uninitiated")
    job_status = models.CharField(
        max_length=100, choices=JOB_STATUS, default="in")

    completed_date = models.DateTimeField(null=True)
    output_path = models.FileField(upload_to=output_directory_path)
    submitted_date = models.DateTimeField(null=True)
    evaluation_status = models.ForeignKey(
        EvaluationStatus, on_delete=models.CASCADE)

    @property
    def mto(self):
        mto = MTO.objects.filter(id=self.assigned_to).first()
        return mto

    @property
    def average_time(self):
        if self.submitted_date is None:
            time = 0
        else:

            time = self.submitted_date - self.assigned_date
        return time

    @property
    def average_accept_time(self):

        time = self.assigned_date - self.job_id.posted_date
        # context = dict({'days':time.days,'seconds':time.seconds})
        return time

    @property
    def submitted_file_name(self):
        return os.path.basename(self.output_path.name)

    def __str__(self):
        return f"{self.job_id.job_name} :: {self.mto.full_name}"
