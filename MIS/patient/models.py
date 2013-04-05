from django.db import models
from django.contrib import admin
from countries.models import Country
from staff.models import Doctor 
from pmis_user.models import PmisUser
from django.contrib.auth.models import User
 

class Patients_vital(models.Model):
 
     hospital_ID      = models.AutoField(primary_key=True,editable = False)
     User_name        = models.ForeignKey(PmisUser, help_text = " Select a registered Patient or Add a new Patient",unique = True)
     age              = models.PositiveIntegerField(blank = True, null = True)
     sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others")),max_length = 7)
    # date_Of_birth    = models.DateField(blank = True, null = True)
     #place_Of_Birth  = models.CharField(max_length = 30)
     Nationality      =  models.ForeignKey(Country)
     City             = models.CharField("City/Town",max_length = 30,blank = True, null = True)
     postal_Address   =  models.TextField(max_length = 60,blank = True, null = True)
     phone_number     = models.CharField(max_length = 15, blank = True, null = True,unique =  True)
     Email            = models.EmailField(blank = True, null = True)
     Contact_Of_Next_Of_Kin = models.TextField("Contact",help_text ="Please enter contact details of Next of Kin",max_length = 60,blank =True,null = True)
     date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
     date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)

     def __unicode__(self):
           return '%s %s' % (self.User_name.first_name.upper(), self.User_name.last_name.upper())
   
     class Meta:
		verbose_name 	    = "Patient Details"
		verbose_name_plural = "Patient Details"
		ordering 	    = ('User_name','age','sex','hospital_ID')

     
     def Full_name(self):
		return "%s %s [ %s ]" %(self.User_name.first_name.upper(),self.User_name.last_name.upper(),self.User_name.username.upper())



class PatientGuardian(models.Model):

	'''
	Class that defines the Guardian of a Particular patient    
	'''

	__model_label__ = "guardian"

	guardian_name 		= models.CharField(max_length = 20,help_text ="Enter Patient's Guardian Name")
	relation_to_guardian 	= models.CharField('Relation',max_length =20, blank= True, null	= True, help_text = "Select relationship to Patient", choices =(("Father","Father"),("Mother","Mother"),("Sibling","Sibling"),("Local Guardian","LocalGuardian"),("Other","Other") ))
	guardian_phone 		= models.CharField('Phone',max_length= 20, blank = True, null= True)
	patient 		= models.ForeignKey(Patients_vital, null = False, blank = False)

	def __unicode__(self):
		if self.guardian_name:
			return "%s "%(self.guardian_name.upper())
		else:
			return "No Guardian Name Provided"
        def set_name(self):
 		return '%s '%(self.guardian_name.upper())

	class Meta:
		verbose_name 	    = "Guardian Details"
		verbose_name_plural = "Guardian Details"
		ordering 	    = ('patient','guardian_name')

#model for the various billings in the Hospital
class  bill_type(models.Model):
       name = models.CharField(max_length = 20)
       
       def __unicode__(self):
           return self.name.upper()
           
       class Meta:
		verbose_name 	    = "Billing Type"
		verbose_name_plural = "Billing types"
           
		
class patient_bill(models.Model):
      patient = models.ForeignKey(Patients_vital)
      bill_type = models.ForeignKey(bill_type,max_length = 20)
      mode_of_payment = models.CharField(choices = (("CASH","CASH"),("CHEQUE","CHEQUE"),("NHIS","NHIS")),max_length = 10)
      is_paid = model.BooleanField(blank =  True, null = True,help_text = "Designates whether the patient has made payments.")#amount to be payment would be indicated by the cashier
      
      class Meta:
		verbose_name 	    = "Patient Bill"
		verbose_name_plural = "Patient Billings"
		
      def __unicode__(self):
           return self.patient.upper()



class Guardian_Admin(admin.ModelAdmin):
      list_display = ('set_name','patient','relation_to_guardian','guardian_phone')
      search_fields = ('guardian_name','relation_to_guardian')
      list_filter = ('relation_to_guardian','patient','guardian_name')
      list_per_page = 20

class Patients_Admin(admin.ModelAdmin):
      list_display = ('hospital_ID','Full_name','City','postal_Address','phone_number','age','sex','Nationality')
      search_fields = ['hospital_ID','^User_name__first_name','^User_name__last_name','Contact_Of_Next_Of_Kin']
      list_filter = ('City','date_registered','date_updated')
      ordering = ('-date_updated',)
      date_hierarchy = 'date_registered'
      fieldsets = ( (None, {'fields':('User_name','phone_number','City','sex','Nationality')}),
                    ('Advanced details',{ 'classes':('collapse',),'fields':('age','postal_Address','Email','Contact_Of_Next_Of_Kin',)}),)
      list_per_page = 20
      raw_id_fields   = ('User_name',)
      readonly_fields = ('age',)

class patient_bill_Admin(admin.ModelAdmin):
      list_display = ('patient',' bill_type',' mode_of_payment','is_paid')
      list_filter = ('mode_of_payment','is_paid')
      raw_id_fields = ('patient',)
      
      
class bill_type_Admin(admin.ModelAdmin):
      list_display ('name')




admin.site.register(Patients_vital,Patients_Admin)
admin.site.register(PatientGuardian,Guardian_Admin)
admin.site.register(bill_type,bill_type_Admin)
admin.site.register(patient_bill,patient_bill_Admin)
