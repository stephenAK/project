from django.db import models
from django.contrib import admin
from countries.models import Country
from staff.models import Doctor 
from django.contrib.auth.models import User
from datetime import datetime,date,time
 



#MODELS/TABLE FOR PATIENT DETAILS
class Patient_detail(models.Model):
 
     hospital_ID      = models.AutoField(primary_key=True,editable = False)
     patient_type     = models.BooleanField(default = True, help_text = "Uncheck if IN-PATIENT")
     Pmis_id          = models.ForeignKey(User, help_text = " Select a registered Patient or Add a new Patient",unique = True)
     username         = models.CharField('Username',help_text= "This designates the Username entered at the User's table", max_length = 50,null = True, blank =  True)
     first_Name       = models.CharField('First Name',max_length = 30,help_text ="This designates the  first name of the patient") 
     other_Name       = models.CharField ('Other Name(s)',max_length = 50,help_text = "This designates the Other name/s of the Patient")
     age              = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
     sex              = models.CharField('Gender', choices =(("Male","Male"),("Female","Female")),max_length = 7)
     date_Of_birth    = models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
     Nationality      =  models.ForeignKey(Country,default = "GH")
    # pat_id           = models.CharField(blank =True, null =True)
     City             = models.CharField("City/Town",max_length = 30,blank = True, null = True)
     postal_Address   =  models.TextField(max_length = 60,blank = True, null = True,help_text = "")
     phone_number     = models.CharField(max_length = 15, blank = True, null = True,unique =  True,help_text = "XXX-XXXXXXX")
     Email            = models.EmailField('Email-address',blank = True, null = True)
     Contact_Of_Next_Of_Kin = models.TextField("Contact-N.O.K",help_text ="Please enter contact details of Next of Kin",max_length = 60,blank =True,null = True)
     date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
     date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)
     

     
   
     class Meta:
		verbose_name 	    = "Patient Details"
		verbose_name_plural = "Patient Details"
		ordering 	    = ('Pmis_id','age','sex','hospital_ID')
  
     def Full_name_(self,*args, **kwargs):
         if self.Pmis_id.username:
              self.Pmis_id.first_name = self.first_Name
              self.Pmis_id.last_name  = self.other_Name
              self.Pmis_id.email      = self.Email
              self.username           = self.Pmis_id.username
              self.Pmis_id.save(*args, **kwargs)
              return "%s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
              
     '''
     def save(self,*args, **kwargs):
		
		Custom Save Method needs to be defined. 
		This should check for:
		1. Setting the Full_name attribute
		
                self.Full_name()
		super(Patient_detail, self).save(*args, **kwargs)

     
       
   
     def Full_name(self,*args,**kwargs):
           self.save(*args,**kwargs)
	   return "%s %s " %(self.Pmis_id.first_name.upper(),self.Pmis_id.last_name.upper())
         
     def username_(self):
          if self.Pmis_id.username:
             self.username = self.Pmis_id.username
             self.save()
             return "%s" %(self.username)
     '''


