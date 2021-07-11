from django.urls import path
from users.decorators import super_admin_required
from super_admin.views import create_mto_admin, super_admin_profile

urlpatterns = [

    path('create-admin/', super_admin_required(create_mto_admin), name="create_admin"),
    path('super_admin_profile/', super_admin_required(super_admin_profile), name='super_admin_profile'),

]
