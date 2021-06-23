from django.shortcuts import render,redirect
from jobs.models import MTOJob,Jobs
from .forms import MTOAdminSignUpForm
from django.contrib import messages
from jobs.forms import JobsForm

def home(request):
    context = {'jobs': MTOJob.objects.all(), }
    return render(request, 'jobs/index.html', context)


def mtoadminsignup(request):
    if request.method == 'POST':
        f = MTOAdminSignUpForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/') # Redirect to Dashboard Page
        else:
            return render(request, 'jobs/admin-register.html', {'form': f})
    context = {
            'jobs': MTOJob.objects.all(),
            'form' : MTOAdminSignUpForm()
             }
    return render(request, 'jobs/admin-register.html', context)
     

def add_job(request):
    if request.method == 'POST':
        form = JobsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Job is Successfully Created !")
        else:
            messages.error(request, "Something went wrong!")
            return render(request, "jobs/jobsform.html", {'form': form})
    context = {'form': JobsForm()}
    return render(request, 'jobs/jobsform.html', context)


def alljobs(request):
    data = Jobs.objects.all().order_by('-id')
    return render(request, 'jobs/jobs.html', {'data': data})
     