# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth import views as auth_views

from igame_platform.accounts import views as account_views
from igame_platform.accounts.decorators import redirect_if_logged_in
from igame_platform.core import views as core_views

urlpatterns = [
    url(
        r'^$',
        redirect_if_logged_in(TemplateView.as_view(template_name='pages/index.html')),
        name='index'
    ),

    # Your stuff: custom urls includes go here
    url(
        r'^login/$', auth_views.login,
        {'template_name': 'accounts/login.html', 'redirect_authenticated_user': True}, name='login'
    ),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', account_views.RegisterView.as_view(), name='register'),
    url(r'^home/$', account_views.home, name='home'),

    # Core app urls
    url(r'^deposit/$', core_views.DepositView.as_view(), name='deposit'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
