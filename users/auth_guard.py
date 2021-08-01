import six
from datetime import timedelta
from smtplib import SMTPException
from socket import gaierror

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from jobs.models import AdminLoginAttempt
from mto.models import MTOLoginAttempt

User = get_user_model()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    used to create hashed tokens for reactivating user accounts when they have
    exceeded settings.MAX_LOGIN_ATTEMPTS. This generates the link to be sent to the
    user via email
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


def send_user_email(user, mail_subject, to_email, current_site):
    """
    We use this function to send emails when a person's account has been
    deactivated due to login attempts exceeding settings.MAX_LOGIN_ATTEMPTS
    """
    is_mto = 0
    if user.is_mto:
        is_mto = 1

    message = render_to_string('email_account_suspended.html', {'user': user, 'domain': current_site.domain,
                                                                    'uid': urlsafe_base64_encode(
                                                                        force_bytes(user.id)),
                                                                    'token': account_activation_token.make_token(
                                                                        user),
                                                                    'mto': is_mto})
    try:
        send_mail(mail_subject, message, '<youremail>', [to_email])
        return 'success'
    except (ConnectionAbortedError, SMTPException, gaierror):
        return "error"


def get_user_from_both_dbs(username):
    """
    Get a User object by trying either in vendor os or varal_job_posting db.
    by using supplied username
    """
    try:
        return User.objects.using('vendor_os_db').get(username=username)
    except User.DoesNotExist:
        try:
            return User.objects.using('varal_job_posting_db').get(username=username)
        except User.DoesNotExist:
            return None


def handle_user_authentication(username, password, request):
    """
    We use this function to handle brute force attack protection in the auth procee.

    When an exceede number of login attempts defined by settings.MAX_LOGIN_ATTEMPTS
    is exceeded, ther user is set to inactive and an email is sent to the user notifying
    him/her of suspecious activity in his account.

    The time between subsequent attempts is also limited by settings.LOGIN_ATTEMPTS_TIME_LIMIT,
    this time is in seconds. So subsequent login attempts will be limited by this time.
    """
    now = timezone.now()
    # Try to get the user using the username (for MTO's) but we use the user args for Admins
    _user = get_user_from_both_dbs(username)
    # _user.is_active = True
    # _user.save()

    if _user is None:
        return "invalid credentials"

    # get the user's login attempt
    if _user.is_mto:
        login_attempt, created = MTOLoginAttempt.objects.get_or_create(user=_user)
    else:
        login_attempt, created = AdminLoginAttempt.objects.get_or_create(user=_user)
    # if it is a new record created, make the last attempt to be 10 minutes ago
    if not login_attempt.timestamp:
        login_attempt.timestamp = timezone.now() - timedelta(minutes=10)
        login_attempt.save()

    # limit the time between login attempts and make user to be inactive if login attemps is exceeded.
    if (login_attempt.timestamp + timedelta(seconds=settings.LOGIN_ATTEMPTS_TIME_LIMIT)) < now:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if login_attempt.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                return 'suspended'
            else:
                login(request, user)
                login_attempt.login_attempts = 0  # reset the login attempts
                login_attempt.save()
                return 'success'
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

                return 'suspended'
            else:
                return "invalid credentials"
    else:
        return "first trial"

