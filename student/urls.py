from django.conf.urls import patterns, url


urlpatterns = patterns('student.views',
    url(r'^dashboard/$', 'dashboard', name='student_dashboard'),
    url(r'^test/(?P<pk>\d+)/$', 'pass_test', name='student_pass_test'),
    url(r'^test/(?P<pk>\d+)/start/$', 'start_test', name='student_start_test'),
    url(r'^skill/(?P<skill_code>[a-zA-Z0-9_-]+)/$', 'skill_pedagogic_ressources', name='student_skill_pedagogic_ressources'),
)
