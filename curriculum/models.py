from django.db import models
from django.contrib.auth import get_user_model

from custom_settings.models import BaseModel
User = get_user_model()

# Create your models here.

class Curriculum(BaseModel):
    def get_upload_path(instance, filename):
        return 'curriculum/{}/{}'.format('nagar_admin', filename)


    title = models.CharField(max_length=100,null=True,blank=True)
    pdf = models.FileField(upload_to=get_upload_path,
                           max_length=254, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'user_type': 'NA'},null=True,blank=True) 
    is_published = models.BooleanField(default=True)


    def __str__(self):
        return self.title