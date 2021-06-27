from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views import View
from django.conf import settings
import random
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from users.decorators import mto_required
from django.template.context import RequestContext
import json
# from django.views.generic.base import View
#
# from jobs.models import MALRequirement, MicroTask, MTOJobCategory
from jobs.models import MTOJob, Jobstatus, PaymentStatus, MALRequirement, Jobs
from users.models import User
from .forms import SignUpForm
from .models import MTO
from mto.forms import MTOUpdateProfileForm
from datetime import datetime
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'mto/register.html'

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
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
        user = form.save(commit=False)
        context = {}
        if User.objects.using('varal_job_posting_db').filter(username=user.username).exists():
            messages.info(self.request, f"{user.username} exists in varal job posting db")
        elif User.objects.using('vendor_os_db').filter(username=user.username).exists():
            messages.info(self.request, f"{user.username} exists in vendor os db")
        else:
            domain_name = get_current_site(self.request).domain
            token = str(random.random()).split('.')[1]
            user.token = token
            # user.is_mto = True
            # user.is_active = False
            user.save()
            link = f'http://{domain_name}/verify/{token}'
            send_mail(
                'Verify your email',
                f'Click on this {link} to verify your account.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False

            )
            messages.success(self.request, f"Hi {user.full_name}, your account was created successfully.")
            context['redirect'] = '/mto/login'
        return JsonResponse(context, status=200)


def verify(request, token):
    try:
        user = MTO.objects.get(token=token)
        if user:
            user.is_active = True
            user.save()
            return redirect('/mto/login')
    except:
        print("5")
        msg = "Invalid token"
        return redirect('error.html', {'msg': msg})


# class SignUpView(View):
#     template_name = 'mto/register.html'
#
#     def get(self, *args, **kwargs):
#         form = SignUpForm
#         context = {'form': form}
#         return render(self.request, self.template_name, context)
#
#     def post(self, *args, **kwargs):
#         # check if there's need to handle race condition when creating users
#         form = SignUpForm(self.request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect(reverse('account_login'))


def dummy_home_view(request):
    mtos = MTO.objects.all()
    jobs_applied = MTOJob.objects.all()
    for job in jobs_applied:  # testing mto foreignkey
        print(job.mto.full_name)
    context = {'mtos': mtos}
    return render(request, 'mto/index.html', context)


