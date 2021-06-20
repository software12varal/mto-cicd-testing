from django.shortcuts import render,redirect
from jobs.models import MTOJob
from .forms import MTOAdminSignUpForm

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