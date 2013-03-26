#appointments

from django.db import models 
from patient.models import Patients_vital
from pmis_user.models import PmisUser
from django.contrib import admin
from staff.models import Doctor
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date, time, timedelta
from django.contrib.auth.models import User
from django.template import loader, RequestContext


class Doctor_schedule(models.Model):
	doctor 		= models.ForeignKey(Doctor)	
	patient         = models.ManyToManyField(Patients_vital, blank = True,null = True)
        #patients can make only one appointment in a day.
        
	def __unicode__(self):
	     	return "%s "%(self.doctor)


	def appointments(self):
                return self.doctor.patient_appointment_set.count()

	class Meta:
		verbose_name 	    = "Doctor Schedule"
		verbose_name_plural = "Doctor Schedules"
		
		
		
class Doctor_reservation(models.Model):
	STATUS_CHOICES = (
		(1, _("disabled")),
		(2, _("enabled")),
		(3, _("booked")),
		
	)
	start_date    = models.DateField(_("Date"),help_text ="This designates the day of the week this appointment can be booked to") 
	starting_time = models.TimeField(_("starting time"), help_text = "This designates the time for start of the appointment")
	end_time      = models.TimeField(_("valid until"),help_text = "This indicates the time the appointment is supposed to end")
	doctor        = models.ForeignKey(Doctor, verbose_name=_("medical Doctor"),help_text = "Select Doctor or add new Doctor")
	#patient       = models.ForeignKey(Patients_vital, verbose_name=_("patient"), null=True, blank=True)
	status        = models.PositiveSmallIntegerField(_("status"), default=2, choices=STATUS_CHOICES)
	#booked_at     = models.DateTimeField(_("booked at"), null=True, blank=True)
	booked_by     = models.CharField(_("booked by"), max_length=100, blank=True)

	class Meta:
		verbose_name = _("doctor reservation")
		verbose_name_plural = _("doctor reservations")
		ordering = ("-starting_time",)
		unique_together = (("starting_time", "doctor"),)

	def __unicode__(self):
		return "[ %s %s @%s] %s %s [ %s ]" %(self.start_date.strftime("%A"),self.start_date,self.starting_time,self.doctor.User_name.first_name.upper(),self.doctor.User_name.last_name.upper(),self.doctor.specialization.name_of_field.upper())

#	def _passed(self):
#		if self.starting_time < datetime.now():
#			return True
#		else:
#			return False
#	passed = property(_passed)
        def expire(self):
            pass
        
	
	def appointments(self):
                return self.patient_appointment_set.count()
                
	def Day(self):
            return '%s' %(self.start_date.strftime("%A"))   
            
            
class Patient_appointment(models.Model):
      	patient		 = models.ForeignKey(Patients_vital,null = False, blank = False,help_text = "Select a registered patient in the hospital")
       	doctor		 = models.ForeignKey(Doctor_reservation,help_text = "Select Doctor based on appointment date, time and specialization of Doctor")
       	date_created 	 = models.DateTimeField ("booked at",auto_now_add=True,blank =True, null = True)
	date_updated	 = models.DateTimeField( auto_now = True, blank =True, null =True)        
        referrer         = models.ForeignKey(User,blank =True, null = True)

	class Meta:
		verbose_name 	    = "Patient Appointment"
		verbose_name_plural = "Patient Appointments"
		ordering 	    = ('patient', 'doctor','date_created','date_updated')

       	def __unicode__(self):
	     	return "%s "%(self.patient)
       	def patient_id(self):
           	return "%s" %(self.patient.hospital_ID)
       	def doctor_(self):
           	return "%s %s " %(self.doctor.doctor.User_name.first_name.upper(),self.doctor.doctor.User_name.last_name.upper())
           	
        def appointment_date_(self):
             return "[ %s ] %s @ %s" %(self.doctor.start_date.strftime("%A"),self.doctor.start_date,self.doctor.starting_time)
         
        def has_reservation(self):
		if self.doctor:
			return True
		else:
			return False
	has_reservation.boolean = True
        
       
        def referrer_(self):
               return "%s %s" %(self.referrer.first_name.upper(),self.referrer.last_name.upper())


class booking(models.Model):
      Name =  models.ForeignKey(Doctor)
       

class AppointmentInline(admin.TabularInline):
      model = Patient_appointment  
		

class Patient_appointment_Admin(admin.ModelAdmin):
      list_display	 = ('patient_id','patient','date_created','appointment_date_','referrer_','doctor_','date_updated','has_reservation')
      list_filter 	 = ('doctor','patient','date_created','date_updated')
      raw_id_fields	 = ('patient','doctor',)
      readonly_fields    = ('referrer',)

class Doctor_scheduleAdmin(admin.ModelAdmin):
      list_display	  = ('doctor','appointments')
     # inlines            = [AppointmentInline]
     # search_fields     = ('guardian_name','relation_to_guardian')
     # list_filter 	 = ('doctor','patient','date_created','appointment_date')
     
class Doctor_reservation_Admin(admin.ModelAdmin):
	list_display        = ('start_date','Day','starting_time','doctor', 'status','appointments')
	readonly_fields     = ('booked_by',)
	list_filter         = ('status', 'doctor', 'starting_time')
	ordering            = ('starting_time', 'doctor')
	inlines             = [AppointmentInline]
	search_fields       = ['^patient__User_name__first_name','^patient__User_name__last_name']
	fieldsets           = (
		(None, {"fields": ("doctor", "start_date","starting_time","end_time", "status")}),
		
	)
	
admin.site.register(Doctor_reservation, Doctor_reservation_Admin)
#admin.site.register(Doctor_schedule,Doctor_scheduleAdmin)
admin.site.register(Patient_appointment,Patient_appointment_Admin)


