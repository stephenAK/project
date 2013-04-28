from django.conf.urls.defaults import *
from site_urls.views import *


urlpatterns = patterns('',
                  
		  url(r'^login/$', 'staff_urls.views.do_login'),
		  url(r'^logout/$', 'staff_urls.views.do_logout'),
                  url(r'^doc/$', 'staff_urls.views.doctorPortal'),
		  url(r'^nurse/$', 'staff_urls.views.nursePortal'),
		  url(r'^nurse_pat/$', 'staff_urls.views.nurse_patient'),
		  url(r'^nurse_ref/$', 'staff_urls.views.nurse_referral'),
                  url(r'^pat_details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'staff_urls.views.patient_detail'),
                  url(r'^patient/search/(?P<term>.*?)$','staff_urls.views.patient_search'),
		  
)
  
