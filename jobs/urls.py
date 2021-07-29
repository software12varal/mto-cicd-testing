from django.urls import path
from users.decorators import varal_admin_required
from .views import create_jobs, home, displaying_categories, mto_admin_login, admin_dashboard, add_paymentstatus, add_jobstatus, admin_profile, mto_bank, microtask_page, mal_requirement, \
    add_job, alljobs, view_mto, deleteMto, appliedjobs,admin_monitoring,view_admin,microtask_job_details,displaying_microtask,displaying_files

urlpatterns = [

    # updated
    path('admin-login/', mto_admin_login, name='admin_register'),
    path('admin_dashboard', varal_admin_required(
        admin_dashboard), name='adminDashboard'),
    path('mto_bank', varal_admin_required(mto_bank), name='mto_bank'),
    path('mto_bank', mto_bank, name='mto_bank'),
    path('view_mto/<int:id>', view_mto, name='viewMto'),
    path('deleteMto/<int:id>/', deleteMto, name='deleteMto'),
    path('microtask', varal_admin_required(microtask_page), name='microtask'),
    path('requirements', varal_admin_required(
        mal_requirement), name='requirements'),
    path('admin_profile', varal_admin_required(
        admin_profile), name='admin_profile'),
    path('addjobs/', varal_admin_required(add_job), name='add_job'),
    path('alljobs/', varal_admin_required(alljobs), name='alljobs'),
    path('appliedjobs/', varal_admin_required(appliedjobs), name='appliedjobs'),
    path('add-mal/', varal_admin_required(create_jobs), name='add_mal'),
    path('paymentstatus/<int:job_id>/', add_paymentstatus, name='paymentstatus'),
    path('jobstatus/<int:job_id>/', add_jobstatus, name='jobstatus'),
    path('displaying_categories/', varal_admin_required(displaying_categories),
         name='displaying_categories'),
    path('', home, name='home'),
    path('admin_monitoring/', varal_admin_required(admin_monitoring), name='admin_monitoring'),
    path('view_admin/<int:id>', varal_admin_required(view_admin), name='viewAdmin'),
    path('microtask_job_details/<int:id>',varal_admin_required(microtask_job_details), name='microtask_job_details'),
  
    path('ajax_url/',varal_admin_required(displaying_microtask),
         name='displaying_microtask'),
    path('ajax_url2/',varal_admin_required(displaying_files),
         name='displaying_microtask2'), 
]
