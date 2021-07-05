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


class MicroTask(models.Model):
    type_of_tc = [('M', 'Manual'),
                  ('A', 'Automatic')
                  ]

    microtask_name = models.CharField(max_length=300, help_text='e.g develop website')
    microtask_category = models.CharField(max_length=300)
    job_cost = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="currency AED")
    time_required = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], help_text="In Hours")
    skills = models.CharField(_('skills'), max_length=500, help_text='e.g coding, data entry')
    people_required_for_valid_tc = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                                               help_text='number of people required e.g 2')
    job_sample = models.FileField(upload_to='job_documents/job_samples/', )
    job_instructions = models.FileField(upload_to='job_documents/job_instructions/', )
    tc_type = models.CharField(_('type of tc to be done'), max_length=1, choices=type_of_tc, default='Manual',
                               help_text='e.g Senior developer, tester & client')

    def __str__(self):
        return f'{self.microtask_category}'


@receiver(signal=post_save, sender=MicroTask)
def rename_file(sender, instance, created, **kwargs):
    if created:
        def content_file_name(instance, is_sample=None):
            if is_sample:
                filename = os.path.basename(instance.job_sample.name)
                ext = filename.split('.')[-1]
                filena = "Samples_%s.%s" % (instance.id, ext)
                new_path = os.path.join(settings.MEDIA_ROOT, 'images/job_documents/job_samples/', filena)
                os.rename(instance.job_sample.path, new_path)
                instance.job_sample.name = new_path
                instance.save()
            else:
                filename = os.path.basename(instance.job_instructions.name)
                ext = filename.split('.')[-1]
                filena = "Instructions_%s.%s" % (instance.id, ext)
                new_path = os.path.join(settings.MEDIA_ROOT, 'images/job_documents/job_instructions/', filena)
                os.rename(instance.job_instructions.path, new_path)
                instance.job_instructions.name = new_path
                instance.save()

        content_file_name(instance=instance, is_sample=True)
        content_file_name(instance=instance, is_sample=False)


class EvaluationStatus(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Jobstatus(models.Model):
    job_status = models.CharField(max_length=200)

    def __str__(self):
        return self.job_status


class PaymentStatus(models.Model):
    payment_status = models.CharField(max_length=200)

    def __str__(self):
        return self.payment_status


class Jobs(models.Model):
    Jobstatus = [('cr', 'Created'),
                 ('co', 'Completed'),
                 ('ur', 'Under review'),
                 ('as', 'Assigned')

                 ]
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    identification_number = models.CharField(max_length=50, blank=True, validators=[alphanumeric])
    assembly_line_id = models.CharField(max_length=50, blank=True, validators=[alphanumeric])
    assembly_line_name = models.TextField(blank=True)
    person_name = models.TextField(help_text="Name of the person in charge")
    # as per predecesor 2 there is no need of person_email
    # person_email = models.EmailField(null=True)
    output = models.FilePathField(path='media/documents/job_documents/output', help_text="Link of the output folder")
    job_name = models.CharField(max_length=300,
                                help_text='e.g develop website')  # models.ForeignKey(MicroTask, on_delete=models.CASCADE)
    cat_id = models.ForeignKey(MicroTask, on_delete=models.CASCADE)
    target_date = models.DateTimeField(null=True, help_text='e.g 2021-10-25 14:30:59')
    total_budget = models.PositiveIntegerField(help_text="e.g currency AED")
    job_description = models.CharField(_('job description'), max_length=1000, help_text='e.g car website')
    job_sample = models.FileField(upload_to='images/job_documents/job_samples')
    job_instructions = models.FileField(upload_to='images/job_documents/job_instructions', max_length=100, null=True)
    job_quantity = models.IntegerField(help_text="e.g Quantity of Job")
    input_folder = models.FilePathField(path='media/documents/job_documents/input',
                                        help_text="Link of the Input folder")
    job_status = models.CharField(max_length=100, choices=Jobstatus, default="as")

    def __str__(self):
        return self.job_name


def output_directory_path(instance, filename):
    job = instance.job_id.job_name
    mto = MTO.objects.filter(id=instance.assigned_to).first()
    mto_username = mto.username
    return f"images/job_documents/job_submissions/{mto_username}_{job}.{filename.split('.')[-1]}"


class MTOJob(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.PROTECT, null=True)
    assigned_to = models.IntegerField(help_text='related to MTO')
    due_date = models.DateTimeField()
    assigned_date = models.DateTimeField(auto_now_add=True)
    fees = models.FloatField()
    rating_evaluation = models.IntegerField(null=True)
    payment_status = models.ForeignKey(PaymentStatus, verbose_name=_("payment status"), on_delete=models.CASCADE,
                                       null=True)
    job_status = models.ForeignKey(Jobstatus, verbose_name=_("job status"), on_delete=models.CASCADE,
                                   null=True)
    completed_date = models.DateTimeField(null=True)
    output_path = models.FileField(upload_to=output_directory_path)
    is_submitted = models.BooleanField(default=False)
    evaluation_status = models.ForeignKey(EvaluationStatus, on_delete=models.CASCADE)

    @property
    def mto(self):
        mto = MTO.objects.filter(id=self.assigned_to).first()
        return mto

    @property
    def average_time(self):
        if self.completed_date is None:
            time = 0
        else:

            time = self.completed_date - self.assigned_date
            # try:
            #     if time.days >= 1:
            #         days = time
            #     else:
            #         days = 1
            # except:
            #     if self.completed_date == self.assigned_date:
            #         days = 1
            #     else:
            #         days = 0
        return time

    @property
    def average_accept_time(self):

        time = self.assigned_date - self.job_id.posted_date
        # context = dict({'days':time.days,'seconds':time.seconds})
        return time

    def __str__(self):
        return f"{self.job_id.job_name} :: {self.mto.full_name}"


class AdminRoles(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    # def save(self, *args, **kwargs):
    #     super(AdminRoles, self).save(using='varal_job_posting_db')


class MTOAdminUser(User):
    varal_role_id = models.ForeignKey(AdminRoles, on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'MTO Admin Users'

    # def save(self, *args, **kwargs):
    #     super(MTOAdminUser, self).save(using='varal_job_posting_db')

# trial session
