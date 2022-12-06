from django.db import models
from authentication.models import SchoolProfile, TeacherProfile
from custom_settings.models import BaseModel
from custom_settings.grades import GradeChoices
# Create your models here.


class Subjects(BaseModel):
    subject=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id}-{self.subject}'


class Grade(BaseModel):
    grade_name = models.CharField(choices=GradeChoices.choices,max_length=10,default=GradeChoices.ONE)
    section = models.CharField(max_length=10,default='A')
    subject = models.ManyToManyField(Subjects, related_name='sub_grade')
    admission_fee = models.FloatField(null=True, blank=True)
    monthly_fee = models.FloatField(null=True, blank=True)
    extra_fee = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.grade_name}'


class ClassRoutine(BaseModel):
    school =models.ForeignKey(SchoolProfile,on_delete=models.CASCADE,related_name='school_routine')
    teacher = models.ForeignKey(TeacherProfile,on_delete=models.SET_NULL,related_name='routine_teacher',null=True,blank=True)
    grade =models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)
    sub= models.ForeignKey(Subjects,on_delete=models.CASCADE,null=True,blank=True)
    time = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return f'{self.school.school_name}-{self.teacher.user.username}-{self.grade.grade_name}'