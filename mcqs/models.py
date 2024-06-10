from django.db import models
import datetime
from authentication.models import StudentProfile, TeacherProfile
from django.utils.translation import gettext_lazy  as _
from custom_settings.models import BaseModel
from grade_and_subject.models import Subjects, Grade
from django.db.models.signals import pre_save
# Create your models here.
#from authentication.models import User

class QuizManager(models.Manager):
    pass


class Quiz(BaseModel):
    """models"""
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)
    sub= models.ForeignKey(Subjects,on_delete=models.CASCADE,null=True,blank=True)
    teacher = models.ForeignKey(TeacherProfile,on_delete=models.SET_NULL,related_name='teacher_quiz',null=True,blank=True)
    title = models.CharField(max_length=150,unique = False)
    description = models.TextField(blank=True)
    total_question = models.IntegerField(default=0)
    publish = models.BooleanField(default=False)
    quiz_duration = models.IntegerField(default=0)
    published_date = models.DateTimeField(null=True,blank=True)
    attended_users = models.ManyToManyField(StudentProfile,blank=True,related_name = 'attended_user')

    objects = QuizManager()

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if self.publish is False:
            self.published_date = None
        else:
            self.published_date = datetime.datetime.today()
        super(Quiz,self).save(*args,**kwargs)


class Questions(BaseModel):
    """models"""
    question = models.TextField(blank=True)
    option1 = models.CharField(max_length=250)
    option2 = models.CharField(max_length=250)
    option3 = models.CharField(max_length=250)
    option4 = models.CharField(max_length=250)
    answer = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="question_quiz")
    attended_users = models.ManyToManyField(StudentProfile,blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Questions'


class AnswerSheet(BaseModel):
    """models"""
    user_id = models.PositiveSmallIntegerField(default=1)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="questionanswer")
    user_answer = models.CharField(max_length=150,null=True,blank=True)
    is_true = models.BooleanField(default = False)

    def __str__(self):
        return str(self.question)


class AttemptedQuiz(BaseModel):
    """models"""
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    mark_obtain = models.PositiveSmallIntegerField(default=0)
   

    def __str__(self):
        return f'{self.user}|{self.mark_obtain}'


class ShortQuestion(BaseModel):
    """models"""
    #quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)
    sub= models.ForeignKey(Subjects,on_delete=models.CASCADE,null=True,blank=True)
    teacher = models.ForeignKey(TeacherProfile,on_delete=models.SET_NULL,related_name='teacher_SQ',null=True,blank=True)
    question = models.TextField()
    answer = models.TextField()
    mark = models.PositiveIntegerField(default=2)
    attended_users = models.ManyToManyField(StudentProfile,blank=True)
    

    def __str__(self):
        return self.question


class ShortAnswerSheet(BaseModel):
    """models"""
    def get_upload_path(instance, filename):
        return 'shortanswersheet/{}/{}'.format(instance.short_question.sub.school.school_name, filename)

    user_id = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    short_question = models.ForeignKey(ShortQuestion, on_delete=models.CASCADE, related_name="shortquestionanswer")
    user_answer = models.TextField(null=True,blank=True)
    answer_file = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    mark_ob = models.CharField(max_length=2,null=True,blank=True)

    def __str__(self):
        return f'{self.user_id.user.username}-{self.short_question.question}'