from django.urls import path

from .views import home,mtoadminsignup

urlpatterns = [
    path('', home, name='home'),
    path('admin-registration/', mtoadminsignup, name='adm-reg'),

]
