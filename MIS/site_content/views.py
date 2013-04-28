from django.shortcuts import render_to_response
from models import about_us
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader

from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.xheaders import populate_xheaders
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model



def about_US(request):
      about = about_us.objects.get(pk=1)
      return render_to_response('medicare/index.html',{'about':about})

