
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
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
	Pmis_id          = models.ForeignKey(User, help_text = " Select a registered Doctor or Add a new Doctor")
	username         = models.CharField('Username',help_text= "This designates the Username entered at the User's table", max_length = 50,null = True, blank =  True)
	first_Name       = models.CharField('First Name',max_length = 30,help_text ="This designates the  first name of the Doctor") 
        other_Name       = models.CharField ('Other Name(s)',max_length = 50,help_text = "This designates the Other name/s of the Doctor")
	specialization   = models.ForeignKey(Specialization, null = True,blank = True,help_text = "select doctor's specialization")
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender',choices =(("Male","Male"),("Female","Female")),max_length = 7,blank =False,null =False)
	Email            = models.EmailField('Email-address',blank = True, null = True)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
	age              = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
         

	def address_first_10(self):
		return self.address[:10]
		
	def admin_image(self):
              if self.headshot:
                 return '<div><img src ="%s" /></div>' %(self.headshot) 
             
              else:
                 return False
        admin_image.short_description = 'headshot'
        admin_image.allow_tags = True
		
        
        def Full_name(self,*args, **kwargs):
           if self.Pmis_id.username:
              self.Pmis_id.first_name = self.first_Name
              self.Pmis_id.last_name  = self.other_Name
              self.Pmis_id.email      = self.Email
              self.username           = self.Pmis_id.username
              self.Pmis_id.save(*args, **kwargs)
              return "DR. %s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())

	def __unicode__(self):
	        if self.Doc_ID <= 9: 
    	           return '[ 0DOC00%s ] %s  %s || %s' % (self.Doc_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper(),self.specialization)
    	        elif self.doc_ID > 9 and self.doc_ID < 100:
    	           return '[ 0DOC0%s ] %s  %s || %s' % (self.Doc_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper(),self.specialization)
    	        else:
    	           return '[ 0DOC%s ] %s  %s || %s' % (self.Doc_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper(),self.specialization)
		
    	
    	def doc_id_(self):
    	      if self.Doc_ID <= 9: 
    	         return "0DOC00%s" %(self.Doc_ID)
    	      elif self.doc_ID > 9 and self.doc_ID < 100:
    	         return "0DOC0%s" %(self.Doc_ID)
    	      else:
    	         return "0DOC%s" %(self.Doc_ID)
	
#hurray!!!! now working after an hour of continuous try and error :)
	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			 self.save()
               			 return "%s" %(self.age)
                             
			 else:
				 raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
          	elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.date_Of_birth = None
		        return True
	 	else:
		    raise Exception("Invalid Date of Birth / Age Supplied")
	      	    return False

    
