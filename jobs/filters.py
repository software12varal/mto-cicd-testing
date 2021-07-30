from django.db.models.base import Model
import django_filters
from .models import *
from django import forms

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


class JobsFilterForSuperadmin(django_filters.FilterSet):
    cat_id = django_filters.ChoiceFilter(choices=job_category, widget=forms.Select, label='Category name')

    class Meta:
        model = Jobs
        fields = {
            'cat_id': ['exact'],
            'person_name': ['exact'],

        }


class JobsFilterForVaraladmin(django_filters.FilterSet):
    cat_id = django_filters.ChoiceFilter(choices=job_category, widget=forms.Select, label='Category name')

    class Meta:
        model = Jobs

        fields = ['cat_id']


class OngoingJobsFilterForSuperadmin(django_filters.FilterSet):
    cat = MTO.objects.all()
    job_name = Jobs.objects.all()
    job_id__cat_id = django_filters.ChoiceFilter(choices=job_category, widget=forms.Select, label='Category name')

    class Meta:
        model = MTOJob

        fields = {
            'job_id__cat_id': ['exact'],
            'job_id__person_name': ['exact']

        }

        # fields = ['job_id__cat_id', 'assigned_to', 'job_id__name']


class OngoingJobsFilterForadmin(django_filters.FilterSet):
    cat = MTOJob.objects.all()
    # job = Jobs.objects.filter(id__in = [c.job_id_id for c in cat])
    job_id__cat_id = django_filters.ChoiceFilter(choices=job_category, widget=forms.Select, label='Category name')

    class Meta:
        model = MTOJob

        fields = ['job_id__cat_id']
