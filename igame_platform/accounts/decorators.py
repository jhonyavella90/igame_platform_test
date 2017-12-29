# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.urls import reverse


def redirect_if_logged_in(function):
    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated():
            return redirect(reverse('home'))

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
