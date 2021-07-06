from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from jobs.models import MTOJob, Jobs
from .forms import MTOAdminSignUpForm, JobForm
from django.contrib import messages
from jobs.forms import JobsForm

from jobs.models import MTOJob, MicroTask, MTOAdminUser
from .forms import MTOAdminSignUpForm, AdminUpdateProfileForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mto.models import MTO
from .models import Jobstatus
from functools import reduce
import json


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


def add_paymentstatus(request, job_id):
    instance = MTOJob.objects.filter(id=job_id).first()

    if request.method == 'POST':
        payment_id = request.POST['payment_status']
        instance.payment_status = payment_id
        instance.save()
        messages.success(request, "Payment Status updated")

    return redirect('jobs:appliedjobs')


def add_jobstatus(request, job_id):
    instance = MTOJob.objects.filter(id=job_id).first()
    if request.method == 'POST':
        status_id = request.POST['job_status']
        instance.job_status = status_id
        instance.save()
        messages.success(request, "Job Status updated")

    return redirect('jobs:appliedjobs')


def appliedjobs(request):
    job = MTOJob.objects.all().order_by('-id')
    p = Paginator(job, 5)
    page_num = request.GET.get('page')
    try:
        data = p.page(page_num)
    except PageNotAnInteger:
        data = p.page(1)
    except EmptyPage:
        data = p.page(p.num_pages)
    return render(request, 'jobs/appliedjobs.html', {'data': data})


def alljobs(request):
    jobs = Jobs.objects.all().order_by('-id')
    p = Paginator(jobs, 5)
    page_num = request.GET.get('page')
    try:
        data = p.page(page_num)
    except PageNotAnInteger:
        data = p.page(1)
    except EmptyPage:
        data = p.page(p.num_pages)
    return render(request, 'jobs/jobs.html', {'data': data})


def admin_dashboard(request):
    print(request.user)
    return render(request, 'jobs/admin_dashboard.html')


def mto_bank(request):
    mto = MTO.objects.all()
    context = {'mto': mto}

    return render(request, 'jobs/MTOBank.html', context)


def convert_seconds(performance):
    if performance >= 60:
        minutes = performance / 60
        if minutes == 1:
            time = f"{round(minutes)} minute"
        else:
            time = f"{round(minutes)} minutes"
        if minutes >= 60:
            hours = minutes / 60
            if hours >= 60:
                time = f"{round(hours)} hour"
            else:
                time = f"{round(hours)} hours"
    else:
        time = performance
    return time


def convert_days(performance_days):
    if performance_days > 1:
        performance_days = f"{round(performance_days)} days"
        control = True
    else:
        if performance_days == 1:
            performance_days = f"{round(performance_days)} day"
            control = True
        else:
            performance_days = f"{round(performance_days)} day"
            control = False
    context = {'time': performance_days, 'status': control}
    return context


def percentage(mto_job, total_job, total_completed):
    if total_completed is None:
        percentage_accept = (int(mto_job) / int(total_job) * 100)
        percentage_accept = round(percentage_accept)
    else:
        percentage_accept = (int(total_completed) / int(mto_job) * 100)
        percentage_accept = round(percentage_accept)
    return percentage_accept


