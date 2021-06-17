from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def mto_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='mto:login'):
    """
    Decorator for views that checks that the logged in user is an MTO,
    redirects to the MTO's log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_mto,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
