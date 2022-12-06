import os
from django.db import models
from authentication.models import TeacherProfile
from custom_settings.models import BaseModel
from grade_and_subject.models import Subjects, Grade
# Create your models here.


def get_upload_path(instance, filename):
    return os.path.join(
      "School_%s" % instance.teacher,"Teacher_%s" % instance.teacher.user, "Grade_%s" % instance.grade, filename)


class Notes(BaseModel):
    title = models.CharField(max_length=100,null=True)
    sub= models.ForeignKey(Subjects,on_delete=models.CASCADE,null=True,blank=True)
    teacher=models.ForeignKey(TeacherProfile,on_delete=models.SET_NULL,related_name='teacher_note',null=True,blank=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)
    notes_pdf=models.FileField(upload_to=get_upload_path, null=True, blank=True)

    def __str__(self):
      return self.title