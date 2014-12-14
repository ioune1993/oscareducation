from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('oscar.views',
    url(r'^accounts/', include('authentification.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^professor/', include("promotions.urls")),
    url(r'^student/', include("student.urls")),
    url(r'^$', 'root_redirection', name="home"),
)
