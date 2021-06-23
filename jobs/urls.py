from django.urls import path
from users.decorators import varal_admin_required
from .views import home,mto_admin_signup,admin_dashboard,admin_profile,mto_bank,microtask_page,mal_requirement,add_job, alljobs

urlpatterns = [
    path('', home, name='home'),
    path('admin-registration/', mto_admin_signup, name='admin_register'),
    path('admin_dashboard', varal_admin_required(admin_dashboard), name='adminDashboard'),
    path('mto_bank', varal_admin_required(mto_bank), name='mto_bank'),
    path('microtask', varal_admin_required(microtask_page), name='microtask'),
    path('requirements', varal_admin_required(mal_requirement), name='requirements'),
    path('admin_profile', varal_admin_required(admin_profile), name='admin_profile'),
    path('addjobs/', add_job, name='add_job'),
    path('alljobs/',alljobs,name='alljobs'),

]
