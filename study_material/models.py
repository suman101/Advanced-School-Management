from django.db import models
from authentication.models import SchoolProfile
from django.template.defaultfilters import slugify
from custom_settings.models import BaseModel

# Create your models here.
class StudyMaterialQuerySet(models.QuerySet):
    """suds"""

    def not_approved(self):
        return self.filter(publish=True, approved=False)

    def public(self):
        return self.filter(publish=True, approved=True)
    def draft(self):
        return self.filter(publish=False)


class StudyMaterialManager(models.Manager):
    """suds"""

    def get_queryset(self):
        return StudyMaterialQuerySet(self.model, using=self._db)

    def not_approved(self):
        return self.get_queryset().not_approved()

    def public(self):
        return self.get_queryset().public()
    def draft(self):
        return self.get_queryset().draft()


class StudyMaterial(BaseModel):
    """suds"""
    def get_upload_path(instance, filename):
        try: 
            return 'study_materials/{}/{}'.format(instance.published_by.school.school_name, filename)
        except:
            return 'study_materials/{}/{}'.format('nagar_admin', filename)
        

    title = models.CharField(max_length=250, unique=True)
    published_by = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True)
    link = models.URLField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to=get_upload_path,
                           max_length=254, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    approved = models.BooleanField(default=True)
    publish = models.BooleanField(default=True)
    school = models.ForeignKey(SchoolProfile,on_delete = models.CASCADE,null = True,blank = True)
    objects = StudyMaterialManager()

    def save(self, *args, **kwargs):
        super(StudyMaterial, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            if StudyMaterial.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()