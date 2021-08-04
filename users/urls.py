from django.urls import path
from .views import MTOAdminLoginView, recover_suspended_account_view

urlpatterns = [
    path('admin-login/', MTOAdminLoginView.as_view(), name='admin_login'),
    path('account-reactivation/<slug:uidb64>/<slug:token>/<int:mto>/', recover_suspended_account_view, name='reactivate_account'),
]