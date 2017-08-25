# encoding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url, redirect, render, get_object_or_404
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from stats.models import LoginStats

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from users.models import Professor
from django.db import transaction
from django.contrib import messages


from forms import UsernameLoginForm, CodeForm, CreatePasswordForm, SubscribeTeacherForm
from django.core.mail import send_mail
from users.models import Student, Professor

@sensitive_post_parameters()
@csrf_protect
@never_cache

# TODO: TO DELETE
# def root_redirection(request):
#     """
#     Whenever a user tries to access the main page, this view will look at its status and redirect him
#     to the corresponding page.
#     :param request:
#     :return:
#     """
#     redirect_to = request.POST.get("next", request.GET.get("next", ''))
#
#     if redirect_to:
#         return HttpResponseRedirect(redirect_to)
#
#     if request.user.is_superuser:
#         return HttpResponseRedirect("/admin/")
#
#     if hasattr(request.user, "professor"):
#         return HttpResponseRedirect(reverse("professor:dashboard"))
#
#     if hasattr(request.user, "student"):
#         return HttpResponseRedirect(reverse("student_dashboard"))
#
#     return HttpResponseRedirect(reverse("login"))

def username(request, template_name='registration/login_username.haml',
             redirect_field_name=REDIRECT_FIELD_NAME,
             usernamelogin_form=UsernameLoginForm,
             current_app=None, extra_context=None) :
    """
    Displays the username form and handles the login action.
    """
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")

    if hasattr(request.user, "professor"):
        return HttpResponseRedirect(reverse("professor:dashboard"))

    if hasattr(request.user, "student"):
        return HttpResponseRedirect(reverse("student_dashboard"))


    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        form = usernamelogin_form(request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            user = form.cleaned_data['username']
            return is_pending(request,user)
    else:
        form = usernamelogin_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }

    return TemplateResponse(request, template_name, context,
                        current_app)

def pending_teacher(request):
    if request.method == "POST":
        if User.objects.filter(email=request.POST['email']):
            user = User.objects.get(email=request.POST['email'])
            if Professor.objects.filter(user_id=user.id):
                professor = Professor.objects.get(user_id=user.id)
                if professor.is_pending:
                    domain = request.META['HTTP_HOST']
                    url = "http://{}/accounts/confirmteacher/{}".format(domain, user.id)
                    body = "Bonjour, suivez ce lien pour confirmer votre inscription : {}".format(url)
                    send_mail(u'Votre inscription a bien été enregistrée.', body, 'noreply@oscar.education',
                        [request.POST['email']], fail_silently=False)
                    messages.add_message(request, messages.SUCCESS, "Un email a bien été renvoyé à {}".format(request.POST['email']))
                else:
                    messages.add_message(request, messages.ERROR, "Ce compte est déjà actif !")
        else:
            messages.add_message(request, messages.ERROR, "Cette adresse e-mail n'est associée à aucun compte !")
    return render(request, 'registration/pending_teacher.haml', locals())

def confirm_teacher(request, user_id):
    user = get_object_or_404(Professor, user_id=user_id, is_pending=True)
    user.is_pending = False
    user.save()
    messages.add_message(request, messages.SUCCESS, "Votre compte a été activé, vous pouvez désormais vous connecter.")
    return HttpResponseRedirect(reverse('username_login'))

def is_pending(request, user):
    """
    Redirect the user either to :
    - code page if he needs to create a password (by giving his code first)
    - password page if he already has a password
    """

    if user[0].is_pending:
        if isinstance(user[0], Student):
            request.session['user'] = user[1]
            return HttpResponseRedirect(reverse('code_login'))
        elif isinstance(user[0], Professor):
            request.session['user'] = user[1]
            return HttpResponseRedirect(reverse('pending_teacher'))
    else:
        request.session['user'] = user[1]
        return HttpResponseRedirect(reverse('password_login'))

