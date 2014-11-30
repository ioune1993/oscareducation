from django.conf.urls import patterns, url


urlpatterns = patterns('promotions.views',
    url(r'^dashboard/$', 'dashboard', name='professor_dashboard'),
)
