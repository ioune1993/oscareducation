from django.conf.urls import patterns, url, include


urlpatterns = patterns('authentification.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url('^', include('django.contrib.auth.urls')),
)
