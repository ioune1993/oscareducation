from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^auth/', include('authentification.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^professor/', include("promotions.urls")),
    url(r'^student/', include("student.urls")),
    url(r'^$', RedirectView.as_view(pattern_name="login")),
)
