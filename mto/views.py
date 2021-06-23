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

# from django.views.generic.base import View
#
# from jobs.models import MALRequirement, MicroTask, MTOJobCategory
from jobs.models import MTOJob
from .forms import SignUpForm
from .models import MTO


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
        user.save()
        domain_name = get_current_site(self.request).domain
        token = str(random.random()).split('.')[1]
        user.token = token
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
        context = {'redirect': '/mto/login'}
        return JsonResponse(context, status=200)

def verify(request,token):
    try:
        user = MTO.objects.get(token=token)
        if user:
            user.is_active = True
            user.save()
            return redirect('/mto/login')
    except:
        print("5")
        msg = "Invalid token"
        return redirect('error.html',{'msg':msg})



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
