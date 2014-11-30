from django.conf.urls import patterns, url


urlpatterns = patterns('promotions.views',
    url(r'^dashboard/$', 'dashboard', name='professor_dashboard'),
    url(r'^lesson/(?P<pk>\d+)/$', 'lesson_detail_view', name='professor_lesson_detail_view'),
    url(r'^student/(?P<pk>\d+)/$', 'student_detail_view', name='professor_student_detail_view'),
)
