
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from pmis_user.models import PmisUser
from datetime import datetime,date,time
from staff.thumbs import ImageWithThumbsField
from sorl.thumbnail import default
from sorl.thumbnail import get_thumbnail
#from sorl.thumbnail.main import DjangoThumbnail
#from appointment.models import Patient_appointment


# Specializations in the Clinic
class Specialization(models.Model):
	name_of_field   = models.CharField(max_length = 100, unique = True,help_text = "please enter name of field. eg: General Practicianers..etc")
	date_created    = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated    = models.DateTimeField (auto_now=True,blank =True, null = True)
  
	def __unicode__ (self):
		return '%s' %(self.name_of_field.upper())
     
	def number_of_practicians(self):
		return self.doctor_set.count() 
      
	def Field_Name(self):
		return '%s' %(self.name_of_field.upper())


class SpecInline(admin.StackedInline):
	model           = Specialization


# Doctors in the clinic
class Doctor(models.Model):
      
	Doc_ID           = models.AutoField(primary_key=True,editable = False)
	User_name        = models.ForeignKey(PmisUser, help_text = " Select a registered Doctor or Add a new Doctor",unique = True)
	specialization   = models.ForeignKey(Specialization, null = True,blank = True,help_text = "select doctor's specialization")
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others") ),max_length = 7,blank =False,null =False)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True)
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
         

	def address_first_10(self):
		return self.address[:10]
 
	def Full_name(self):
		return "%s %s [ %s ]" %(self.User_name.first_name.upper(),self.User_name.last_name.upper(),self.User_name.username.upper())

	def __unicode__(self):
		return '%s || %s  %s || %s' % (self.Doc_ID,self.User_name.first_name.upper(),self.User_name.last_name.upper(),self.specialization)
    	
	

#Still not working '(  
	def set_age(self):
		if self.date_of_birth:
	         #print "122221212212"	
               		 min_allowed_dob = datetime.datetime(1900,01,01)
	        	 max_allowed_dob = datetime.datetime.now()
			#if self.date_of_birth >= min_allowed_dob and self.date_of_birth <= max_allowed_dob:
               		 age  = "%s" %(max_allowed_dob - self.date_of_birth )
                	 return "%s" %(self.date_of_birth)
                             
			#else:
			#	raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
          	elif self.age and int(self.age[0:3])<=120:
	        	self.date_of_birth = None
			return True
	 	else:
			#	raise Exception("Invalid Date of Birth / Age Supplied")
	      		return False
      
# Nurses in the clinic
class Nurse(models.Model):
      
	nurse_ID         = models.AutoField(primary_key=True,editable = False)
	User_name        = models.ForeignKey(PmisUser, help_text = " Select a registered Nurse or Add a new Nurse",unique = True)
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others") ),max_length = 7)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True)
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        

	def address_first_10(self):
		return self.address[:10]
  
	def Full_name(self):
		return "%s %s" %(self.User_name.first_name.upper(),self.User_name.last_name.upper())

	def __unicode__(self):
		return '%s || %s  %s ' % (self.nurse_ID,self.User_name.first_name.upper(),self.User_name.last_name.upper())





# Pharmacist in the clinic
class Pharmacist(models.Model):
      
	Pharmacist_ID    = models.AutoField(primary_key=True,editable = False)
	User_name        = models.ForeignKey(PmisUser, help_text = " Select a registered Pharmacist or Add a new Pharmacist",unique = True)
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others") ),max_length = 7)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True)
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        

	def address_first_10(self):
		return self.address[:10]
  
	def Full_name(self):
		return "%s %s" %(self.User_name.first_name.upper(),self.User_name.last_name.upper())

	def __unicode__(self):
		return '%s || %s  %s ' % (self.Pharmacist_ID,self.User_name.first_name.upper(),self.User_name.last_name.upper())