def password(request, template_name='registration/login_password.haml',
             redirect_field_name=REDIRECT_FIELD_NAME,
             authentication_form=AuthenticationForm,
             current_app=None, extra_context=None) :

    """
    Displays the password form and handles the login action.
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
                LoginStats.objects.create(user=request.user, user_kind="admin")
                return HttpResponseRedirect("/admin/")
            elif hasattr(request.user, "professor"):
                LoginStats.objects.create(user=request.user, user_kind="professor")
                return HttpResponseRedirect(reverse("professor:dashboard"))
            elif hasattr(request.user, "student"):
                LoginStats.objects.create(user=request.user, user_kind="student")
                return HttpResponseRedirect(reverse("student_dashboard"))
            else:
                raise Exception("Unknown user kind, can't login")
    else:
        form = authentication_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'user': request.session['user'],
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app)

def code(request, template_name='registration/login_code.haml',
             redirect_field_name=REDIRECT_FIELD_NAME,
             code_form=CodeForm,
             current_app=None, extra_context=None) :

    """
    Displays the authentication-code form and handles the login action.
    """

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = code_form(request.POST)
        if form.is_valid():
            # Once the code has been verified in the form, allow the user to create its password.
            return HttpResponseRedirect(reverse('create_password'))

    else:
        form = code_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'user': request.session['user'],
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app)

def create_password(request, template_name='registration/create_password.haml',
                    redirect_field_name=REDIRECT_FIELD_NAME,
                    cp_form=CreatePasswordForm,current_app=None, extra_context=None):

    """
    Displays the password creation form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        form = cp_form(request.POST)
        if form.is_valid():
            # Once the code has been verified in the form, allow the user to create its password.
            prof_or_stud = form.cleaned_data['username'][0]
            user = prof_or_stud.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            prof_or_stud.is_pending = False
            prof_or_stud.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('username_login'))
    else:
        form = cp_form()


    current_site = get_current_site(request)
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'user': request.session['user'],
    }
    return TemplateResponse(request, template_name, context, current_app)

def subscribe_teacher(request):
    if request.method == "POST":
        form = SubscribeTeacherForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.generate_teacher_username()
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            registration_number = form.cleaned_data["registration_number"]

            with transaction.atomic():
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)
                prof = Professor.objects.create(user=user, code=registration_number, is_pending=True)
                # Send email to confirm and thus set is_pending to True instead of False ?
            domain = request.META['HTTP_HOST']
            url = "http://{}/accounts/confirmteacher/{}".format(domain, user.id)
            body = "Bonjour, merci de votre inscription sur Oscar ! Votre nom d'utilisateur est {}" \
                   ". Pour finaliser votre inscription, veuillez suivre ce lien : {}".format(username, url)
            send_mail(u'Votre inscription a bien été enregistrée.', body, 'noreply@oscar.education',
                      [request.POST['email']], fail_silently=False)
            messages.add_message(request, messages.SUCCESS,
                                 "Veuillez consulter votre boite mail ({}) pour activer votre compte.".format(request.POST['email']))
            return HttpResponseRedirect(reverse('username_login'))

    return render(request,'registration/subscribe_teacher.haml', locals())

def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))

# TODO : TO DELETE
# def login(request, template_name='registration/login.haml',
#           redirect_field_name=REDIRECT_FIELD_NAME,
#           authentication_form=AuthenticationForm,
#           current_app=None, extra_context=None):
#     """
#     Displays the login form and handles the login action.
#     """
#     redirect_to = request.POST.get(redirect_field_name,
#                                    request.GET.get(redirect_field_name, ''))
#
#     if request.method == "POST":
#         form = authentication_form(request, data=request.POST)
#         if form.is_valid():
#
#             # Ensure the user-originating redirection url is safe.
#             if not is_safe_url(url=redirect_to, host=request.get_host()):
#                 redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
#
#             # Security check is complete. Log the user in.
#             auth_login(request, form.get_user())
#
#             if request.user.is_superuser:
#                 user_kind = "admin"
#             elif hasattr(request.user, "professor"):
#                 user_kind = "professor"
#             elif hasattr(request.user, "student"):
#                 user_kind = "student"
#             else:
#                 raise Exception("Unknown user kind, can't login")
#
#             LoginStats.objects.create(user=request.user, user_kind=user_kind)
#             return HttpResponseRedirect(redirect_to)
#     else:
#         form = authentication_form(request)
#
#     current_site = get_current_site(request)
#
#     context = {
#         'form': form,
#         redirect_field_name: redirect_to,
#         'site': current_site,
#         'site_name': current_site.name,
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return TemplateResponse(request, template_name, context,
#                             current_app)
