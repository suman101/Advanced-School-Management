import mailbox
from django.db import models
from custom_settings.models import BaseModel
import os
# Create your models here.

def get_upload_path(instance, filename):
    return os.path.join(
      "School_%s" % "Mailbox_%s" % instance.sender, filename)

class Mailboxes(BaseModel):
    sender = models.CharField(max_length=100)
    subject = models.CharField(max_length=250, null=True, blank=True)
    send_to = models.EmailField()
    body = models.TextField()
    file = models.FileField(upload_to=get_upload_path,null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    #spam = models.
    trash = models.BooleanField(default=False)
    important =models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}-{self.subject}'