#Cashier of the Hospital
class cashier(models.Model):
      
	cashier_ID       = models.AutoField(primary_key=True,editable = False)
	User_name        = models.ForeignKey(PmisUser, help_text = " Select a registered Cashier or Add a new Cashier",unique = True)
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others") ),max_length = 7)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True)
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        

	def address_first_10(self):
		return self.address[:10]
  
	def Full_name(self):
		return "%s %s" %(self.User_name.first_name.upper(),self.User_name.last_name.upper())

	def __unicode__(self):
		return '%s || %s  %s ' % (self.cashier_ID,self.User_name.first_name.upper(),self.User_name.last_name.upper())

class clinical_Staff(models.Model):
      
	clinical_Staff_ID    = models.AutoField(primary_key=True,editable = False)
	User_name        = models.ForeignKey(PmisUser, help_text = " Select a registered Staff or Add a new Staff",unique = True)
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female"),("Others","Others") ),max_length = 7)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True)
	work_title       = models.CharField(max_length = 20,blank =True, null =True,help_text ="Please Enter the work field of the staff.")
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        

        def address_first_10(self):
		return self.address[:10]
  
        def Full_name(self):
                return "%s %s" %(self.User_name.first_name.upper(),self.User_name.last_name.upper())

        def __unicode__(self):
                return '%s || %s  %s ' % (self.clinical_Staff_ID,self.User_name.first_name.upper(),self.User_name.last_name.upper())
      
	class Meta:
		verbose_name 	    = "Other Clinical Staff"
		verbose_name_plural = "Other Clinical Staffs"
		ordering 	    = ('clinical_Staff_ID', 'User_name')



#Doctor Admin
class DocAdmin(admin.ModelAdmin):
	list_display   = ('Doc_ID','Full_name','specialization','phone_number','sex','date_Of_birth','address_first_10','date_registered','date_updated','set_age','headshot')
	search_fields  = ('Doc_ID','Full_name','specialization')
	list_filter    = ('specialization','date_registered','date_updated')
	ordering       = ('-date_updated',)
	date_hierarchy = 'date_updated'
	raw_id_fields  = ('User_name',)
        raw_horizontal_fields = ('specialization',)

#Specialization Admin
class SpecAdmin(admin.ModelAdmin):
	list_display    = ('Field_Name','number_of_practicians','date_created','date_updated')
      	search_fields   = ('name_of_field','number_of_practicians')
     	list_filter     = ('name_of_field','date_created','date_updated')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20

#Nurse Admin
class NurseAdmin(admin.ModelAdmin):
      	list_display    = ('nurse_ID','Full_name','phone_number','sex','address_first_10','date_Of_birth','date_registered','date_updated','headshot')
      	search_fields   = ('nurse_ID','phone_number')
      	list_filter     = ('date_registered','date_updated')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   = 20
      	raw_id_fields   = ('User_name',)

#Pharmacist Admin
class PharmacistAdmin(admin.ModelAdmin):
      	list_display    = ('Pharmacist_ID','Full_name','phone_number','sex','address_first_10','date_Of_birth','date_registered','date_updated','headshot')
      	search_fields   = ('Pharmacist_ID','phone_number')
      	list_filter     = ('date_registered','date_updated')
     	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20
      	raw_id_fields   = ('User_name',)

#Cashier Admin
class CashierAdmin(admin.ModelAdmin):
      	list_display    = ('cashier_ID','Full_name','phone_number','sex','address_first_10','date_Of_birth','date_registered','date_updated','headshot')
      	search_fields   = ('cashier_ID','phone_number')
      	list_filter     = ('date_registered','date_updated')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20
      	raw_id_fields   = ('User_name',)

class Clinical_staffAdmin(admin.ModelAdmin):
      	list_display    = ('clinical_Staff_ID','Full_name','phone_number','sex','address_first_10','date_Of_birth','date_registered','date_updated','headshot')
      	search_fields   = ('clinical_Staff_ID','phone_number')
      	list_filter     = ('date_registered','date_updated')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20
      	raw_id_fields   = ('User_name',)

#Registration of models
admin.site.register(clinical_Staff,Clinical_staffAdmin)
admin.site.register(cashier,CashierAdmin)
admin.site.register(Pharmacist,PharmacistAdmin)
admin.site.register(Nurse,NurseAdmin)
admin.site.register(Specialization, SpecAdmin)
admin.site.register(Doctor,DocAdmin)



