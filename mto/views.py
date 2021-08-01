from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views import View
from django.conf import settings
import random
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from users.auth_guard import handle_user_authentication
from users.decorators import mto_required
from django.utils import timezone
from django.template.context import RequestContext
import json
# from django.views.generic.base import View
#
# from jobs.models import MALRequirement, MicroTask, MTOJobCategory
from jobs.models import MTOJob, Jobs, MicroTask
from users.models import User
from .forms import SignUpForm
from .models import MTO
from mto.forms import MTOUpdateProfileForm
from datetime import datetime, timedelta
from django.db.models import Count, Sum
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
            # messages.info(self.request, f"{user.username} exists in varal job posting db")
            context['info'] = f"{user.username} exists in varal job posting db"
        elif User.objects.using('vendor_os_db').filter(username=user.username).exists():
            # messages.info(self.request, f"{user.username} exists in vendor os db")
            context['info'] = f"{user.username} exists in vendor os db"
        else:
            job_categories = form.cleaned_data['job_category']
            job_categories_ids = json.dumps([job for job in job_categories])
            domain_name = get_current_site(self.request).domain
            token = str(random.random()).split('.')[1]
            user.token = token
            user.is_mto = True
            user.is_active = False
            user.job_category = job_categories_ids
            user.save()
            link = f'http://{domain_name}/verify/{token}'
            send_mail(
                'Verify your email',
                f'Click on this {link} to verify your account.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False

            )
            messages.success(
                self.request, f"Hi {user.full_name}, your account was created successfully.")
            context['redirect'] = '/mto/login'
        return JsonResponse(context, status=200)


