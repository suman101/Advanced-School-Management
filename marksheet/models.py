from django.db import models
from authentication.models import SchoolProfile, StudentProfile
from custom_settings.grades import GradeChoices
from django.core.validators import ValidationError
from custom_settings.models import BaseModel
from grade_and_subject.models import Grade, Subjects
from django.core.validators import FileExtensionValidator

# Create your models here.


class Exam(BaseModel):
    def get_upload_path(instance, filename):
        return 'exam/{}/{}'.format(instance.school.school_name, filename)
    
    
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True)
    routine = models.FileField(upload_to=get_upload_path,
                           max_length=254, null=True, blank=True)
    start_date = models.DateField(blank=True, null=True, auto_now_add=False)
    
    def __str__(self):
        return f'{self.title}'


class Marksheet(BaseModel):
    def get_upload_path(instance, filename):
        return 'marksheet/{}/{}'.format(instance.exam.school.school_name, filename)
    # student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='std_marksheet', null=True, blank=True)
    # student=models.CharField(max_length=150,null = True)

    exam=models.ForeignKey(Exam,on_delete=models.PROTECT,related_name='exam_marksheet',null=True,blank=True)
    grade = models.ForeignKey(Grade,on_delete=models.PROTECT,null=True,blank = True)
    file = models.FileField(upload_to=get_upload_path,
                           max_length=254, null=True, blank=True,validators=[FileExtensionValidator(allowed_extensions=['csv'])],)

    def __str__(self):
        return f'{self.grade}-{self.exam}'


class Marks(BaseModel):
    marksheet=models.ForeignKey(Marksheet,on_delete=models.CASCADE,related_name='mark_marksheet',null=True,blank=True)
    sub= models.CharField(max_length=150,null = True)
    student=models.CharField(max_length=150,null = True)

    obtain_mark = models.FloatField(default=0)
    full_mark = models.FloatField(default=4)

    def clean(self):
        if self.full_mark > 4:
            raise ValidationError("Full GPA should not be more than 4")
        if self.obtain_mark > 4:
            raise ValidationError("Obtain GPA should not be more than 4")

    def __str__(self):
        return f'{self.marksheet}'

    # def get_total_std_count(self)
