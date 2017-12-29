# -*- coding: utf-8 -*-
from decimal import Decimal

from django import forms


class DepositForm(forms.Form):
    deposit_amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
