# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from igame_platform.core.models import Account
from igame_platform.core.forms import DepositForm


class DepositView(FormView):
    template_name = 'core/deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DepositView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        amount = form.cleaned_data.get('deposit_amount')
        Account.deposit(self.request.user, amount)
        return super(DepositView, self).form_valid(form)
