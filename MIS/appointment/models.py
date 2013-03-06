#appointments

from django.db import models 
from patient.models import Patients_vital
from pmis_user.models import PmisUser
from django.contrib import admin
from staff.models import Doctor

class Patient_appointment(models.Model):
      	patient		 = models.ForeignKey(Patients_vital,null = False, blank = False)
       	doctor		 = models.ForeignKey(Doctor)# the appointment is with Doctors not just any PmisUser
       	appointment_date = models.DateTimeField ()
       	date_created 	 = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	date_updated	 = models.DateTimeField( auto_now = True, blank =True, null =True)        



       	def __unicode__(self):
	     	return "%s "%(self.patient)
       	def patient_id(self):
           	return "%s" %(self.patient.hospital_ID)
       	def doctor_(self):
           	return "%s: %s: %s" %(doctor.staff_Name)

class Doctor_schedule(models.Model):
	doctor 		= models.ForeignKey(Doctor)	
	patient         = models.ManyToManyField(Patients_vital, blank = True,null = True)

	def __unicode__(self):
	     	return "%s "%(self.doctor)


	def appointments(self):
                return self.doctor.patient_appointment_set.count()

	#def number_of_appointments(self):
           	#return "%s" %(doctor.appointments)

class Patient_appointment_Admin(admin.ModelAdmin):
      list_display	 = ('patient_id','patient','doctor','date_created','appointment_date')
     # search_fields     = ('guardian_name','relation_to_guardian')
      list_filter 	 = ('doctor','patient','date_created','appointment_date')
      

class Doctor_scheduleAdmin(admin.ModelAdmin):
      list_display	 = ('doctor','appointments')
     # search_fields     = ('guardian_name','relation_to_guardian')
     # list_filter 	 = ('doctor','patient','date_created','appointment_date')
      

admin.site.register(Doctor_schedule,Doctor_scheduleAdmin)
admin.site.register(Patient_appointment,Patient_appointment_Admin)


