from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^accounts/', include('authentification.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^professor/', include("promotions.urls", namespace="professor")),
    url(r'^student/', include("student.urls")),
    url(r'^stats/', include("stats.urls", namespace="stats")),
    #url(r'^$', views.root_redirection, name="home"),
    url(r'^$', views.home, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
