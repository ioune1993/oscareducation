from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def root_redirection(request):
    redirect_to = request.POST.get("next", request.GET.get("next", ''))

    if redirect_to:
        return HttpResponseRedirect(redirect_to)

    if hasattr(request.user, "professor"):
        return HttpResponseRedirect(reverse("professor:dashboard"))

    if hasattr(request.user, "student"):
        return HttpResponseRedirect(reverse("student_dashboard"))

    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")

    return HttpResponseRedirect(reverse("login"))
