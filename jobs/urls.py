from django.urls import path
from users.decorators import varal_admin_required
from .views import home, mto_admin_signup, admin_dashboard, admin_profile,mto_bank, microtask_page, mal_requirement, \
    add_job, alljobs, MALRequirementCreateView,view_mto,deleteMto,appliedjobs,admin_monitoring


urlpatterns = [

    path('admin-registration/', mto_admin_signup, name='admin_register'),
    path('admin_dashboard', varal_admin_required(admin_dashboard), name='adminDashboard'),
    path('mto_bank', varal_admin_required(mto_bank), name='mto_bank'),
    path('mto_bank', mto_bank, name='mto_bank'),
    path('view_mto/<int:id>', view_mto, name='viewMto'),
    path('deleteMto/<int:id>/', deleteMto, name='deleteMto'),
    path('microtask', varal_admin_required(microtask_page), name='microtask'),
    path('requirements', varal_admin_required(mal_requirement), name='requirements'),
    path('admin_profile', varal_admin_required(admin_profile), name='admin_profile'),
    path('addjobs/', varal_admin_required(add_job), name='add_job'),
    path('alljobs/',varal_admin_required(alljobs),name='alljobs'),
    path('appliedjobs/',varal_admin_required(appliedjobs),name='appliedjobs'),
    path('add-mal/', varal_admin_required(MALRequirementCreateView.as_view()), name='add_mal'),
    # path('paymentstatus/<int:job_id>/',add_paymentstatus,name='paymentstatus'),
    path('admin_monitoring/', varal_admin_required(admin_monitoring), name='admin_monitoring'),
    path('', home, name='home'),

]
