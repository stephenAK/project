from django.db import models
from django.contrib import admin
from patient.models import Patient_detail

#model for the various billings in the Hospital
class  bill_type(models.Model):
       name = models.CharField(max_length = 20)
       
       def __unicode__(self):
           return self.name.upper()
           
       class Meta:
		verbose_name 	    = "Billing Type"
		verbose_name_plural = "Billing types"
           
		
class patient_bill(models.Model):
      patient                 = models.ForeignKey(Patient_detail,related_name ='Patient')
      billing_type            = models.ForeignKey(bill_type,max_length = 20)
      mode_of_payment         = models.CharField('mode of payment',choices = (("CASH","CASH"),("CHEQUE","CHEQUE"),("NHIS","NHIS")),max_length = 10)
      is_paid                 = models.BooleanField(default = False,help_text = "Designates whether the patient has made payments.")#amount to be payment would be indicated by the cashier
      
      class Meta:
		verbose_name 	    = "Patient Bill"
		verbose_name_plural = "Patient Billings"
		
      def __unicode__(self):
           return self.mode_of_payment

class patient_bill_Admin(admin.ModelAdmin):
      list_display = ('patient','billing_type','mode_of_payment','is_paid')
      list_filter = ('mode_of_payment','is_paid')
      raw_id_fields = ('patient',)
      
      
#class bill_type_Admin(admin.ModelAdmin):
 #     list_display = ('name',)


admin.site.register(bill_type)#bill_type_Admin)
admin.site.register(patient_bill,patient_bill_Admin)
