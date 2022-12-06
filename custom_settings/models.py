from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.core import exceptions
from django.template.defaultfilters import slugify
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PrivacyPolicy(BaseModel):
    """Suds"""
    content = RichTextField(config_name='awesome_ckeditor')
 

    def save(self, *args, **kwargs):
        if not self.pk and PrivacyPolicy.objects.exists():
            raise ValidationError('privacy policy can be created only once')
        return super(PrivacyPolicy, self).save(*args,**kwargs)


class TermsAndCondition(BaseModel):
    """Suds"""
    content = RichTextField(config_name='awesome_ckeditor')

    def save(self,*args,**kwargs):
        if not self.pk and TermsAndCondition.objects.exists():
            raise ValidationError('terms and conditions can be created only once')
        return super(TermsAndCondition, self).save(*args,**kwargs)


class SMTPSetting(models.Model):
    """Suds"""
    email_port = models.IntegerField(default=587)
    email_host_user = models.EmailField(blank=True, null=True)
    email_host_password = models.CharField(max_length=200, blank=True, null=True, help_text="Use the app password not your actual password for the security reason.")

    def __str__(self):
        return f'{self.email_host_user}'

    def save(self, *args, **kwargs):
        if not self.pk and SMTPSetting.objects.exists():
            raise exceptions.PermissionDenied('create action not allowed')
        return super(SMTPSetting, self).save(*args, **kwargs)

    def delete(self):
        raise exceptions.PermissionDenied('delete action not allowed')


class MailTemplate(models.Model):
    """Suds"""
    send_mail = RichTextField(help_text='required keywords: [EMAIL],[USERNAME],[PASSWORD]')
    # send_mail_password_reset = RichTextField(help_text='required keywords: [CODE],[EMAIL],[USERNAME]', null=True)
    # send_mail_verifed = RichTextField(help_text='required keywords: [EMAIL],[USERNAME]', null=True)
    # send_mail_password_change = RichTextField(help_text='required keywords: [EMAIL],[USERNAME]', null=True)
    # send_mail_order = RichTextField(help_text='required keywords: [EMAIL],[PRODUCT],[PRICE],[USERNAME]', null=True)

    def save(self, *args, **kwargs):
        if not self.pk and MailTemplate.objects.exists():
            raise exceptions.PermissionDenied('multiple create action not allowed')
        return super(MailTemplate, self).save(*args, **kwargs)


class CMS(BaseModel):
    title = models.CharField(max_length=200,unique = True)
    description = RichTextField(config_name='awesome_ckeditor',null = True,blank = True)
    image = models.ImageField(upload_to='cms/',null = True,blank = True)
    slug = models.SlugField(null = True,blank = True)
    m_title = models.CharField(max_length=200,null=True,blank=True)
    m_keyword = models.CharField(max_length=200,null=True,blank=True)
    m_description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(CMS, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            if CMS.objects.filter(slug = self.slug).exists():
                self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()
            

class AboutUs(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError('about us can be created only once')
        return super(AboutUs, self).save(*args,**kwargs)


class ContactUsForm(BaseModel):
    f_name = models.CharField(max_length=100)
    phone_code = models.CharField(max_length=5,null = True,blank = True)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=150,null = True)
    country = models.CharField(max_length=30)
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.f_name


class Faq(BaseModel):
    title = models.CharField(max_length=250,unique = True)
    description = RichTextField(config_name='awesome_ckeditor')


class HomePageNagarAdmin(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(config_name='awesome_ckeditor',null = True,blank = True)
    image = models.ImageField(upload_to='homepage-admin/',null = True,blank = True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk and HomePageNagarAdmin.objects.exists():
            raise ValidationError('Homepage can be created only once')
        return super(HomePageNagarAdmin, self).save(*args,**kwargs)
