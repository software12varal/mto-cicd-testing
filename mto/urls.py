from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.decorators import mto_required
from mto.views import SignUpView, dummy_home_view,view_jobs,apply_job,job_detail,MTOProfileView,dashboard

urlpatterns = [
    path('', mto_required(dummy_home_view), name='home'),    
    path('dashboard/',dashboard,name='dashboard'),
    path('profile/',MTOProfileView.as_view(),name='profile'),


    # authentication patterns
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(template_name='mto/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('viewjob/', mto_required(view_jobs), name='view'),
    path('apply/<int:id>', mto_required(apply_job), name='apply'),
    path('job_detail/<int:slug>', mto_required(job_detail), name='job_detail'),
]
