from django.conf.urls.defaults import *
from site_urls.views import *


urlpatterns = patterns('',
                  url(r'^home/$', 'site_urls.views.home'),
		  url(r'^aboutUs/$', 'site_urls.views.abtUs'),
		  url(r'^services/$', 'site_urls.views.service'),
                  url(r'^contact/$', 'site_urls.views.contact'),
		  url(r'^news/$', 'site_urls.views.news'),
		  url(r'^login/$', 'site_urls.views.do_login'),
                  url(r'^app/$', 'site_urls.views.appointment'),
		  url(r'^pat_portal/$', 'site_urls.views.patient_portal'),
		  url(r'^pat_App/$', 'site_urls.views.patient_App'),
		  url(r'^logout/$', 'site_urls.views.do_logout'),
		  url(r'^req_App/$', 'site_urls.views.request_App'),
		  url(r'^scheduled_App/$', 'site_urls.views.scheduled_App'),

		  
)
  
