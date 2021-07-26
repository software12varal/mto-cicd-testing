from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from users.forms import MTOAdminAuthenticationForm

from django.urls import reverse
from django.shortcuts import render, redirect


class MTOAdminLoginView(LoginView):
    template_name = 'admin_login.html'
    authentication_form = MTOAdminAuthenticationForm

    # Solves Bug: mto_admin can see the login page even when logged in(when put the url directly)
    def get(self, *args, **kwargs):
        request = self.request
        if request.user.is_authenticated and request.user.is_admin and not request.user.is_mto:
            return redirect(reverse('jobs:adminDashboard'))
        return render(self.request, self.template_name, self.get_context_data())

    def form_valid(self, form):
        print(form.get_user())
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect('/admin_dashboard')
