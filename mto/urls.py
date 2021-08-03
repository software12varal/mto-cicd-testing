from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.decorators import mto_required
from mto.views import SignUpView, dummy_home_view,view_jobs,apply_job,job_detail,MTOProfileView,dashboard,view_applied_jobs,\
    view_applied_details, submit_job, notification, recommended_jobs, view_payment_status, view_job_deadline, MTOLoginView
from mto.views import MTOProfileView, SignUpView, apply_job, dashboard, dummy_home_view, forget_password, job_detail, notification, recommended_jobs, reset_password, submit_job, view_applied_details, view_applied_jobs, view_job_deadline, view_jobs, view_payment_status

urlpatterns = [
    path('', mto_required(dummy_home_view), name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', MTOProfileView.as_view(), name='profile'),


    # authentication patterns
    path('register/', SignUpView.as_view(), name='sign_up'),
    # path('login/', LoginView.as_view(template_name='mto/login.html'), name='login'),
    path('login/', MTOLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('viewjob/', mto_required(view_jobs), name='view'),
    path('apply/<int:id>', mto_required(apply_job), name='apply'),
    path('job_detail/<int:slug>', mto_required(job_detail), name='job_detail'),
    path('view-applied-jobs/', mto_required(view_applied_jobs), name='applied'),
    path('view-applied-details/<int:mto_id>/<int:job_id>', mto_required(view_applied_details), name='view_applied_details'),
    path('submit-job/', mto_required(submit_job), name='submit_job'),
    path('notificatons/', mto_required(notification), name='notification'),
    path('recommended-jobs/', mto_required(recommended_jobs), name='recommended_jobs'),
    path('payment-status/', mto_required(view_payment_status), name='view_payment_status'),
    path('view-job-deadline/', mto_required(view_job_deadline), name='job_deadline'),
]
