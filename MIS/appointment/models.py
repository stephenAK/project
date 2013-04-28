#appointments

from django.db import models 
from patient.models import Patient_detail
#from pmis_user.models import PmisUser
from django.contrib import admin
from staff.models import Doctor
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date, time, timedelta
from django.contrib.auth.models import User
from django.template import loader, RequestContext

class AppointmentTime(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
         return unicode(self.date_created.strftime("%b %d, %Y, %I:%M %p"))
    def current_user(request):
          return "%s" %(request.user)



		
class Doctor_reservation(models.Model):
	STATUS_CHOICES = (
		(1, _("disabled")),
		(2, _("enabled")),
		(3, _("booked")),
		
	)
	TIME_CHOICES = (
		(6, _("6:00 AM")),
		(7, _("7:00 AM")),
		(8, _("8:00 AM")),
		(9, _("9:00 AM")),
		(10, _("10:00 AM")),
		(11, _("11:00 AM")),
		(12, _("12:00 PM")),
		(13, _("01:00 PM")),
		(14, _("02:00 PM")),
		(15, _("03:00 PM")),
		(16, _("04:00 PM")),
		(17, _("05:00 PM")),
		(18, _("06:00 PM")),
		
	)
	start_date    = models.DateField(_("Appointment Date"),help_text ="This designates the day of the week this appointment can be booked to") 
	starting_time = models.PositiveIntegerField("starting time",max_length = 7,choices = TIME_CHOICES, help_text = "This designates the time for start of the appointment",unique = False)
	end_time      = models.PositiveIntegerField(_("valid until"),max_length = 7,choices = TIME_CHOICES,help_text = "This indicates the time the appointment is supposed to end")
	doctor        = models.ForeignKey(Doctor,verbose_name=_("ID | Medical Doctor | Specialization"),help_text = "Select Doctor or add new Doctor")
	status        = models.PositiveSmallIntegerField(_("status"), default=2, choices=STATUS_CHOICES)
	max_Number    = models.PositiveIntegerField(default = 0,blank = True, null = True,help_text = "This designates the maximum number of patients the doctor can attend to within the time frame")
	
	date_created   = models.ForeignKey(AppointmentTime,unique = False)
	date_updated = models.DateTimeField(auto_now=True, blank = True, null =  True)

	class Meta:
		verbose_name = _("doctor reservation")
		verbose_name_plural = _("doctor reservations")
		ordering = ("-starting_time",)
		unique_together = (("start_date", "doctor"),)

	def __unicode__(self):
		return "[ %s %s @%s] %s %s [ %s ]" %(self.start_date.strftime("%A"),self.start_date,self.starting_time,self.doctor.Pmis_id.first_name.upper(),self.doctor.Pmis_id.last_name.upper(),self.doctor.specialization.name_of_field.upper())

#	def _passed(self):
#		if self.starting_time < datetime.now():
#			return True
#		else:
#			return False
#	passed = property(_passed)
        def expire(self):
            pass
        
        
       # def Status_check(self):
         #    if self.patient_appointment_set.count() == max 
	
	def appointments(self):
                return self.request_appointment_set.count()
                
	def Day(self):
            return '%s' %(self.start_date.strftime("%A"))   
        
        def check (self):
          if self.request_appointment_set.count() == self.max_Number:
             self.status = 3
             return False
          elif self.request_appointment_set.count() < self.max_Number:
             return True
          else:
              return "OVER BOOKED"
        check.boolean = True 
        
    #progress not in use  
'''  
        def progress_(self):
             if self.patient_appointment_set.count() < self.max_Number:
                self.progress =   self.patient_appointment_set.count()* 10
                return "<div style='width: 100px; border: 1px solid #ccc;'>" +  "<div style='height: 10px; width: %dpx; background: #555; '></div></div>" % (self.progress)
             else:
                 self.progress = 100
                 return "<div style='width: 100px; border: 1px solid #ccc;'>" +  "<div style='height: 10px; width: %dpx; background: #555; '></div></div>" % (self.progress)
             
        progress_.allow_tags = True
'''           
class Ailment(models.Model):
      name_of_ailment =  models.CharField(max_length = 40, null = True, blank =  True)
      date_created    = models. DateTimeField(auto_now_add = True, blank = True, null =  True)
      date_updated    = models. DateTimeField(auto_now =True, blank = True, null = True)
      
      def __unicode__(self):
           return self.name_of_ailment
           
      def number_of_reported_cases(self):
           return "%s" %(self.request_appointment_set.count())
               
class Request_appointment(models.Model):	
      	patient		 = models.ForeignKey(Patient_detail,null = False, blank = False,help_text = "Select a registered patient in the hospital")
       	doctor		 = models.ForeignKey(Doctor_reservation,help_text = "Select Doctor based on appointment date, time and specialization of Doctor")
        ailment          = models.ForeignKey(Ailment, blank = True, null = True)
       	date_created 	 = models.DateTimeField ("Request date",auto_now_add=True,blank =True, null = True)
	date_updated	 = models.DateTimeField(auto_now = True, blank =True, null =True)        
        comment          = models.TextField(blank =True, null = True)
        confirmed        = models.BooleanField(default = False, help_text = "Designates whether the appointment request is confirmed by doctor")
        
      
	class Meta:
		verbose_name 	    = "Patient Appointment Request"
		verbose_name_plural = "Patient Appointment Requests"
		ordering 	    = ('patient', 'doctor','date_created','date_updated')

       	def __unicode__(self):
	     	return "%s "%(self.patient)
	     	
       	def patient_ID(self):
              if self.patient.hospital_ID <= 9 and self.patient.patient_type is True:
    	         return "OUTPT000%s" %(self.patient.hospital_ID)
    	      elif self.patient.hospital_ID > 9 and self.patient. hospital_ID < 100 and self.patient.patient_type is True:
    	         return "OUTPT00%s" %(self.patient. hospital_ID)
    	      elif self.patient.hospital_ID > 99 and self.patient.hospital_ID <1000 and self.patient.patient_type is True:
    	         return "OUTPT0%s" %(self. patient.hospital_ID)
    	      elif self.patient.hospital_ID > 999 and self.patient.patient_type is True:
    	         return "OUTPT%s" %(self.patient. hospital_ID)
    	      elif self.patient.hospital_ID <= 9 and self.patient.patient_type is False:
    	         return "INPT000%s" %(self.patient.hospital_ID)
    	      elif self.patient.hospital_ID > 9 and self.patient. hospital_ID < 100 and self.patient.patient_type is False:
    	         return "INPT00%s" %(self.patient. hospital_ID)
    	      elif self.patient.hospital_ID > 99 and self.patient.hospital_ID <1000 and self.patient.patient_type is False:
    	         return "INPT0%s" %(self.patient. hospital_ID)
    	      else:
    	         return "INPT%s" %(self.patient.hospital_ID)
           	
       	def doctor_(self):
           	return "%s %s " %(self.doctor.doctor.Pmis_id.first_name.upper(),self.doctor.doctor.Pmis_id.last_name.upper())
           	
        def appointment_date_(self):
             return "[ %s ] %s @ %s" %(self.doctor.start_date.strftime("%A"),self.doctor.start_date,self.doctor.starting_time)
         
        
        
       
       
               
class referred_appointment(models.Model):
      	patient		 = models.ForeignKey(Patient_detail,null = False, blank = False,help_text = "Select a registered patient in the hospital")
       	doctor		 = models.ForeignKey(Doctor,help_text = "Select Doctor based on specialization of Doctor")    
        referrer         = models.ForeignKey(User,blank =True, null = True)
        comment          = models.TextField('Remarks',blank =True, null = True)
        
	date_created 	 = models.DateTimeField (blank =True, null = True)
	date_updated	 = models.DateTimeField( auto_now = True, blank =True, null =True)    
	
	class Meta:
		verbose_name 	    = "Referred Appointment"
		verbose_name_plural = "Referred Appointments"
		ordering 	    = ('patient', 'doctor','date_created','date_updated')
		
        def __unicode__(self):
	     	return "%s " %(self.patient)
	
	def Patient_id(self):
           	return "%s" %(self.patient.hospital_ID)
        
        def Doctor_(self):
           	return "%s %s " %(self.doctor.Pmis_id.first_name.upper(),self.doctor.Pmis_id.last_name.upper())
           	
        def referrer_(self):
             return "%s %s"%(self.referrer.first_name.upper(),self.referrer.last_name.upper())
       
class doctor_reservationInline(admin.TabularInline):
      model = Doctor_reservation
      
class AppointmentInline(admin.TabularInline):
      model = Request_appointment  
		

class request_appointment_Admin(admin.ModelAdmin):
      list_display	 = ('patient','date_created','appointment_date_','doctor_','date_updated','confirmed')
      list_filter 	 = ('doctor','patient','date_created','date_updated')
      raw_id_admin	 = ('patient','doctor',)
      readonly_fields    = ('confirmed',) 
     
class Doctor_reservation_Admin(admin.ModelAdmin):
	list_display        = ('start_date','Day','starting_time','end_time','doctor','max_Number','appointments','check')
	list_filter         = ('doctor__Pmis_id__first_name','doctor__Pmis_id__last_name','status','date_updated')
	ordering            = ('starting_time', 'doctor')
	inlines             = [AppointmentInline]
	date_hierarchy      = 'date_updated'
	search_fields       = ['^doctor__Pmis_id__first_name','^doctor__Pmis_id__last_name']
	fieldsets           = (
		(None, {"fields": ("doctor", "start_date","starting_time","end_time", "max_Number","date_created","status")}),
		
	)
class AppointmentTime_Admin(admin.ModelAdmin):
       list_display = ('date_created','current_user')
       inlines = [doctor_reservationInline]


class referred_appointment_Admin(admin.ModelAdmin):
      list_display	 = ('patient','Doctor_','referrer_','comment','date_created')
      list_filter 	 = ('doctor__Pmis_id__first_name','doctor__Pmis_id__last_name','date_created','date_updated')
      raw_id_admin	 = ('patient','doctor',)
      search_fields      = ['^doctor__Pmis_id__first_name','^doctor__Pmis_id__last_name']
         

class ailment_Admin(admin.ModelAdmin):
     list_display    = ('name_of_ailment','number_of_reported_cases','date_created', 'date_updated')
         
     
       
admin.site.register(Doctor_reservation, Doctor_reservation_Admin)
admin.site.register(AppointmentTime,AppointmentTime_Admin)
admin.site.register(Request_appointment,request_appointment_Admin)
admin.site.register(referred_appointment,referred_appointment_Admin)
admin.site.register(Ailment,ailment_Admin)