class MTOLoginView(View):
    template_name = 'mto/login.html'
    form = AuthenticationForm

    def get(self, *args, **kwargs):
        context = {'form': self.form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        request = self.request
        form = self.form(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            response = handle_user_authentication(username, password, request)
            if response == "success":
                return redirect(reverse('mto:dashboard'))
            elif response == "invalid credentials":
                messages.error(request, 'Incorrect username or password')
            elif response == 'first trial':
                messages.error(request, 'Login failed, please try again')
            elif response == 'suspended':
                messages.error(request, 'Account suspended, maximum login attempts exceeded. '
                                        'Reactivation link has been sent to your email')
        context = {'form': form}
        return render(self.request, self.template_name, context)


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
    JOB_STATUS = [('in', 'in progress'),
                  ('sub', 'submitted'),
                  ('co', 'Completed'),

                  ]
    jobs = MTOJob.objects.filter(assigned_to=request.user.mto.id)
    job_progress = MTOJob.objects.filter(
        assigned_to=request.user.mto.id, job_status='in').count()
    jobs_submitted = MTOJob.objects.filter(
        assigned_to=request.user.mto.id, job_status='sub').count()
    jobs_completed = MTOJob.objects.filter(
        assigned_to=request.user.mto.id, job_status='co').count()
    if MTOJob.objects.filter(job_status='co'):
        totals = jobs.aggregate(Sum('fees'))['fees__sum'] or 0
        total = '{:0.2f}'.format(totals)
    else:
        total = 0
    context = {'jobs': jobs, 'jobs_submitted': jobs_submitted,
               'jobs_completed': jobs_completed, 'total': total}

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
        job_categories = []
        # we get the items from string type to list type and get the users job categories
        jsonDec = json.decoder.JSONDecoder()
        mto_preferred_categories = jsonDec.decode(mto.job_category)
        for i in MicroTask.job_category:
            for j in mto_preferred_categories:
                if j in i:
                    job_categories.append(i)

        print(job_categories)
        context = {self.context_object_name: mto,
                   'form': self.form, 'job_categories': job_categories}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            phone = form.cleaned_data['contact_number']
            location = form.cleaned_data['location']
            paypal = form.cleaned_data['paypal_id']

            # convert the job categories to a list then save them as a JSON string in the database.
            job_categories = form.cleaned_data['job_category']
            job_categories_ids = json.dumps([job for job in job_categories])

            # update our fields in the database
            MTO.objects.filter(id=self.request.user.id).update(contact_number=phone, location=location,
                                                               job_category=job_categories_ids, paypal_id=paypal)
            messages.success(self.request, 'Changes saved successfully')
        return redirect(reverse('mto:profile'))


def view_jobs(request):  # MTO view all
    # and not request.user.is_admin :
    if request.user.is_authenticated and request.user.is_mto:
        job = Jobs.objects.all()
        mt = list(MTOJob.objects.values('job_id').order_by(
            'job_id').annotate(count=Count('job_id')))
        # ADDED BY SHAKEEL

        # ls = list(map(lambda x, y: x if 10 <= y else 0,
        #               list(map(lambda x: x['job_id'], mt)), list(map(lambda x: x['count'], mt))))

        ls = list(map(lambda x, y: x if (Jobs.objects.get(id=x).job_quantity * MicroTask.objects.get(
            microtask_name=Jobs.objects.get(id=x).job_name).people_required_for_valid_tc) <= y else 0,
            list(map(lambda x: x['job_id'], mt)), list(map(lambda x: x['count'], mt))))

        # ls = list(map(lambda x, y: x if Jobs.objects.get(id=x) <= y else 0,
        #               list(map(lambda x: x['job_id'], mt)), list(map(lambda x: x['count'], mt))))

        ujob = Jobs.objects.filter(
            target_date__gte=datetime.now()).exclude(id__in=set(ls)).all()
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


# This code can be refactored further using an if statement
# Email notifications to MTO_admin
def email_notification_job_applied(request):
    # link = f'http://{domain_name}/verify/{token}'
    email = EmailMessage(
        'Job applied',
        'User has applied for job',
        settings.EMAIL_HOST_USER,
        # [request.user.profile.email]
        ['software8@varaluae.com'],
    )

    email.fail_silently = False
    return email.send()


# Email notifications to MTO_admin; add it to apply job function

def email_notification_job_submit(request):
    email = EmailMessage(
        'Job ',
        'User has submitted the job',
        settings.EMAIL_HOST_USER,
        # [request.user.profile.email]
        ['software8@varaluae.com'],
    )

    email.fail_silently = False
    return email.send()


def apply_job(request, id):
    if MTOJob.objects.filter(job_id_id=id, assigned_to=request.user.mto.id).exists():
        messages.warning(request, "Already Applied to this Job !")
        return redirect('mto:view')
    else:
        job_details = Jobs.objects.get(id=id)
        microtask = MicroTask.objects.get(microtask_name=job_details.job_name)
        print(microtask)
        assigned_to = request.user.mto.id
        due_date = job_details.target_date
        assigned_date = datetime.now()
        fees = microtask.job_cost
        apply = MTOJob(job_id=job_details, assigned_to=assigned_to, due_date=due_date,
                       assigned_date=assigned_date,
                       fees=fees)
        apply.save()
        job_details.job_status = "as"
        job_details.save()
        messages.success(request, "Applied Successfully !")
        email_notification_job_applied(request)
        return redirect('mto:view')


def view_applied_jobs(request):
    mtos = MTO.objects.get(id=request.user.id)
    jobs = MTOJob.objects.filter(
        assigned_to=request.user.mto.id).order_by('-assigned_date')

    context = {'jobs': jobs}
    return render(request, 'mto/appliedjobs.html', context)


def view_applied_details(request, mto_id, job_id):
    mtos = MTO.objects.get(id=mto_id)
    details = MTOJob.objects.filter(
        job_id=job_id, assigned_to=mto_id).first()
    mtoss = mtos.full_name

    context = {'mto': mtos, 'details': details}
    return render(request, 'mto/applied_jobs_details.html', context)


def submit_job(request):
    mto = MTO.objects.get(id=request.user.mto.id)

    # jobs = MTOJob.objects.get(assigned_to=request.user.mto.id)
    if request.method == 'POST':
        job_id = request.POST.get("job_id")
        output_path = request.FILES.get('file1','NA') #['file1']
        Jobs.objects.filter(id=job_id).first()
        if MTOJob.objects.filter(job_id_id=job_id, job_status='sub', assigned_to=mto.id).exists():
            messages.info(request, f'You already submitted')
        elif MTOJob.objects.filter(job_id_id=job_id, job_status='co', assigned_to=mto.id).exists():
            messages.info(request, f'You already submitted')
        else:
            instance = MTOJob.objects.filter(
                job_id_id=job_id, assigned_to=mto.id).first()
            instance.output_path = output_path
            instance.job_status = 'sub'
            instance.submitted_date = timezone.now()
            instance.save()
            messages.success(request, f'Job successfully submitted')
            email_notification_job_submit(request)

        return redirect('mto:applied')


def notification(request):
    return render(request, 'mto/notification.html')


def recommended_jobs(request):
    mto = MTO.objects.get(id=request.user.id)
    print(mto.id)
    jsonDec = json.decoder.JSONDecoder()
    mto_preferred_categories = jsonDec.decode(mto.job_category)
    print(mto_preferred_categories)
    print(type(mto_preferred_categories))
    # job_categories = [Jobs.objects.get(id=job_id) for job_id in mto_preferred_categories]
    # print(job_categories)
    all_job = Jobs.objects.filter(cat_id__in=[job_id for job_id in mto_preferred_categories],
                                  target_date__gte=datetime.now())
    print(all_job)
    context = {'jobs': all_job}
    return render(request, 'mto/recommended_jobs.html', context)


def view_payment_status(request):
    job_payment_status = MTOJob.objects.filter(assigned_to=request.user.id)
    context = {'jobs': job_payment_status}
    return render(request, 'mto/view_payment_status.html', context)


def view_job_deadline(request):
    due_date = timezone.now() + timedelta(hours=4)
    due_jobs = MTOJob.objects.filter(assigned_to=request.user.id, due_date__gte=timezone.now(
    ), due_date__lte=due_date, job_status='in').order_by('-due_date')
    context = {'jobs': due_jobs}
    return render(request, 'mto/job_deadline.html', context)
