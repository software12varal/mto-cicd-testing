from django.urls import path
from .views import MTOAdminLoginView

urlpatterns = [
    path('admin-login/', MTOAdminLoginView.as_view(), name='admin_login'),
]