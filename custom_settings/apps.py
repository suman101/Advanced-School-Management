from django.apps import AppConfig
from django.db.models.signals import post_migrate


def generate_initial_obj(sender, **kwargs):
    from .models import SMTPSetting, MailTemplate, AboutUs, PrivacyPolicy, TermsAndCondition,HomePageNagarAdmin

    if not SMTPSetting.objects.exists():
        SMTPSetting.objects.create(email_host_user=None)
    
    if not AboutUs.objects.exists():
        AboutUs.objects.create()

    if not MailTemplate.objects.exists():
        MailTemplate.objects.create()

    if not TermsAndCondition.objects.exists():
        TermsAndCondition.objects.create()
        
    if not PrivacyPolicy.objects.exists():
        PrivacyPolicy.objects.create()
    
    if not HomePageNagarAdmin.objects.exists():
        HomePageNagarAdmin.objects.create()
        
class CustomSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_settings'

    def ready(self):
        post_migrate.connect(generate_initial_obj, sender=self)
