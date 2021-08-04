from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View

from jobs.models import AdminLoginAttempt
from mto.models import MTOLoginAttempt
from users.auth_guard import account_activation_token, handle_user_authentication, get_user_from_both_dbs
from users.forms import MTOAdminAuthenticationForm

from django.urls import reverse
from django.shortcuts import render, redirect

User = get_user_model()


class MTOAdminLoginView(View):
    template_name = 'admin_login.html'
    authentication_form = MTOAdminAuthenticationForm

    def get_context_data(self):
        context = {"form": self.authentication_form}
        return context

    # Solves Bug: mto_admin can see the login page even when logged in(when put the url directly)
    def get(self, *args, **kwargs):
        request = self.request
        if request.user.is_authenticated and request.user.is_admin and not request.user.is_mto:
            return redirect(reverse('jobs:adminDashboard'))
        return render(self.request, self.template_name, self.get_context_data())

    def post(self, *args, **kwargs):
        # login(self.request, form.get_user())
        request = self.request
        form = self.authentication_form(request.POST)
        # print('THE USR FROM FORM>>>>', form.get_user())
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            response = handle_user_authentication(username, password, request)
            if response == "success":
                return redirect(reverse('jobs:adminDashboard'))
            elif response == "invalid credentials":
                messages.error(request, 'Incorrect username or password')
            elif response == 'first trial':
                messages.error(request, 'Login failed, please try again')
            elif response == 'suspended':
                messages.error(request, 'Account suspended, maximum login attempts exceeded. '
                                        'Reactivation link has been sent to your email')
        return render(self.request, self.template_name, self.get_context_data())
        # return redirect(settings.LOGIN_URL)


def recover_suspended_account_view(request, uidb64, token, mto):
    "We use this function to reactivate users accounts when they have exceeded login attemps"
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        if mto == 1:
            user = User.objects.using('vendor_os_db').get(id=uid)
        else:
            user = User.objects.using('varal_job_posting_db').get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        if user.is_mto:
            login_attempt, created = MTOLoginAttempt.objects.get_or_create(user=user)
        else:
            login_attempt, created = AdminLoginAttempt.objects.get_or_create(user=user)

        # reset the login attempts
        login_attempt.login_attempts = 0
        login_attempt.save()
        messages.success(request, 'Account restored, you can now proceed to login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect(settings.LOGIN_URL)
