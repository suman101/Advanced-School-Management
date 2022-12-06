from django.db import models
from authentication.models import SchoolProfile
from custom_settings.models import BaseModel
from grade_and_subject.models import Grade
from marksheet.models import Exam

# Create your models here.

class Report(BaseModel):
    def get_upload_path(instance, filename):
        return 'exam/{}/{}'.format(instance.school.school_name, filename)

    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path,
                           max_length=254, null=True, blank=True)
    
    def __str__(self):
        return f'{self.school.school_name}-{self.exam.title}-{self.grade.grade_name}'
    