def view_mto(request, id):
    mto = MTO.objects.get(pk=id)
    mto_job = MTOJob.objects.filter(assigned_to=id)

    days_list = [0]
    seconds_list = [0]
    for i in mto_job:
        if i.average_time is not 0:
            days_list.append(i.average_time.days)
            seconds_list.append(i.average_time.seconds)
    length = len(days_list) - 1
    # performance in days
    performance = reduce(lambda x, y: x + y, days_list)

    try:
        performance_days = round(performance / length)
    except ZeroDivisionError:
        performance_days = 0
    performance_days = convert_days(performance_days)

    # performance in seconds
    performance = reduce(lambda x, y: x + y, seconds_list)
    try:
        performance = performance / length
    except ZeroDivisionError:
        performance = 0
    performance_seconds = convert_seconds(performance)

    #  acceptance time calculating
    days = [0]
    seconds = [0]
    for i in mto_job:
        seconds.append(i.average_accept_time.seconds)
        days.append(i.average_accept_time.days)
    mto_job = MTOJob.objects.filter(assigned_to=id).count()
    accept_days = reduce(lambda x, y: x + y, days)
    try:
        accept_day = round(accept_days / mto_job)
        accept_days = convert_days(accept_day)
    except ZeroDivisionError:
        accept_days = 0
    final_date = reduce(lambda x, y: x + y, seconds)
    try:
        accept_date = final_date / mto_job
        accept_seconds = convert_seconds(accept_date)
    except ZeroDivisionError:
        accept_seconds = 0
    mto_job = MTOJob.objects.filter(assigned_to=id).count()
    total_completed = MTOJob.objects.filter(
        completed_date__isnull=False, assigned_to=id).count()
    total_job = Jobs.objects.all().count()

    # cat_list = []
    # list(
    #     map(lambda i: i if i == '[' or i == ',' or i == ']' or i == " " else cat_list.append(int(i)), mto.job_category))
    # print(cat_list)
    # jobs = list(map(lambda i: i if i == '[' or i == ',' or i == ']' or i == " " else {
    #     'name': Jobs.objects.filter(cat_id=i).first()}, cat_list))
    # print(jobs.count('name'))

    try:
        percentage_acceptance = percentage(
            mto_job=mto_job, total_job=total_job, total_completed=None)
    except ZeroDivisionError:
        percentage_acceptance = 0
    try:
        percentage_completeness = percentage(
            mto_job=mto_job, total_job=None, total_completed=total_completed)
    except ZeroDivisionError:
        percentage_completeness = 0
    context = {'mto': mto, 'mto_job': mto_job, 'completed': total_completed,
               'percentage_completeness': percentage_completeness,
               'percentage_acceptance': percentage_acceptance,
               'accept_days': accept_days, 'accept_seconds': accept_seconds,
               'performance_days': performance_days, 'performance_seconds': performance_seconds}
    return render(request, 'jobs/view_mto.html', context)


def deleteMto(request, id):
    if request.method == "POST":
        mto = MTO.objects.get(pk=id)
        mto.delete()
        messages.success(request, f"Deleted successfully")
    return redirect('jobs:mto_bank')


def microtask_page(request):
    context = {'jobs': MicroTask.objects.all(), }
    return render(request, 'jobs/Microtask.html', context)


def mal_requirement(request):
    context = {'jobs': Jobs.objects.all(), }
    return render(request, 'jobs/MAL_requirement.html', context)


def admin_profile(request):
    data = {}
    form = AdminUpdateProfileForm(instance=request.user.mtoadminuser)
    if request.method == "POST":
        form = AdminUpdateProfileForm(
            request.POST, instance=request.user.mtoadminuser)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated!")
            # return redirect(request, 'jobs/admin_profile.html')
        else:
            messages.info(request, "sorry profile is not updated!")
            # return redirect(request, 'jobs/admin_profile.html')
    data['form'] = form
    return render(request, 'jobs/admin_profile.html', data)


