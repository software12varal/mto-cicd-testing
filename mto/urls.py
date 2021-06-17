from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.decorators import mto_required
from mto.views import SignUpView, dummy_home_view

urlpatterns = [
    path('', mto_required(dummy_home_view), name='home'),

    # authentication patterns
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(template_name='mto/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
