from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#REPORTS
from model_report import report
report.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MIS.views.home', name='home'),
    # url(r'^MIS/', include('MIS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
   # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   # url(r'', include('model_report.urls')),
    url(r'^mis/', include('site_urls.urls')),
    url(r'^pmis/', include('staff_urls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT,}),
)