def create_jobs(request):
    context = {}
    context['form'] = JobForm
    if request.method == 'POST':

        form = JobForm(request.POST)
        print(request.POST.get('identification_number'))
        sample = request.FILES.get('sample')
        instructions = request.FILES.get('instructions')

        if instructions and sample is not None:
            identification_number = request.POST.get('identification_number')
            assembly_line_id = request.POST.get('assembly_line_id')
            assembly_line_name = request.POST.get('assembly_line_name')
            person_name = request.POST.get('person_name')
            output = request.POST.get('output')
            job_name = request.POST.get('job_name')
            cat_id = request.POST.get('cat_id')
            target_date = request.POST.get('target_date')
            total_budget = request.POST.get('total_budget')
            job_description = request.POST.get('job_description')
            job_quantity = request.POST.get('job_quantity')
            input_folder = request.POST.get('input_folder')
            job_status = request.POST.get('job_status')

            instance = Jobs.objects.create(identification_number=identification_number, assembly_line_id=assembly_line_id,
                                           assembly_line_name=assembly_line_name, person_name=person_name,
                                           job_name=job_name, cat_id_id=cat_id, target_date=target_date, total_budget=total_budget,
                                           job_description=job_description, job_quantity=job_quantity, job_status=job_status)
            instance.output = output
            instance.input_folder = input_folder
            instance.save()
            messages.success(request, 'Form Has Been Submited Successfully !')
            print(request.POST.get('identification_number'))
            instance = MicroTask.objects.get(id=cat_id)
            instance.sample = sample
            instance.instructions = instructions
            print(sample)
            instance.save()
        else:
            identification_number = request.POST.get('identification_number')
            assembly_line_id = request.POST.get('assembly_line_id')
            assembly_line_name = request.POST.get('assembly_line_name')
            person_name = request.POST.get('person_name')
            output = request.POST.get('output')
            job_name = request.POST.get('job_name')
            cat_id = request.POST.get('cat_id')
            target_date = request.POST.get('target_date')
            total_budget = request.POST.get('total_budget')
            job_description = request.POST.get('job_description')
            job_quantity = request.POST.get('job_quantity')
            input_folder = request.POST.get('input_folder')
            job_status = request.POST.get('job_status')

            instance = Jobs.objects.create(identification_number=identification_number, assembly_line_id=assembly_line_id,
                                           assembly_line_name=assembly_line_name, person_name=person_name,
                                           job_name=job_name, cat_id_id=cat_id, target_date=target_date, total_budget=total_budget,
                                           job_description=job_description, job_quantity=job_quantity, job_status=job_status)
            instance.output = output
            instance.input_folder = input_folder
            instance.save()
            messages.success(request, 'Form Has Been Submited Successfully !')
            print(request.POST.get('identification_number'))
    return render(request, 'jobs/mal_requirement_creation.html', context)

# class MALRequirementCreateView(CreateView):
#     form_class = JobForm
#     template_name = 'jobs/mal_requirement_creation.html'

#     def get_form_kwargs(self):
#         kwargs = super(MALRequirementCreateView, self).get_form_kwargs()
#         return kwargs

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_invalid(self, form):
#         return JsonResponse(form.errors, status=200)

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.save()
#         context = {'message': f" {instance.job_name}, has been created successfully."}
#         return JsonResponse(context, status=200)


def admin_monitoring(request):
    jobs = Jobs.objects.all()
    submitted_jobs = MTOJob.objects.all().count()
    completed_jobs = MTOJob.objects.all().count()
    rejected_jobs = MTOJob.objects.all().count()
    Job_payment = MTOJob.objects.all().count()
    No_of_mtos_working_onjobs = MTOJob.objects.all().count()
    Number_of_Ongoing_Jobs = MTOJob.objects.all().count()
    Approved_amount_per_job = MTOJob.objects.all().count()
    Job_TITLE = MTOJob.objects.all()
    Job_category = MTOJob.objects.all()
    date_of_posting = MTOJob.objects.all()

    context = {'jobs': jobs, 'submitted_jobs': submitted_jobs, 'completed_jobs': completed_jobs, 'rejected_jobs': rejected_jobs, 'Job_payment': Job_payment, 'No_of_mtos_working_onjobs': No_of_mtos_working_onjobs,
               'Number_of_Ongoing_Jobs': Number_of_Ongoing_Jobs, 'Approved_amount_per_job': Approved_amount_per_job, 'Job_TITLE': Job_TITLE, 'Job_category': Job_category, 'date_of_posting': date_of_posting}

    return render(request, 'jobs/admin_monitoring.html', context)


def displaying_categories(request):
    context = {}
    data = json.loads(request.body.decode("utf-8"))
    cat_id = data['cat_id']
    try:
        cat_id = int(cat_id)
        category = MicroTask.objects.filter(id=cat_id).first()
        context['sample'] = category.sample.url
        context['instructions'] = category.instructions.url
        context['message'] = f"{category.microtask_name}, has been selected"
    except ValueError:
        print("Select something please")
    return JsonResponse(context)
