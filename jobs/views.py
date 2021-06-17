from django.shortcuts import render
from jobs.models import MTOJob


def home(request):
    context = {'jobs': MTOJob.objects.all(), }
    return render(request, 'jobs/index.html', context)
