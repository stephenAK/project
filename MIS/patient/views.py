from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django import  forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.xheaders import populate_xheaders
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from site_content.models import *
from patient.models import *







def home(request):
    about = about_us.objects.get(pk=1)
    notPatient = 'galore'
    if request.user.is_staff:
	notPatient = ''
    return render_to_response('medicare/index.html',{'user':request.user,'notPatient':notPatient,'about':about})

def abtUs(request):
    return render_to_response('medicare/about.html',{'user':request.user})

def service(request):
    return render_to_response('medicare/services.html',{'user':request.user})

def contact(request):
    return render_to_response('medicare/contact.html',{'user':request.user})

def news(request):
    return render_to_response('medicare/news.html',{'user':request.user})


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '    Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '    Enter your password'}))

# Login view - @Nana B.
#tested code and it works logs in perfectly
@csrf_exempt
def do_login(request):
	empty_cred = '' #empty login credential variable
	disabled_accMsg = ''
	invalidMsg = ''
	sess_data = ''
	notPatient = ''
        already_logged_in=''#william made changes to your code here...had errors to added this to work
	if request.user.username != '':
		already_logged_in = 'You are already logged in.'
	
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			
			if user is not None:
				if user.is_staff:
	                      		notPatient = 'You are not Supposed to log in here'
					form = LoginForm()
					return render_to_response('medicare/login.html', {
        							  'form': form,
        							  'logged_in': request.user.is_authenticated(),
								  'disabled_accMsg': disabled_accMsg,
								  'invalidMsg': invalidMsg,
								  'empty_cred':empty_cred,
								  'already_logged_in': already_logged_in,
								  'user': request.user,
								  'notPatient' : notPatient
    								  })	
				elif user.is_active:
				
					login(request, user)
					#patient = Patient_vital.objects.get(User_name=uname)
					#request.session["uname_sess"] = uname
					return HttpResponseRedirect('/mis/pat_portal')
			        
				##redirect
				else:
					disabled_accMsg = "Sorry, your account has been disabled. Contact the administrator."
				
				##return a disabled account msg
			else:
				invalidMsg = "Username or Password is invalid!"
			
			#return an invalid login message
	
		#YOUR CODE HERE
	else:
		form = LoginForm()
	form = LoginForm()
	return render_to_response('medicare/login.html', {
        'form': form,
        'logged_in': request.user.is_authenticated(),
	'disabled_accMsg': disabled_accMsg,
	'invalidMsg': invalidMsg,
	'empty_cred':empty_cred,
	'already_logged_in': already_logged_in,
	'user': request.user,
	'notPatient' : notPatient
    })


# Logout view - Nana B.

@csrf_exempt
def do_logout(request):
	if request.user.username != '':
		logout(request)
		request.user.username = ''
		return HttpResponseRedirect('/mis/home')
		
	else:
		return HttpResponseRedirect('/mis/login')
	return render_to_response('medicare/base_logout.html',{'user': request.user})



def appointment(request):
    return  render_to_response('medicare/about.html',{'user':request.user})


def patient_portal(request):
    if request.user.username == '':
	return HttpResponseRedirect('/mis/home')
    try:
    	patUser = User.objects.get(username=request.user.username)
    
    	patient = Patients_vital.objects.get(User_name=patUser.pk)
	
    	return  render_to_response('medicare/pat_portal.html',{'user':request.user,'patient':patient})
    except Patients_vital.DoesNotExist:
	return render_to_response('medicare/base_logout.html',{'user': request.user})


def patient_App(request):
    patUser = User.objects.get(username=request.user.username)
    
    patient = Patients_vital.objects.get(User_name=patUser.pk)
    return  render_to_response('medicare/pat_App.html',{'user':request.user,'patient':patient})


