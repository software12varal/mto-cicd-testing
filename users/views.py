from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from users.forms import MTOAdminAuthenticationForm


class MTOAdminLoginView(LoginView):
    template_name = 'admin_login.html'
    authentication_form = MTOAdminAuthenticationForm

    def form_valid(self, form):
        print(form.get_user())
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect('/admin_dashboard')
