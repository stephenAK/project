#date: 15/01/2013

from django.db     			 import models
from django.forms   			 import ModelForm
from django.contrib.auth.models 	 import User
from django.contrib.auth                 import REDIRECT_FIELD_NAME
from django.contrib.auth.forms           import AuthenticationForm
from django.contrib                      import admin
#from staff.models 			 import *
#from patient.models 			 import *



PMIS_USER_ROLES =      ( ('pmis_admin'    , 'Admin'     ) ,
                       ('Patient'       , ' Patient'      ) ,
                       ('Doctor'      , 'Doctor '    ) ,
                       ('Nurse'  , 'Nurse' ) ,
		       ('Cashier'  , 'Cashier' ) ,
		       ('Pharmacist'  , 'Phamacist' ) ,
                       ('pmis_user'  , 'Other User' ) ,

                     )


#Defining the models for Pmis user
# All Pmis uses should therefore be logged in and should have a role
# Fine grained permissions throughout the application can be set on role and 
# permissions defined here


class PmisUser(User):
   pmis_user_role   = models.CharField("Pmis User Role", 
                                          help_text   =""" Users Role in Pmis Software. 
                                                           This is different from the role in the Hospital""",  
                                          max_length  = 30, 
                                          choices     = PMIS_USER_ROLES,
                                          default     = "pmis_user"
                                          )
   date_created = models.DateTimeField (auto_now_add=True, blank =True, null = True)
   date_updated = models.DateTimeField (auto_now_add=True,blank =True, null = True)
   #user_details = models.ForeignKey(Staff_detail, related_name = "Staff Detail",blank = True, null = True)


   def full_name(self):
       return '%s %s' % (self.last_name.capitalize(),self.first_name.capitalize())
   
   
   def get_role(self):
      pass

class PmisUserInline(admin.StackedInline):
    pass# model = PmisUser

class PmisUserForm(AuthenticationForm):
   model = PmisUser

"""
PmisUser Admin
"""
class PmisUserAdmin(admin.ModelAdmin):
   list_display = ('username','full_name','pmis_user_role','last_login')
   search_fields = ('username','last_name')
   list_filter = ('pmis_user_role','last_login','date_created','date_updated')
   ordering = ('-last_login',)
   date_hierarchy = 'date_updated'

admin.site.register(PmisUser, PmisUserAdmin)


