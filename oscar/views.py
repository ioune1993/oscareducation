from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def root_redirection(request):

    return HttpResponseRedirect(reverse("username_login"))
