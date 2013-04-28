# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django import  forms 
from django.forms import ModelForm
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
from django.contrib.auth.decorators import login_required
from site_content.models import *
from patient.models import *
from appointment.models import *
from staff.models import *
import datetime
from datetime import date

staff_uname=''

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '    Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '    Enter your password'}))


@csrf_exempt
def do_login(request):
	
	empty_cred = '' #empty login credential variable
	disabled_accMsg = ''
	invalidMsg = ''
	sess_data = ''
	notPatient = ''
        already_logged_in = ''#william made changes to your code here...had errors to added this to work
	
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			
			if user is not None:
				if user.is_active and user.is_staff:
					try:
						
						ID = User.objects.get(username=uname)	
						doc = Doctor.objects.get(Pmis_id=ID)
						if doc is not None:
							
							login(request, user)
							request.session["staff_uname"] = uname
	                      				return HttpResponseRedirect('/pmis/doc')
					except Doctor.DoesNotExist:
						pass
					
					try:
					       
						ID = User.objects.get(username=uname)	
						nurse = Nurse.objects.get(Pmis_id=ID)
						if nurse is not None:
							
							login(request, user)
							request.session["staff_uname"] = uname
	                      				return HttpResponseRedirect('/pmis/nurse')
					except Nurse.DoesNotExist:
						pass	
					
						
						
						
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
	return  render_to_response('staff/login.html',{
        'form': form,
        'logged_in': request.user.is_authenticated(),
	'disabled_accMsg': disabled_accMsg,
	'invalidMsg': invalidMsg,
	'empty_cred':empty_cred,
	'already_logged_in': already_logged_in,
	'user': request.user,
        
    })



# Logout view - Nana B.

@csrf_exempt
def do_logout(request):
	try:
    		if request.session["staff_uname"] != staff_uname:
			logout(request)
			request.session["staff_uname"] = ''
			return HttpResponseRedirect('/pmis/login')
    
		else:
			return HttpResponseRedirect('/pmis/login')
		#return render_to_response('staff/.html',{'user': request.user})

        except KeyError:
		logout(request)
		request.session["staff_uname"] = ''
		return HttpResponseRedirect('/pmis/login')


def doctorPortal(request):
	return  render_to_response('staff/doc.html',{'user':request.user})

#NURSE PORTAL HTMLS
def nursePortal(request):
        
        numberOfPat = PatientImmunisation.objects.filter(administrator__username__icontains = request.user.username)
        numberSeenToday = PatientImmunisation.objects.filter(administrator__username__icontains = request.user.username, vaccination_date = date.today())
        MaleSeenToday = PatientImmunisation.objects.filter(administrator__username__icontains = request.user.username, vaccination_date = date.today(), patient__sex = "Male")
        FemaleSeenToday = PatientImmunisation.objects.filter(administrator__username__icontains = request.user.username, vaccination_date = date.today(), patient__sex = "Female")
        aboveAvg = Patient_vitals.objects.filter(body_temp__gt = 37.3, date_created = date.today())
        totalNumber = Patient_vitals.objects.filter(date_created = datetime.datetime.now())
        n1 = float(aboveAvg.count())
        n2 = int(totalNumber.count())
        if n2 != 0:
             percent = (n1/n2) * 100
        else:
             percent = 0
               # number_vital = Patient_vitals.objects.filter (administrator__username__icontains = request.user.username)
             
        
	return  render_to_response('staff/nurse.html',{'MaleSeenToday':MaleSeenToday,
							'percent':percent,
							'FemaleSeenToday':FemaleSeenToday,
							'numberSeenToday':numberSeenToday,
							'numberOfPat':numberOfPat,
							'totalNumber':totalNumber,
							'aboveAvg':aboveAvg,
							'user':request.user})
def patient_search(request, term):
	if request.GET.get('search_item','') != '':
		term = request.GET.get('search_item','')
	patient = Patient_detail.objects.filter(hospital_ID__icontains=term)| Patient_detail.objects.filter(first_Name__icontains=term)|Patient_detail.objects.filter(other_Name__icontains=term)
	return render_to_response('staff/patient_search.html',{'patient':patient,'term':term,'user':request.user})

