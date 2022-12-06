from django.db import models
from django.contrib.auth.models import AbstractUser  
from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from custom_settings.grades import GradeChoices
from custom_settings.models import BaseModel
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
# Create your models here.


def only_int(value): 
    if value.isdigit()==False:
        raise ValidationError('ID contains characters')


class SchoolProfile(BaseModel):
    def get_upload_path(instance, filename):
        return 'school/{}/{}'.format(instance.school_name, filename)
    SCHOOLTYPE = (
          ('PR', 'Primary'),
          ('LS', 'Lower Secondary'),
          ('HS', 'Higher Secondary')
      )
    school_name = models.CharField(max_length=250,null=True,blank=False)
    address = models.CharField(max_length=50,null=True,blank=True)
    school_website = models.URLField(null=True,blank=True)
    school_type = models.CharField(max_length=50,null = True, choices = SCHOOLTYPE)
    school_email = models.CharField(max_length=50,null = True)
    phone_number = models.CharField(max_length=15,null = True, validators=[only_int])
    slug = models.SlugField(max_length=250,unique = True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to=get_upload_path, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    about_us = RichTextField(config_name='awesome_ckeditor',null = True,blank = True)

    
    def save(self, *args, **kwargs):
        super(SchoolProfile, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.school_name)
            if SchoolProfile.objects.filter(slug = self.slug).exists():
                self.slug = slugify(self.school_name) + "-" + str(self.id)
            self.save()

    def __str__(self):
        return f'{self.school_name}'


class User(AbstractUser):
    """Note: User already has email, firstname , lastname, username etc.
    important mandatory field is username and password"""
    email = models.EmailField(unique=True,max_length=254)    
    phone_number = models.CharField(max_length=15,null=True,blank=True,validators=[only_int])
    GENDER = (
          ('Male', 'Male'),
          ('Female', 'Female'),
          ('Other', 'Other')
      )
    gender = models.CharField(max_length=6,choices=GENDER,null=True,blank=True)
    dob = models.DateField(null=True, blank=True)
    school=models.ForeignKey(SchoolProfile,on_delete=models.CASCADE,null=True,blank=True,related_name='user_school')
    USER_TYPE = (
          ('NA', 'Nagar Admin'),
          ('SA', 'School Admin'),
          ('TE', 'Teacher'),
          ('ST', 'Student'),
          )  
    user_type = models.CharField(max_length=15, choices=USER_TYPE,null=True,blank=True)
    
    def __str__(self):
        return self.username


class StaffProfile(BaseModel):
    """
    this is only for Teacher profile 
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='staff_profile')
    address = models.CharField(max_length=50,null=True,blank=True)
    salary = models.IntegerField(blank=True, null=True)
    cv = models.FileField(upload_to='staffcv/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],blank=True, null=True)

    def __str__(self):
        if self.user.username is False:
            raise serializers.ValidationError(
                            'No teacher is created to display')
        return self.user.username

class TeacherProfile(BaseModel):
    """
    this is only for Teacher profile 
    """
    def get_upload_path(instance, filename):
        return 'teacher/{}/{}'.format(instance.user.school.school_name, filename)

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacher_profile')
    address = models.CharField(max_length=50,null=True,blank=True)
    salary = models.IntegerField(blank=True, null=True)
    religion =models.CharField(max_length=100, blank=True)
    caste =models.CharField(max_length=100, blank=True)
    department =models.CharField(max_length=100, blank=True)
    nationality =models.CharField(max_length=100, blank=True)
    experience =models.CharField(max_length=100, blank=True)
    joined_date = models.DateField(auto_now_add=False, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to=get_upload_path, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    cv = models.FileField(upload_to='staffcv/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],blank=True, null=True)

    def __str__(self):
        if self.user.username is False:
            raise serializers.ValidationError(
                            'No teacher is created to display')
        return self.user.username


class StudentProfile(BaseModel):
    def get_upload_path(instance, filename):
        return 'student/{}/{}'.format(instance.user.school.school_name, filename)

    """
    this is only for student
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_profile')
    address = models.CharField(max_length=50,null=True,blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    grade = models.CharField(choices=GradeChoices.choices,max_length=10)
    religion =models.CharField(max_length=100, blank=True)
    nationality =models.CharField(max_length=100, blank=True)
    caste =models.CharField(max_length=100, blank=True)
    roll_number =models.CharField(max_length=100, blank=True)
    admission_date = models.DateField(auto_now_add=False, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to=get_upload_path, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def __str__(self):
        if self.user.username is False:
            raise serializers.ValidationError(
                            'No student is created to display')
        return self.user.username


class LibrarianProfile(BaseModel):
    """
    this is only for Teacher profile 
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='librarian_profile')
    address = models.CharField(max_length=50,null=True,blank=True)
    salary = models.IntegerField(blank=True, null=True)
    cv = models.FileField(upload_to='LibrarianCV/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],blank=True, null=True)

    def __str__(self):
        if self.user.username is False:
            raise serializers.ValidationError(
                            'No librarian is created to display')
        return self.user.username


class ImageGallary(models.Model):
    def get_upload_path(instance, filename):
        try: 
            return 'gallary/{}/{}'.format(instance.school.school_name, filename)
        except:
            return 'gallary/{}/{}'.format('nagar_admin', filename)

    school = models.ForeignKey(SchoolProfile,on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=get_upload_path, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])


class HomePageSchoolAdmin(models.Model):
    title = models.CharField(max_length=200)
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
    description = RichTextField(config_name='awesome_ckeditor',null = True,blank = True)
    image = models.ImageField(upload_to='homepage-school/',null = True,blank = True)

    def __str__(self):
        return self.title