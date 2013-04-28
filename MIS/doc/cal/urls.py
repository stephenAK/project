from django.conf.urls.defaults import *
from cal.models import *

urlpatterns = patterns('cal.views',
    (r"^month/(\d+)/(\d+)/(prev|next)/$", "month"),
    (r"^month/(\d+)/(\d+)/$", "month"),
    (r"^month$", "month"),
    (r"^day/(\d+)/(\d+)/(\d+)/$", "day"),
    (r"^settings/$", "settings"),
    (r"^(\d+)/$", "main"),
    (r"", "main"),
)