def nurse_patient(request):
        patients =  Patient_detail.objects.all()
	return  render_to_response('staff/Nurse_patient.html',{'patients':patients,'user':request.user})

class demoForm(ModelForm):
      class Meta:
            model = PatientDemographicsData
            exclude = ['patient']

class vitalForm(ModelForm):
      class Meta:
            model = Patient_vitals
            exclude = ['patient']

class immuneForm(ModelForm):
       class Meta:
             model = PatientImmunisation
             exclude =['patient','administrator']

@csrf_exempt
def patient_detail(request, id, showDetails=False):
      Patient        = Patient_detail.objects.get(pk=id)
     
      #PATIENT DEMO
      demo           = 'demo'
      demoData       =  None
      formDemo       = None
      
       #PATIENT VITALS
      vital          = 'vital'
      patient_vital  = None
      formVital      = None
      vForm          = vitalForm()
     
      
      
      #immune data
      iForm          = immuneForm()
      immune         = 'immune'
      formImmune     =  None
      patient_immune =  None
      
       #PATIENT DEMO
      try:
      		demoData = PatientDemographicsData.objects.get(patient = Patient)    
      except PatientDemographicsData.DoesNotExist:
      		formDemo = demoForm()
      		demo = ''
      	        #return render_to_response('staff/nurse_pat_detail.html',{'Patient':Patient,'form':form,'demo':demo})
     
        #PATIENT VITALS
      try:         
                patient_vital = Patient.patient.all()
      except Patient_vitals.DoesNotExist:
                formVital = vitalForm()
                vital  = ''
                #return render_to_response('staff/nurse_pat_detail.html',{'Patient':Patient,'form':form,'demo':demo})
      
      #PATIENT IMMUNISATION
      try:
                patient_immune   = Patient.iPatient.all()
      except PatientImmunisation.DoesNotExit:
                formImmune   = immuneForm()
                immune       = ''
     
      if request.method == 'POST':
                vital = request.POST.getlist('vital')
                print vital
                if  vital == [u'1']:
              		 pat_vital         = Patient_vitals(patient = Patient)
               		 vForm             = vitalForm(request.POST,instance = pat_vital)
               		 if vForm.is_valid():
                       		vForm.save()
       	        	        return HttpResponseRedirect('/pmis/pat_details/' + str( Patient.pk)+'/True/#dropdown2')
      
     	        elif vital == [u'2']:
                       pat_immune    =  PatientImmunisation(patient = Patient,administrator = request.user)
                       iForm         =  immuneForm(request.POST, instance = pat_immune)
                       if iForm.is_valid():
                          iForm.save()
                          return  HttpResponseRedirect('/pmis/pat_details/' + str( Patient.pk)+'/True/#immune2') 
                 
      
      
      
      return render_to_response('staff/nurse_pat_detail.html',{'patient_vital':patient_vital,
      							       'patient_immune':patient_immune,
     							       'formVital':formVital,
     							       'formImmune':formImmune,
      							       'vForm':vForm, 
     							       'iForm':iForm,
     							       'vital':vital,
      							       'immune':immune,
     							       'demo':demo,
      							       'formDemo':formDemo,
      							       'demoData':demoData,
      							       'user':request.user,
   							       'Patient':Patient})


#referral form

class refForm(ModelForm):
      class Meta:
            model = referred_appointment
            exclude = ['referrer']


@csrf_exempt
def nurse_referral(request):
        #ref form
        rForm          = refForm()
        formRef        =  None
        patient_ref    =  None
        
        if request.method == 'POST':
       		   patient_ref    =  referred_appointment(referrer= request.user)
        	   rForm          =  refForm(request.POST, instance = patient_ref)
                   if rForm.is_valid():
                          rForm.save()
                          return  HttpResponseRedirect('/pmis/nurse_ref/#today') 
        
        
        
        pat_referral = referred_appointment.objects.filter(referrer__username = request.user.username,date_created__day = date.today().strftime("%d"))
        pat_ref_past = referred_appointment.objects.filter(referrer__username = request.user.username,date_created__lt = date.today())
         
	return  render_to_response('staff/nurse_referal.html',
				  {'pat_ref_past':pat_ref_past,
				  'pat_referral':pat_referral,
				  'rForm':rForm,
				  'user':request.user})
