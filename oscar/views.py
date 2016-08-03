from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def root_redirection(request):
    if hasattr(request.user, "professor"):
        return HttpResponseRedirect(reverse("professor:dashboard"))

    if hasattr(request.user, "student"):
        return HttpResponseRedirect(reverse("student_dashboard"))

    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")

    return HttpResponseRedirect(reverse("login"))
