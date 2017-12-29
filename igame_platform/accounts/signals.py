# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from igame_platform.core.models import Account
from igame_platform.core.models import Bonus


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.create(instance)


# Using the built-in login signal to trigger a login bonus
@receiver(user_logged_in)
def trigger_login_bonus(sender, user, request, **kwargs):

    if user.is_staff or user.is_superuser:
        return

    Bonus.apply_bonus(Bonus.EVENT_TYPES.login, user)
