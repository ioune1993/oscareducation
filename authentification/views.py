from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from stats.models import LoginStats

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.haml',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Security check is complete. Log the user in.
            auth_login(request, form.get_user())

            if request.user.is_superuser:
                user_kind = "admin"
            elif hasattr(request.user, "professor"):
                user_kind = "professor"
            elif hasattr(request.user, "student"):
                user_kind = "student"
            else:
                raise Exception("Unknown user kind, can't login")

            LoginStats.objects.create(user=request.user, user_kind=user_kind)

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app)


def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))
