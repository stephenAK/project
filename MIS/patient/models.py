from django.db import models
from django.contrib import admin
from countries.models import Country
from staff.models import Doctor 
 

class Patients_vital(models.Model):
 
     hospital_ID = models.AutoField(primary_key=True,editable = False)
     first_name = models.CharField(max_length = 30)
     middle_name = models.CharField(max_length = 30,help_text ="Please Enter initials/ Middle name")
     last_name = models.CharField(max_length = 30,help_text ="Please Enter initials/ Last name")
     age = models.PositiveIntegerField()
     sex = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others") ),max_length = 7)
     #date_Of_birth = models.DateField()
     #place_Of_Birth = models.CharField(max_length = 30)
     Nationality =  models.ForeignKey(Country)
     City = models.CharField("City/Town",max_length = 30)
     postal_Address =  models.TextField(max_length = 60,blank = True, null = True)
     phone_number = models.CharField(max_length = 15)
     Email = models.EmailField(blank = True, null = True)
     Contact_Of_Next_Of_Kin = models.TextField("Contact",help_text ="Please enter contact details of Next of Kin",max_length = 60,blank =True,null = True)
     date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
     date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)

     def __unicode__(self):
           return '%s %s' % (self.first_name, self.last_name)
   
     class Meta:
		verbose_name 	    = "Patient Details"
		verbose_name_plural = "Patient Details"
		ordering 	    = ('first_name', 'middle_name','last_name','age','sex','hospital_ID')

     
     def Full_name (self):
          return '%s %s %s' % (self.last_name.upper(), self.middle_name.upper(), self.first_name.upper())



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

class Guardian_Admin(admin.ModelAdmin):
      list_display = ('set_name','patient','relation_to_guardian','guardian_phone')
      search_fields = ('guardian_name','relation_to_guardian')
      list_filter = ('relation_to_guardian','patient','guardian_name')
      list_per_page = 20

class Patients_Admin(admin.ModelAdmin):
      list_display = ('hospital_ID','Full_name','Nationality','City','postal_Address','phone_number','age','sex','Nationality')
      search_fields = ('hospital_ID','last_name','first_name','Contact_Of_Next_Of_Kin')
      list_filter = ('last_name','City','date_registered','date_updated')
      ordering = ('-date_updated',)
      date_hierarchy = 'date_updated'
      fieldsets = ( (None, {'fields':('last_name','middle_name','first_name','phone_number','City','age','sex','Nationality')}),
                    ('Advanced details',{ 'classes':('collapse',),'fields':('postal_Address','Email','Contact_Of_Next_Of_Kin',)}),)
      list_per_page = 20


admin.site.register(Patients_vital,Patients_Admin)
admin.site.register(PatientGuardian,Guardian_Admin)
