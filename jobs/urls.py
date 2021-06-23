from django.urls import path

from .views import home,mtoadminsignup,add_job, alljobs

urlpatterns = [
    path('', home, name='home'),
    path('admin-registration/', mtoadminsignup, name='adm-reg'),
    path('addjobs/', add_job, name='add_job'),
    path('alljobs/',alljobs,name='alljobs'),

]
