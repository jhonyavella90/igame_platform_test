# -*- coding: utf-8 -*-
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'igame_platform.accounts'
    verbose_name = 'accounts'

    def ready(self):
        import igame_platform.accounts.signals  # noqa
