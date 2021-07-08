from django.shortcuts import render, redirect
from jobs.forms import MTOAdminSignUpForm
from jobs.models import MTOJob
from django.contrib import messages


# Create your views here.
from super_admin.forms import SuperAdminUpdateProfileForm


def create_mto_admin(request):
    form = MTOAdminSignUpForm()
    if request.method == 'POST':
        form = MTOAdminSignUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_admin = True
            instance.is_active = True
            instance.is_mto = False
            instance.save()
            form.save()
            messages.success(request, f"{instance.full_name} has been created successfully")
            return redirect('jobs:adminDashboard')

    context = {
        'jobs': MTOJob.objects.all(),
        'form': form
    }
    return render(request, 'admin/create-varal-admin.html', context)


def super_admin_profile(request):
    data = {}
    form = SuperAdminUpdateProfileForm(instance=request.user.superadmin)
    if request.method == "POST":
        form = SuperAdminUpdateProfileForm(
            request.POST, instance=request.user.superadmin)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated!")
            # return redirect(request, 'jobs/admin_profile.html')
        else:
            messages.info(request, "sorry profile is not updated!")
            # return redirect(request, 'jobs/admin_profile.html')
    data['form'] = form
    return render(request, 'jobs/admin_profile.html', data)