# FORMATTING PATIENT ID
     def patient_id(self):
    	      if self.hospital_ID <= 9 and self.patient_type is True:
    	         return "OUTPT000%s" %(self.hospital_ID)
    	      elif self.hospital_ID > 9 and self. hospital_ID < 100 and self.patient_type is True:
    	         return "OUTPT00%s" %(self. hospital_ID)
    	      elif self.hospital_ID > 99 and self.hospital_ID <1000 and self.patient_type is True:
    	         return "OUTPT0%s" %(self. hospital_ID)
    	      elif self.hospital_ID > 999 and self.patient_type is True:
    	         return "OUTPT%s" %(self. hospital_ID)
    	      elif self.hospital_ID <= 9 and self.patient_type is False:
    	         return "INPT000%s" %(self.hospital_ID)
    	      elif self.hospital_ID > 9 and self. hospital_ID < 100 and self.patient_type is False:
    	         return "INPT00%s" %(self. hospital_ID)
    	      elif self.hospital_ID > 99 and self.hospital_ID <1000 and self.patient_type is False:
    	         return "INPT0%s" %(self. hospital_ID)
    	      else:
    	         return "INPT%s" %(self.hospital_ID)
    	      
     def __unicode__(self):
              if self.hospital_ID <= 9 and self.patient_type is True:
    	         return '[ OUTPT000%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      elif self.hospital_ID > 9 and self. hospital_ID < 100 and self.patient_type is True:
    	         return '[ OUTPT00%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      elif self.hospital_ID > 99 and self.hospital_ID <1000 and self.patient_type is True:
    	         return '[ OUTPT0%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      elif self.hospital_ID > 999 and self.patient_type is True:
    	         return '[ OUTPT%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      elif self.hospital_ID <= 9 and self.patient_type is False:
    	         return '[ INPT000%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      elif self.hospital_ID > 9 and self. hospital_ID < 100 and self.patient_type is False:
    	         return '[ INPT00%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      elif self.hospital_ID > 99 and self.hospital_ID <1000 and self.patient_type is False:
    	         return '[ INPT0%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      else:
    	         return '[ INPT%s ] %s %s' % (self.hospital_ID,self.Pmis_id.first_name.upper(), self.Pmis_id.last_name.upper())
    	      
           
    	         
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
	 	#else:
		  #  raise Exception("Invalid Date of Birth / Age Supplied")
	      	  #  return False
    
# END FROM PATIENT MODEL



# MODEL /TABLE FOR PATIENT GUARDIAN
class PatientGuardian(models.Model):

	'''
	Class that defines the Guardian of a Particular patient    
	'''

	__model_label__ = "guardian"

	guardian_name 		= models.CharField(max_length = 20,help_text ="Enter Patient's Guardian Name")
	relation_to_guardian 	= models.CharField('Relation',max_length =20, blank= True, null	= True, help_text = "Select relationship to Patient", choices =(("Father","Father"),("Mother","Mother"),("Sibling","Sibling"),("Local Guardian","LocalGuardian"),("Wife","Wife"),("Husband","Husband"),("Other","Other") ))
	#specify                = models.CharField('Specify',help_text = "Specify if Other", max_length = 30)
	guardian_phone 		= models.CharField('Phone',max_length= 20, blank = True, null= True)
	patient 		= models.ForeignKey(Patient_detail, null = False, blank = False)

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
#END OF PATIENT GUARDIAN TABLE



# MODEL/TABLE FOR PATIENT VITALS.
class Patient_vitals(models.Model):
       body_temp           = models.FloatField("Body Temperature",blank = True, null = True, help_text ="Average: 36.6-37.3 degrees Celcius") 
       blood_pressure      = models.CharField("B.P",max_length= 20,blank = False, null = False, help_text = "Average: 90/60 mm/Hg to 120/80 mmHg")
       heart_rate          = models.FloatField("Pulse",blank =  True, null = True, help_text = "Average: 60-100 beats per minute")   
       respiration_rate    = models.CharField(blank = True,max_length= 20, null = True, help_text ="Average: 12-18 breaths per minute")
       patient 		   = models.ForeignKey(Patient_detail, related_name ='patient')
       #administrator       = models.ForeignKey (User)
       date_created        = models.DateTimeField (auto_now_add=True, blank =True, null = True)
       date_updated        = models.DateTimeField (auto_now=True,blank =True, null = True)
       
       def __unicode__(self):
             return " Vitals for - %s" %(self.patient) 
       
       def date(self):
           # det = int(self.date_created.strftime("%b %d %Y %I"))
            return "%s" %(self.date_created.strftime("%b %d %Y")) 
             
       def patient_(self):
             return "%s" %(self.patient) 
      
       def body_temp_(self):
             return "%s celcius " %(self.body_temp)
       
       def Blood_pressure_ (self):
            return "%s mm/Hg" %(self.blood_pressure)
       
       def Pulse(self):
           return "%s beats per mins" %(self.heart_rate)
           
       def respiration_rate_(self):
            return "%s breaths per minute" %(self.respiration_rate)
            
       class Meta:
		verbose_name 	    = "Patient Vital"
		verbose_name_plural = "Patient Vitals"
#END OF PATIENT VITALS TABLE.


		