@login_required
@mto_required
def dashboard(request):
    mtos = MTO.objects.get(id=request.user.id)
    jobs = MTOJob.objects.filter(assigned_to=request.user.mto.id)
    jobs_status = Jobstatus.objects.all()
    jobpayment = PaymentStatus.objects.all()
    jobs_accepted = jobs_status.filter(job_status_name='Assigned').count()
    jobs_completed = jobs_status.filter(job_status_name='Completed').count()
    jobs_submitted = jobs_status.filter(job_status_name='Approved').count()
    jobs_item = jobs.all()
    total = 0
    # totals = jobs_item.aggregate(Sum('fees'))['fees__sum']
    # total = '{:0.2f}'.format(totals)
    context = {'jobs': jobs, 'jobs_accepted': jobs_accepted, 'jobs_status': jobs_status,
               'jobs_completed': jobs_completed, 'jobs_submitted': jobs_submitted, 'jobpayment': jobpayment,
               'total': total}

    return render(request, 'mto/mto_dashboard.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(mto_required, name='dispatch')
class MTOProfileView(View):
    template_name = 'mto/profile.html'
    context_object_name = 'mto'
    form = MTOUpdateProfileForm

    def get(self, *args, **kwargs):
        mto = MTO.objects.get(id=self.request.user.id)
        self.form = MTOUpdateProfileForm(instance=mto)

        # we get the items from string type to list type and get the users job categories
        jsonDec = json.decoder.JSONDecoder()
        mto_preferred_categories = jsonDec.decode(mto.job_category)
        job_categories = [MALRequirement.objects.get(id=job_id) for job_id in mto_preferred_categories]

        context = {self.context_object_name: mto, 'form': self.form, 'job_categories': job_categories}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            phone = form.cleaned_data['contact_number']
            location = form.cleaned_data['location']
            paypal = form.cleaned_data['paypal_id']

            # convert the job categories to a list then save them as a JSON string in the database.
            job_categories = form.cleaned_data['job_category']
            job_categories_ids = json.dumps([job.id for job in job_categories])

            # update our fields in the database
            MTO.objects.filter(id=self.request.user.id).update(contact_number=phone, location=location,
                                                               job_category=job_categories_ids, paypal_id=paypal)
            messages.success(self.request, 'Changes saved successfully')
        return redirect(reverse('mto:profile'))


# def microtask(request):
#     if request.method == 'POST':
#         form = MicroTaskForm(request.POST, request.FILES)
#         if form.is_valid():
#
#             job_name = form.cleaned_data['job_name']
#
#             form.save()
#             messages.success(request, f'Account created for {job_name}! You have to login')
#             return redirect('/')
#     else:
#         form = MicroTaskForm()
#
#     return render(request, 'microtask.html', {'form': form})
#
#
# def index(request):
#     microtask = MicroTask.objects.all()
#     # category = MAL_Requirements.objects.get(microtask.Category_of_the_microtask)
#
#     context = {'microtask':microtask,
#
#                 }
#     return render(request, 'MalForm.html', context)
#
# def handleSubmit(request):
#     if request.method == 'POST':
#         MAL_Job_Identification_Number = request.POST['malno']
#         Assembly_line_ID = request.POST['asi']
#         Name_of_the_Assembly_line = request.POST['nameassembly']
#         Name_of_the_person_incharge_of_the_MAL = request.POST['personname']
#         Link_of_the_output_folder = request.POST['link1']
#         Name_of_the_micro_task = request.POST['microtask']
#         Category_of_the_Microtask = request.POST['category']
#         Target_date = request.POST['td']
#         Total_budget_allocated_for_the_job = request.POST['budget']
#         Job_description = request.POST['jd']
#         Upload_job_sample = request.POST['jobsample']
#         Upload_Job_instructions = request.POST['instruction']
#         Quantity_of_the_Job = request.POST['quantity']
#         Link_of_the_Input_folder = request.POST['link2']
#
#         job = MicroTask.objects.get(id=Name_of_the_micro_task)
#         cat = MTOJobCategory.objects.get(id=Category_of_the_Microtask)
#
#         data = MALRequirement(MAL_Job_Identification_Number=MAL_Job_Identification_Number, Assembly_line_ID=Assembly_line_ID,
#                                 Name_of_the_Assembly_line=Name_of_the_Assembly_line, Name_of_the_person_incharge_of_the_MAL=Name_of_the_person_incharge_of_the_MAL, Link_of_the_output_folder=Link_of_the_output_folder,
#                                 microtask=job, microtask_category=cat, Target_date=Target_date, Total_budget_allocated_for_the_job=Total_budget_allocated_for_the_job,Job_description=Job_description,
#                                 Uploadjob_sample=Upload_job_sample, UploadJob_instructions=Upload_Job_instructions, Quantity_of_the_Job=Quantity_of_the_Job, Link_of_the_Input_folder=Link_of_the_Input_folder)
#         data.save()
#     return redirect('index')
#
# def posting_page(request,pk=None):
#     #if request.user.is_active:
#     if pk is not None:
#         try:
#             data = MicroTask.objects.get(id=pk)
#         except:
#             data = "NA"
#         return render(request,'JobPosting_Page.html', {'datas': data})
#     return render(request,'JobPosting_Page.html')
# def jobsmto(request):
#     if request.user.is_authenticated and request.user.is_mto:# and not request.user.is_admin :
#         job = Jobs.objects.filter(target_date__gte=datetime.now()).all()
#         # job = Jobs.objects.filter(target_date__gte=datetime.now() and people_required__lt=MTOJob.objects.filter(job_id=id).Count()).all()
#         mto = MTOJob.objects.values('job_id').order_by('job_id').annotate(count=Count('job_id'))
#         ls = []
#         # print(ls)
#         for i in job:
#             for j in range(len(mto)):
#                 if i.id == mto[j]['job_id']:
#                     if i.people_required <= mto[j]['count']:
#                         ls.append(i.id)
#         job = Jobs.objects.filter(target_date__gte=datetime.now()).exclude(id__in=set(ls)).all()
#         return render(request,'mto/mtojobs.html',{'data':job})
#     else:
#         return redirect('mto:login')


def view_jobs(request):  # MTO view all
    if request.user.is_authenticated and request.user.is_mto:  # and not request.user.is_admin :
        job = Jobs.objects.filter(target_date__gte=datetime.now()).all()
        mto = MTOJob.objects.values('job_id').order_by('job_id').annotate(count=Count('job_id'))
        ls = []
        for i in job:
            for j in range(len(mto)):
                if i.id == mto[j]['job_id']:
                    if i.people_required <= mto[j]['count']:
                        ls.append(i.id)
        ujob = Jobs.objects.filter(target_date__gte=datetime.now()).exclude(id__in=set(ls)).all()
        # q1 = Jobs.objects.filter(target_date__gte=datetime.now()).all()
        p = Paginator(ujob, 5)
        page_num = request.GET.get('page')
        try:
            data = p.page(page_num)
        except PageNotAnInteger:
            data = p.page(1)
        except EmptyPage:
            data = p.page(p.num_pages)
        return render(request, 'mto/mto_viewjob.html', {'data': data})


def job_detail(request, slug):
    job_details = Jobs.objects.get(id=slug)
    return render(request, 'mto/apply_job.html', {'job_details': job_details})


def apply_job(request, id):
    job_details = Jobs.objects.get(id=id)
    assigned_to = request.user.mto.id
    due_date = job_details.target_date
    assigned_date = datetime.now()
    fees = job_details.job_cost
    apply = MTOJob(job_id=job_details, assigned_to=assigned_to, evaluation_status_id=2, due_date=due_date,
                   assigned_date=assigned_date,
                   fees=fees)
    apply.save()
    messages.success(request, "Applied Successfully !")
    return redirect('mto:view')
