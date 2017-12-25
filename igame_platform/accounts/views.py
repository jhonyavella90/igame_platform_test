# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views.generic.edit import FormView

from igame_platform.accounts.forms import RegisterForm


@login_required
def home(request):
    return render(request, 'accounts/home.html')


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = '/home/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)
