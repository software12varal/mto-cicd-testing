from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from jobs.models import MTOJob, Jobs
from .forms import MTOAdminSignUpForm, MALRequirementForm
from django.contrib import messages
from jobs.forms import JobsForm

from jobs.models import MTOJob, MicroTask, MTOAdminUser
from .forms import MTOAdminSignUpForm, AdminUpdateProfileForm


def home(request):
    context = {'jobs': MTOJob.objects.all(), }
    return render(request, 'jobs/index.html', context)


def mto_admin_signup(request):
    if request.method == 'POST':
        f = MTOAdminSignUpForm(request.POST)
        if f.is_valid():
            instance = f.save(commit=False)
            instance.is_admin = True
            instance.is_active = True
            instance.is_mto = False
            instance.save()
            f.save()
            return redirect('/admin-login')  # Redirect to Dashboard Page
        else:
            return render(request, 'jobs/admin-register.html', {'form': f})
    context = {
        'jobs': MTOJob.objects.all(),
        'form': MTOAdminSignUpForm()
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


def admin_dashboard(request):
    print(request.user)
    return render(request, 'jobs/admin_dashboard.html')


def mto_bank(request):
    return render(request, 'jobs/MTOBank.html')


def microtask_page(request):
    context = {'jobs': MicroTask.objects.all(), }
    return render(request, 'jobs/Microtask.html', context)


def mal_requirement(request):
    context = {'jobs': MicroTask.objects.all(), }
    return render(request, 'jobs/MAL_requirement.html', context)


def admin_profile(request):
    data = {}
    form = AdminUpdateProfileForm(instance=request.user.mtoadminuser)
    if request.method == "POST":
        form = AdminUpdateProfileForm(request.POST, instance=request.user.mtoadminuser)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated!")
            # return redirect(request, 'jobs/admin_profile.html')
        else:
            messages.info(request, "sorry profile is not updated!")
            # return redirect(request, 'jobs/admin_profile.html')
    data['form'] = form
    return render(request, 'jobs/admin_profile.html', data)


class MALRequirementCreateView(CreateView):
    form_class = MALRequirementForm
    template_name = 'jobs/mal_requirement_creation.html'

    def get_form_kwargs(self):
        kwargs = super(MALRequirementCreateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        context = {'message': f" {instance.micro_task}, has been created successfully."}
        return JsonResponse(context, status=200)