#MODEL/TABLE FOR PATIENT DEMOGRAPHIC		
class PatientDemographicsData(models.Model):
    """
      Maintains Demographic, Social and Family data for the patient
      This has been adapted from the excellent work by GNU Health project
      However this is a very rudimentary adaptation
    """

    __model_label__ = "demographics"

    socio_economics    = models.CharField(max_length = 100, default="Middle", 
                                         choices = (("low", "Low"), 
                                                    ("middle", "Middle" ),
                                                    ("high","High")
                                                   )
                                        )
    education         = models.CharField(max_length = 100, default = "Graduate",              choices = (('Post Graduate','Post-Graduate'),
               ('Graduate','Graduate'),
               ('High School','High School'),
               ('Lower Grade School',"Lower Grade School"),
               ('Iliterate', "Iliterate")
              )
    )
    housing_conditions = models.TextField(max_length = 250,
                                         default = "Comfortable, with good sanitary conditions"
                         )
    religion           = models.CharField(max_length = 200)    
    race               = models.CharField(max_length = 200,help_text = "Eg. Akan,Brono etc")
    languages_known    = models.TextField(max_length = 300)
    patient            = models.ForeignKey(Patient_detail,
                                           null = True,
                                           blank = True,
                                           unique = True
                         )

    
    date_created        = models.DateTimeField (auto_now_add=True, blank =True, null = True)
    date_updated        = models.DateTimeField (auto_now=True,blank =True, null = True)
    
    
    class Meta:
		verbose_name 	    = "Patient Demographics Data"
		verbose_name_plural = "Patient Demographics Data"
    
    def __unicode__(self):
         return " Demographics for - %s" %(self.patient)
         
    def patient_(self):
        return " Demographics for - %s" %(self.patient)
        
#END OF TABLE FOR PATIENT DEMOGRAPHY





#MODEL FOR VACCINES IN THE HOSPITAL
class VaccineRegistry(models.Model):
  """
    Registry for the Vaccines
    This contains the details of vaccine, VIS, Manufacturer, Lot #, Expiration etc..
  """
  vaccine_name        = models.CharField(max_length = 100)
  manufacturer        = models.CharField(max_length = 100)
  lot_number          = models.CharField(max_length = 100)
  manufacturing_date  = models.DateField(auto_now_add = False)
  expiry_date         = models.DateField(auto_now_add = False)
  vis                 = models.TextField("Vaccine Information Statement", 
                                         max_length = 1000, blank = True, null = True
                        )
  date_added          = models.DateTimeField (auto_now_add=True, blank =True, null = True)
  date_updated        = models.DateTimeField (auto_now=True,blank =True, null = True)
  
  
  
  class Meta:
		verbose_name 	    = "Vaccine Registry"
		verbose_name_plural = "Vaccine Registry"
  
  def __unicode__(self):
    return "%s" %(self.vaccine_name)

  def save(self,*args, **kwargs):
    self.__model_label__ = "vaccine_registry"
    super(VaccineRegistry, self).save(*args, **kwargs)
#END OF VACCINES TABLE.

    
        
#PATIENT IMMUNISATION TABLE.
class PatientImmunisation(models.Model):
  
  __model_label__ = "immunisation"

#  vaccine_name     = models.CharField(max_length = 100)
  vaccine_detail    = models.ForeignKey('VaccineRegistry')
  route             = models.CharField(max_length = 30,
                                       choices=(("im", "IM"), 
                                                ("deep_im", "Deep IM"),
                                                ("iv", "Intravenous"),
                                                ("sc", "Sub Cutaneous"),
                                                ("oral", "Oral")
                                        ), 
                                        default="IM" 
                      )
  injection_site    = models.CharField(max_length = 100, 
                                       choices=(("lue", "Left Upper Arm"), 
                                                ("rue", "Right Upper Arm"),
                                                ("lb",  "Left Buttock"),
                                                ("rb",  "Right Buttock"),
                                                ("abd", "Abdomen"),
                                                ("oral", "Oral")
                                        ), 
                                        default="Right Upper Arm"
                      )
  dose              = models.CharField(max_length = 100)
  administrator     = models.ForeignKey(User)
  vaccination_date  = models.DateField(auto_now_add = True)
  next_due          = models.DateField(auto_now_add= False)
  adverse_reaction  = models.TextField(max_length = 100, default = "None")
  patient           = models.ForeignKey(Patient_detail,null = True,blank = True, related_name ='iPatient')
  

  def __unicode__(self):
    return "%s" %(self.vaccine_detail)
  
  
  def patient_(self):
        return " Immunization for - %s" %(self.patient) 
    
  class Meta:
		verbose_name 	    = "Patient Immunisation"
		verbose_name_plural = "Patient Immunisation"

  def save(self,*args, **kwargs):
    self.__model_label__ = "immunisation"
    super(PatientImmunisation, self).save(*args, **kwargs)

