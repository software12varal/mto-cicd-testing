from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class VaralOSDBAuthBackend(BaseBackend):
    """
    To authenticate users using also varal os db
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.using('vendor_os_db').get(username=username)
            return user if user.check_password(password) else None
        except User.DoesNotExist:
            try:
                user = User.objects.using('varal_job_posting_db').get(username=username)
                return user if user.check_password(password) else None
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.using('vendor_os_db').get(pk=user_id)
        except User.DoesNotExist:
            try:
                return User.objects.using('varal_job_posting_db').get(pk=user_id)
            except User.DoesNotExist:
                return None