from django.db import models
from django.contrib import admin
from datetime import datetime, date, time, timedelta

'''
This models contains the content of the medi-care site
Some of the content of the site shall include:
1.textual data-About the product
2. images
3. etc 
'''

class about_us(models.Model):
     ID = models.AutoField(primary_key=True,editable = False)
     post = models.TextField(blank = True, null = True)
     date_created        = models.DateTimeField (auto_now_add=True,blank =True, null = True)
     date_updated        = models.DateTimeField (auto_now=True,blank =True, null = True)


     class Meta:
		verbose_name 	    = "About Us"
		verbose_name_plural = "About Us"
     
     def __unicode__(self):
             return self.post
             
             
class post_content(models.Model):
      ID     = models.AutoField(primary_key=True,editable = False)
      post_1 = models.TextField(blank = True, null = True)
      post_2 = models.TextField(blank = True, null = True)
      post_3 = models.TextField(blank = True, null = True)
      post_4 = models.TextField(blank = True, null = True)
      post_5 = models.TextField(blank = True, null = True)
      post_6 = models.TextField(blank = True, null = True)
      post_7 = models.TextField(blank = True, null = True)
      post_9 = models.TextField(blank = True, null = True)
      post_10 = models.TextField(blank = True, null = True)
      date_created        = models.DateTimeField (auto_now_add=True,blank =True, null = True)
      date_updated        = models.DateTimeField (auto_now=True,blank =True, null = True)

      class Meta:
		verbose_name 	    = "post"
		verbose_name_plural = "posts"
		
      def __unicode__(self):
             return self.post_1
                    
#this models would contain all the images of the medi-care site             
class image_content(models.Model):
      name = models.TextField(blank = True, null = True)
      ID = models.AutoField(primary_key=True,editable = False)
      image_1 = models.ImageField(upload_to = 'tmp',blank = True, null =  True)
      image_2 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      image_3 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      image_4 = models. ImageField(upload_to = 'tmp',blank = True, null = True)
      image_5 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      image_6 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      image_7 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      image_8 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      image_9 = models.ImageField(upload_to = 'tmp',blank = True, null = True) 
      image_10 = models.ImageField(upload_to = 'tmp',blank = True, null = True)
      date_created        = models.DateTimeField (auto_now_add=True,blank =True, null = True)
      date_updated        = models.DateTimeField (auto_now=True,blank =True, null = True)

      class Meta:
		verbose_name 	    = "image"
		verbose_name_plural = "images"
		
      def __unicode__(self):
             return self.name
             
             
class about_us_Admin(admin.ModelAdmin):
      list_display	 = ('post','date_created','date_updated')
      list_filter 	 = ('date_created','date_updated') 
      date_hierarchy     = 'date_created' 


class post_Admin(admin.ModelAdmin):
      list_display	 = ('post_1','post_2','post_3','post_4','post_5','date_created','date_updated')
      list_filter 	 = ('date_created','date_updated') 
      date_hierarchy     = 'date_created' 
                             
class image_Admin(admin.ModelAdmin):
      list_display	 = ('image_1','image_2','image_3','image_4','image_5')
      list_filter 	 = ('date_created','date_updated') 
      date_hierarchy     = 'date_created' 
      
admin.site.register(about_us, about_us_Admin)
admin.site.register(image_content,image_Admin)
admin.site.register(post_content,post_Admin)
     
      
 








