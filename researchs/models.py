from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import SchoolProfile
from custom_settings.models import BaseModel
User = get_user_model()


def get_upload_path(instance, filename):
    try:
        return 'research_papers/{}/{}'.format(instance.published_by.school.school_name, filename)
    except:
        return 'research_papers/{}/{}'.format('nagar_admin', filename)



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, max_length=110)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()
    def __str__(self):
        return f'{self.name}'


class ResearchQuerySet(models.QuerySet):
    """krishna"""

    def not_approved(self):
        return self.filter(publish=True, approved=False)

    def public(self):
        return self.filter(publish=True, approved=True)
    def draft(self):
        return self.filter(publish=False)


class ResearchDetailManager(models.Manager):
    """krishna"""

    def get_queryset(self):
        return ResearchQuerySet(self.model, using=self._db)

    def not_approved(self):
        return self.get_queryset().not_approved()

    def public(self):
        return self.get_queryset().public()
    
    def draft(self):
        return self.get_queryset().draft()


class ResearchDetail(BaseModel):
    """suman -> krishna"""
    def get_upload_path(instance, filename):
        try:
            return 'research_papers/{}/{}'.format(instance.published_by.school.school_name, filename)
        except:
            return 'research_papers/{}/{}'.format('nagar_admin', filename)


    title = models.CharField(max_length=250, unique=True)
    # published_by = models.ForeignKey(User,max_length=100,on_delete=models.CASCADE,blank=True)
    published_by = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(null=True)
    link = models.URLField(max_length=100)
    pdf = models.FileField(upload_to=get_upload_path,
                           max_length=254, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    approved = models.BooleanField(default=True)
    publish = models.BooleanField(default=True)
    school = models.ForeignKey(SchoolProfile,on_delete = models.CASCADE,null = True,blank = True)
    objects = ResearchDetailManager()

    def save(self, *args, **kwargs):
        super(ResearchDetail, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            if ResearchDetail.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()

    def save(self, *args, **kwargs):
        super(ResearchDetail, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            if ResearchDetail.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()

# Dont use this Subject module. Please use the  grade and subject app.
class Subjects(models.Model):

    school = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
                               'user_type': 'SA'}, related_name='school_subject')
    subject = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.school.school_name}-{self.subject}'

# -----------------------------------------------------------------------------------------------------------


# class Subject(models.Model):
#     school=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'user_type': 'School'},related_name='school_subject')
#     subject_name=models.CharField(max_length=100)
