from email import message
from django.db import models
#from django.db.models import Q
from authentication.models import User
from authentication.models import SchoolProfile


# Create your models here.

class Notice(models.Model):
    title = models.CharField(max_length=100)
    detail_notice = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='notice_pdf',max_length=254, null=True, blank=True)
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE,null=True,blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


#class Feedback(models.Model):
    #title = models.CharField(max_length=100)
    #school = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"user_type":'School'})
    #message = models.TextField()
    #sended_on = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return self.title


#class StudentFeedback(models.Model):
    #title = models.CharField(max_length=100)
    #student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    #message = models.TextField()
    #sended_on = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return self.title


#class Event(models.Model):
    #title = models.CharField(max_length=100)
    #posted_by = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'user_type': 'School'} )
    #description = models.CharField(max_length=200)
    #date_of_event = models.DateField()
    #created_on = models.DateTimeField(auto_now_add=True)
    #updated_on = models.DateTimeField(auto_now=True)

    #def __str__(self):
        #return f'{self.title}'