from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.decorators import mto_required
from mto.views import SignUpView, dummy_home_view,view_jobs,apply_job,job_detail,MTOProfileView,dashboard,view_applied_jobs, view_applied_details, submit_job

urlpatterns = [
    path('', mto_required(dummy_home_view), name='home'),    
    path('dashboard/',dashboard,name='dashboard'),
    path('profile/',MTOProfileView.as_view(),name='profile'),


    # authentication patterns
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(template_name='mto/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('viewjob/', mto_required(view_jobs), name='view'),
    path('apply/<int:id>', mto_required(apply_job), name='apply'),
    path('job_detail/<int:slug>', mto_required(job_detail), name='job_detail'),
    path('view-applied-jobs/', mto_required(view_applied_jobs), name='applied'),
    path('view-applied-details/<int:mto_id>/<int:job_id>', mto_required(view_applied_details), name='view_applied_details'),
    path('submit-job/', mto_required(submit_job), name='submit_job'),
]
