# from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from mto.models import MTO


class MTOJobCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MicroTask(models.Model):
    job_name = models.CharField(max_length=300, help_text='e.g develop website')
    cat_id = models.ForeignKey(MTOJobCategory, on_delete=models.CASCADE)
    target_date = models.DateTimeField(null=True, help_text='e.g 2021-10-25 14:30:59')
    job_cost = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="currency AED")
    time_required = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], )
    skills = models.CharField(_('skills'), max_length=500, help_text='e.g coding, data entry')
    people_required = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                                  help_text='number of people required e.g 2')
    job_description = models.CharField(_('job description'), max_length=1000,
                                       help_text='e.g car website', )
    job_sample = models.FileField(upload_to='job_documents/job_samples/', )
    job_instructions = models.FileField(upload_to='job_documents/job_instructions/', )
    tc_type = models.CharField(_('type of tc to be done'), max_length=500,
                               help_text='e.g Senior developer, tester & client')

    def __str__(self):
        return f'{self.job_name}'


class EvaluationStatus(models.Model):
    description = models.ForeignKey(MicroTask, on_delete=models.CASCADE)

    def __str__(self):
        return self.description.job_name


class MTOJob(models.Model):
    job_id = models.ForeignKey(MicroTask, on_delete=models.PROTECT)
    assigned_to = models.IntegerField(help_text='related to MTO')
    due_date = models.DateField()
    assigned_date = models.DateField()
    fees = models.FloatField()
    rating_evaluation = models.IntegerField()
    payment_status = models.IntegerField()  # select a relationship
    completed_date = models.DateField()
    output_path = models.FileField()
    evaluation_status = models.ForeignKey(EvaluationStatus, on_delete=models.CASCADE)

    @property
    def mto(self):
        mto = MTO.objects.filter(id=self.assigned_to).first()
        return mto

    def __str__(self):
        return f"{self.job_id.job_name} :: {self.mto.full_name}"


class MALRequirement(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    identification_number = models.CharField(max_length=50, blank=False, validators=[alphanumeric],
                                             help_text="Mal identification")
    assembly_line_id = models.CharField(max_length=50, blank=False, validators=[alphanumeric])
    assembly_line_name = models.TextField()
    person_name = models.TextField(help_text="Name of the person in charge")
    output = models.FilePathField(path='job_documents/output', help_text="Link of the output folder")
    micro_task = models.ForeignKey(MicroTask, max_length=100, on_delete=models.CASCADE)
    target_date = models.DateField()
    total_budget = models.IntegerField(help_text="Total budget allocated for the job")
    job_description = models.TextField()
    job_sample = models.FileField(upload_to='job sample')
    job_instructions = models.FileField(upload_to='jobs instruction')
    job_quantity = models.IntegerField()
    input_folder = models.FilePathField(path='job_documents/input', help_text="Link of the Input folder")


class MTORoles(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super(MTORoles, self).save(using='varal_job_posting_db')


class MTOAdminUser(User):
    varal_role_id = models.ForeignKey(MTORoles, on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'MTO Admin Users'

    def save(self, *args, **kwargs):
        super(MTOAdminUser, self).save(using='varal_job_posting_db')