#END OF IMMUNISATION TABLE.  
        
 


    


class GuardianInline(admin.TabularInline):
      model = PatientGuardian

class Guardian_Admin(admin.ModelAdmin):
      list_display = ('set_name','patient','relation_to_guardian','guardian_phone')
      search_fields = ('guardian_name','relation_to_guardian')
      list_filter = ('relation_to_guardian','patient','guardian_name')
      list_per_page = 20
        

class Patients_Admin(admin.ModelAdmin):
      list_display      = ('patient_id','Full_name_','username','City','postal_Address','phone_number','date_Of_birth','Age','sex','Nationality')
      search_fields     = ['hospital_ID','^Pmis_id__first_name','^Pmis_id__last_name','Contact_Of_Next_Of_Kin']
      list_filter       = ('City','patient_type','date_registered','date_updated')
      ordering          = ('-date_updated',)
      date_hierarchy    = 'date_registered'
      fieldsets         = ( (None, {'fields':('Pmis_id','first_Name','other_Name','username','sex','phone_number','date_Of_birth','patient_type','Nationality','City')}),
                    ('Advanced details',{ 'classes':('collapse',),'fields':('age','postal_Address','Email','Contact_Of_Next_Of_Kin',)}),)
      list_per_page     = 20
      raw_horizontal_fields = ('Pmis_id',)
      readonly_fields       = ('age','username')
      inlines               = [GuardianInline]

class PatientImmunisation_Admin(admin.ModelAdmin):
         list_display   = ('patient_','vaccine_detail','route','injection_site','dose','administrator','vaccination_date','next_due','adverse_reaction')
         search_fields  = ('vaccine_name','manufacturer')
         list_filter    = ('vaccination_date','vaccination_date')
         list_per_page  = 20  
         date_hierarchy    = 'vaccination_date'       

class VaccineRegistry_Admin(admin.ModelAdmin):
         list_display   = ('vaccine_name','manufacturer','lot_number','manufacturing_date','expiry_date','vis','date_added','date_updated')
         search_fields  = ('vaccine_name','manufacturer')
         list_filter    = ('date_added','date_updated')
         list_per_page  = 20  
         date_hierarchy    = 'date_added' 


class PatientDemographic_Admin(admin.ModelAdmin):
      list_display   = ('patient_','socio_economics','education','housing_conditions','religion','race','languages_known')
      search_fields  = ('^patient__first_Name','^patient__other_Name')
      list_filter    = ('date_created','date_updated')
      list_per_page  = 20
      date_hierarchy    = 'date_created' 


class Patient_vitals_Admin(admin.ModelAdmin):
      list_display   = ('patient_','body_temp_','Blood_pressure_','Pulse','respiration_rate_','date')
      search_fields  = ('^patient__first_Name','^patient__other_Name')
      list_filter    = ('date_created','date_updated')
      list_per_page  = 20
      date_hierarchy    = 'date_created'
      raw_id_fields   =  ('patient',)


admin.site.register(Patient_detail,Patients_Admin)
admin.site.register(PatientGuardian,Guardian_Admin)
admin.site.register(Patient_vitals,Patient_vitals_Admin)
admin.site.register(VaccineRegistry,VaccineRegistry_Admin)
admin.site.register(PatientImmunisation,PatientImmunisation_Admin)
admin.site.register(PatientDemographicsData,PatientDemographic_Admin)