# Nurses in the clinic
class Nurse(models.Model):
      
	nurse_ID         = models.AutoField(primary_key=True,editable = False)
	Pmis_id          = models.ForeignKey(User, help_text = " Select a registered Nurse or Add a new Nurse",unique = True)
	username         = models.CharField('Username',help_text= "This designates the Username entered at the User's table", max_length = 50,null = True, blank =  True)
	first_Name       = models.CharField('First Name',max_length = 30,help_text ="This designates the  first name of the Nurse") 
        other_Name       = models.CharField ('Other Name(s)',max_length = 50,help_text = "This designates the Other name/s of the Nurse")
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender',blank = False, null = False, choices =(("Male","Male"),("Female","Female")),max_length = 7)
	Email            = models.EmailField('Email-address',blank = True, null = True)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
	age              = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        
        
        def Full_name(self,*args, **kwargs):
           if self.Pmis_id.username:
              self.Pmis_id.first_name = self.first_Name
              self.Pmis_id.last_name  = self.other_Name
              self.Pmis_id.email      = self.Email
              self.username           = self.Pmis_id.username
              self.Pmis_id.save(*args, **kwargs)
              return "%s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())

	def address_first_10(self):
		return self.address[:10]
  
	#def Full_name(self):
	#	return "%s %s" %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())

	def __unicode__(self):
	        if self.nurse_ID  <= 9: 
    	           return '[ 0NUR00%s ] %s  %s ' % (self.nurse_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	        elif self.nurse_ID  > 9 and self.nurse_ID  < 100:
       	           return '[ 0NUR0%s ] %s  %s ' % (self.nurse_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	        else:
    	           return '[ 0NUR%s ] %s  %s ' % (self.nurse_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())

	def Nurse_id_(self):
    	      if self.nurse_ID  <= 9: 
    	         return "0NUR00%s" %(self.nurse_ID )
    	      elif self.nurse_ID  > 9 and self.nurse_ID  < 100:
    	         return "0NUR0%s" %(self.nurse_ID)
    	      else:
    	         return "0NUR%s" %(self.nurse_ID)

	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			 self.save()
               			 return "%s" %(self.age)
                             
			 else:
				 raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
          	elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.date_Of_birth = None
		        return True
	 	else:
		    raise Exception("Invalid Date of Birth / Age Supplied")
	      	    return False





# Pharmacist in the clinic
class Pharmacist(models.Model):
      
	Pharmacist_ID    = models.AutoField(primary_key=True,editable = False)
	Pmis_id        = models.ForeignKey(User, help_text = " Select a registered Pharmacist or Add a new Pharmacist",unique = True)
	username         = models.CharField('Username',help_text= "This designates the Username entered at the User's table", max_length = 50,null = True, blank =  True)
	first_Name       = models.CharField('First Name',max_length = 30,help_text ="This designates the  first name of the Pharmacist") 
        other_Name       = models.CharField ('Other Name(s)',max_length = 50,help_text = "This designates the Other name/s of the Pharmacist")
	Email            = models.EmailField('Email-address',blank = True, null = True)
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender',blank = False, null = False, choices =(("Male","Male"),("Female","Female")),max_length = 7)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
	age              = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        
        
        #SAVING INTO USERS OF THE SYSTEM TABLE (DJANGO USER)
        def Full_name(self,*args, **kwargs):
           if self.Pmis_id.username:
              self.Pmis_id.first_name = self.first_Name
              self.Pmis_id.last_name  = self.other_Name
              self.Pmis_id.email      = self.Email
              self.username           = self.Pmis_id.username
              self.Pmis_id.save(*args, **kwargs)
              
              return "%s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())

	def address_first_10(self):
		return self.address[:10]
	
	def __unicode__(self):
	        if self.Pharmacist_ID  <= 9: 
    	           return '[ 0PH00%s ] %s  %s ' % (self.Pharmacist_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	        elif self.Pharmacist_ID  > 9 and self.Pharmacist_ID  < 100:
    	           return '[ 0PH0%s ] %s  %s ' % (self.Pharmacist_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	        else:
    	           return '[ 0PH%s ] %s  %s ' % (self.Pharmacist_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
		


       #FORMATTING PHARMACIST ID
	def Pharm_id_(self):
    	      if self.Pharmacist_ID  <= 9: 
    	         return "0PH00%s" %(self.Pharmacist_ID )
    	      elif self.Pharmacist_ID  > 9 and self.Pharmacist_ID  < 100:
    	         return "0PH0%s" %(self.Pharmacist_ID)
    	      else:
    	         return "0PH%s" %(self.Pharmacist_ID)
       
       #AGE FUNCTION
	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			  self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			  self.save()
               			  return "%s" %(self.age)
                             
			 else:
				  raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
          	elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.date_Of_birth = None
		        return True
	 	else:
		    raise Exception("Invalid Date of Birth / Age Supplied")
	      	    return False


#Cashier of the Hospital
class cashier(models.Model):
      
	cashier_ID       = models.AutoField(primary_key=True,editable = False)
	Pmis_id          = models.ForeignKey(User, help_text = " Select a registered Cashier or Add a new Cashier",unique = True)
	username         = models.CharField('Username',help_text= "This designates the Username entered at the User's table", max_length = 50,null = True, blank =  True)
	first_Name       = models.CharField('First Name',max_length = 30,help_text ="This designates the  first name of the Cashier") 
        other_Name       = models.CharField ('Other Name(s)',max_length = 50,help_text = "This designates the Other name/s of the Cashier")
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender',blank = False, null = False, choices =(("Male","Male"),("Female","Female")),max_length = 7)
	Email            = models.EmailField('Email-address',blank = True, null = True)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
	age              = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        
	
	def Full_name(self,*args, **kwargs):
            if self.Pmis_id.username:
               self.Pmis_id.first_name = self.first_Name
               self.Pmis_id.last_name  = self.other_Name
               self.Pmis_id.email      = self.Email
               self.username           = self.Pmis_id.username
               self.Pmis_id.save(*args, **kwargs)
               
               return " %s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
	
	
	def Username(self):
		return "%s" %(self.Pmis_id.username)
	
	
	def address_first_10(self):
		return self.address[:10]
		
  
	def __unicode__(self):
	       if self.cashier_ID  <= 9: 
    	          return '[ OCAS00%s ] %s  %s ' % (self.cashier_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	       elif self.cashier_ID  > 9 and self.cashier_ID  < 100:
    	          return '[ OCAS0%s ] %s  %s ' % (self.cashier_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	       else:
    	          return '[ OCAS%s ] %s  %s ' % (self.cashier_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
		
	def Cashier_id_(self):
    	      if self.cashier_ID  <= 9: 
    	         return "OCAS00%s" %(self.cashier_ID )
    	      elif self.cashier_ID  > 9 and self.cashier_ID  < 100:
    	         return "OCAS0%s" %(self.cashier_ID)
    	      else:
    	         return "OCAS%s" %(self.cashier_ID)

	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			  self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			  self.save()
               			  return "%s" %(self.age)
                             
			 else:
				  raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
          	elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.date_Of_birth = None
		        return True
	 	else:
		    raise Exception("Invalid Date of Birth / Age Supplied")
	      	    return False



#Clinical staff models
class clinical_Staff(models.Model):
      
	clinical_Staff_ID = models.AutoField(primary_key=True,editable = False)
	Pmis_id        = models.ForeignKey(User, help_text = " Select a registered Staff or Add a new Staff",unique = True)
	username         = models.CharField('Username',help_text= "This designates the Username entered at the User's table", max_length = 50,null = True, blank =  True)
	first_Name       = models.CharField('First Name',max_length = 30,help_text ="This designates the  first name of the Cashier") 
        other_Name       = models.CharField ('Other Name(s)',max_length = 50,help_text = "This designates the Other name/s of the Cashier")
	phone_number     = models.CharField(max_length = 15,blank = True, null = True,unique = True,help_text = "e.g: (XXX)XXXXXXX")
	sex              = models.CharField('Gender', blank = False, null = False,choices =(("Male","Male"),("Female","Female") ),max_length = 7)
	Email            = models.EmailField('Email-address',blank = True, null = True)
	address          = models.TextField(blank = True, null = True,help_text ="Please enter both residential and postal address")
	date_Of_birth    = models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
	age              = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
	work_title       = models.CharField(max_length = 20,blank =True, null =True,help_text ="Please Enter the work field of the staff.")
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
	date_updated     = models.DateTimeField (auto_now_add=True,blank =True, null = True)
	headshot         = models.ImageField(upload_to = 'tmp',blank = True, null = True)
        
        
        #SAVING INTO USERS OF THE SYSTEM TABLE(DJANGO USER)
        def Full_name(self,*args, **kwargs):
           if self.Pmis_id.username:
              self.Pmis_id.first_name = self.first_Name
              self.Pmis_id.last_name  = self.other_Name
              self.Pmis_id.email      = self.Email
              self.username           = self.Pmis_id.username
              self.Pmis_id.save(*args, **kwargs)
             
              return "%s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())


        def address_first_10(self):
		return self.address[:10]
  
        def __unicode__(self):
        	if self.clinical_Staff_ID  <= 9: 
    	           return '[ 0ST00%s ] %s  %s ' % (self.clinical_Staff_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	        elif self.clinical_Staff_ID  > 9 and self.clinical_Staff_ID  < 100:
    	           return '[ 0ST0%s ] %s  %s ' % (self.clinical_Staff_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
    	        else:
    	           return '[ 0ST%s ] %s  %s ' % (self.clinical_Staff_ID,self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
                
      
	class Meta:
		verbose_name 	    = "Other Clinical Staff"
		verbose_name_plural = "Other Clinical Staffs"
		ordering 	    = ('clinical_Staff_ID', 'Pmis_id')
		
	def staff_ID_(self):
    	      if self.clinical_Staff_ID  <= 9: 
    	         return "0ST00%s" %(self.clinical_Staff_ID )
    	      elif self.clinical_Staff_ID  > 9 and self.clinical_Staff_ID  < 100:
    	         return "0ST0%s" %(self.clinical_Staff_ID)
    	      else:
    	         return "0ST%s" %(self.clinical_Staff_ID)

	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			 return "%s" %(self.age)
                             
			 else:
				 raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
          	elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.date_Of_birth = None
		        return True
	 	else:
		    raise Exception("Invalid Date of Birth / Age Supplied")
	      	    return False



#Doctor Admin
class DocAdmin(admin.ModelAdmin):
	list_display   = ('doc_id_','Full_name','username','specialization','phone_number','sex','date_Of_birth','Age','address_first_10','admin_image')
	search_fields  = ('Doc_ID','Full_name','specialization')
	list_filter    = ('specialization','date_registered','date_updated','sex')
	ordering       = ('-date_updated',)
	date_hierarchy = 'date_updated'
	#raw_horizontal_fields  = ('Pmis_id',)
	readonly_fields = ('age','username')
        #raw_horizontal_fields = ('specialization',)

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
      	list_display    = ('Nurse_id_','Full_name','username','phone_number','sex','address_first_10','date_Of_birth','Age','date_registered','date_updated')
      	search_fields   = ('nurse_ID','phone_number')
      	list_filter     = ('date_registered','date_updated','sex')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   = 20
      	#raw_horizontal_fields   = ('Pmis_id',)
      	readonly_fields = ('age','username')

#Pharmacist Admin
class PharmacistAdmin(admin.ModelAdmin):
      	list_display    = ('Pharm_id_','Full_name','username','phone_number','sex','address_first_10','date_Of_birth','Age','date_registered','date_updated')
      	search_fields   = ('Pharmacist_ID','phone_number')
      	list_filter     = ('date_registered','date_updated','sex')
     	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20
      	#raw_horizontal_fields   = ('Pmis_id',)
      	readonly_fields = ('age','username')

#Cashier Admin
class CashierAdmin(admin.ModelAdmin):
      	list_display    = ('Cashier_id_','Full_name','username','phone_number','sex','address_first_10','date_Of_birth','Age','date_registered','date_updated')
      	search_fields   = ('cashier_ID','phone_number')
      	list_filter     = ('date_registered','date_updated','sex')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20
      	#raw_horizontal_fields   = ('Pmis_id',)
      	readonly_fields = ('age','username')


class Clinical_staffAdmin(admin.ModelAdmin):
      	list_display    = ('staff_ID_','Full_name','username','phone_number','work_title','sex','address_first_10','date_Of_birth','Age','date_registered','date_updated')
      	search_fields   = ('clinical_Staff_ID','phone_number')
      	list_filter     = ('date_registered','date_updated','sex')
      	ordering        = ('-date_updated',)
      	date_hierarchy  = 'date_updated'
      	list_per_page   =  20
      	#raw_horizontal_fields   = ('Pmis_id',)
      	readonly_fields = ('age','username')

#Registration of models
admin.site.register(clinical_Staff,Clinical_staffAdmin)
admin.site.register(cashier,CashierAdmin)
admin.site.register(Pharmacist,PharmacistAdmin)
admin.site.register(Nurse,NurseAdmin)
admin.site.register(Specialization, SpecAdmin)
admin.site.register(Doctor,DocAdmin)



