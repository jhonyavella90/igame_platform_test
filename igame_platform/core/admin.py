# -*- coding: utf-8 -*-
from django.contrib import admin

from igame_platform.core.models import (
    Bonus,
    Account,
    Transaction,
)


class BonusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'bonus_type')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    date_hierarchy = 'modified'


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'trans_type', 'delta')
    date_hierarchy = 'created'


admin.site.register(Bonus, BonusAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
