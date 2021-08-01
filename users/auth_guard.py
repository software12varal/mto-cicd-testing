import six
from datetime import timedelta
from smtplib import SMTPException
from socket import gaierror

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from jobs.models import AdminLoginAttempt
from mto.models import MTOLoginAttempt

User = get_user_model()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


def send_user_email(user, mail_subject, to_email, current_site):
    message = render_to_string('profiles/auth/email_account_suspended.html', {'user': user, 'domain': current_site.domain,
                                                                    'uid': urlsafe_base64_encode(
                                                                        force_bytes(user.id)),
                                                                    'token': account_activation_token.make_token(
                                                                        user)})
    try:
        send_mail(mail_subject, message, '<youremail>', [to_email])
        return 'success'
    except (ConnectionAbortedError, SMTPException, gaierror):
        return "error"


def prevent_exceeding_login_attempts(username, password, request):
    now = timezone.now()
    try:
        _user = User.objects.get(username=username)

        # get the user's login attempt
        if _user.is_mto:
            login_attempt, created = MTOLoginAttempt.objects.get_or_create(user=_user)
        else:
            login_attempt, created = AdminLoginAttempt.objects.get_or_create(user=_user)

        # limit the time between login attempts and make user to be inactive if login attemps is exceeded.
        if (login_attempt.timestamp + timedelta(seconds=settings.LOGIN_ATTEMPTS_TIME_LIMIT)) < now:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                login_attempt.login_attempts = 0  # reset the login attempts
                login_attempt.save()
                return redirect(settings.LOGIN_REDIRECT_URL)  # change expected_url in your project
            else:
                # if the password is incorrect, increment the login attempts and
                # if login attempts == MAX_LOGIN_ATTEMPTS, set the user to be inactive and send activation email
                login_attempt.login_attempts += 1
                login_attempt.timestamp = now
                login_attempt.save()
                if login_attempt.login_attempts == settings.MAX_LOGIN_ATTEMPTS:
                    _user.is_active = False
                    _user.save()
                    # send the re-activation email
                    mail_subject = "Account suspended"
                    current_site = get_current_site(request)
                    send_user_email(_user, mail_subject, _user.email, current_site)
                    messages.error(request, 'Account suspended, maximum login attempts exceeded. '
                                            'Reactivation link has been sent to your email')
                else:
                    messages.error(request, 'Incorrect username or password')
                return redirect(settings.LOGIN_URL)
        else:
            messages.error(request, 'Login failed, please try again')
            return redirect(settings.LOGIN_URL)
    except ObjectDoesNotExist:
        messages.error(request, 'Incorrect username or password')
        return redirect(settings.LOGIN_URL)
